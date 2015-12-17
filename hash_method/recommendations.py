import csv
import sys
import pdb
from math import sqrt

def loadMovieLens(path='./dataset/full/'):
  # Get movie titles
  movies = {}
  with open(path+'movies.csv','rb') as f:
    line = csv.reader(f)
    for row in line:
      (id,title) = row[0:2]
      movies[id] = title
  return movies

def getMovieById(id):
  return loadMovieLens()[id]

# Stat tags of users
def statUserAndTag(path='./dataset/full/'):
  (user,taglist) = ({},{})
  with open(path+'tags.csv','rb') as f:
    reader = csv.reader(f)
    for row in reader:
      (userid,movieid,tag,ts) = row[:]

      if tag in taglist:
        taglist[tag]['count'] += 1
        if movieid in taglist[tag]['movielist']: taglist[tag]['movielist'][movieid] += 1
        else: taglist[tag]['movielist'][movieid] = 1
      else:
        taglist.setdefault(tag,{'count':1,'movielist':{movieid:1}})

      if userid in user:
        if ts < user[userid]['userfirst']: user[userid]['userfirst'] = ts
        if ts > user[userid]['userlast']: user[userid]['userlast'] = ts
        if tag in user[userid]['taglist']:
          user[userid]['taglist'][tag]['count'] += 1
          if ts < user[userid]['taglist'][tag]['tsfirst']: user[userid]['taglist'][tag]['tsfirst'] = ts
          if ts > user[userid]['taglist'][tag]['tslast']: user[userid]['taglist'][tag]['tslast'] = ts
        else:
          user[userid]['taglist'][tag] = {'count':1,'tsfirst':ts,'tslast':ts}
      else:
        user.setdefault(userid,{'taglist':{tag:{'count':1,'tsfirst':ts,'tslast':ts}},'userfirst':ts,'userlast':ts})
  return [user,taglist]


# tag tf-idf, input user id(string)
def userTopTags(user,userlist=statUserAndTag()[0],min=5,top=50):
  tagsort = []
  for tag in userlist[user]['taglist']:
     if statGlobalTags(tag) >= min: #tag-movies count >= min
      tagfrequency = float(userlist[user]['taglist'][tag]['count'])/statGlobalTags(tag)
      tagsort.append([tagfrequency,tag])
  tagsort.sort()
  tagsort.reverse()
  return tagsort[0:top]

# input tag name,return tag count
def statGlobalTags(tag,taglist=statUserAndTag()[1]):
  return taglist[tag]['count']

# input tag name,return tag-movies
def tagMovies(tag,taglist=statUserAndTag()[1]):
  return taglist[tag]['movielist']

def getCommonMovies(tag1,tag2):
  (tag1movies,tag2movies) = (tagMovies(tag1),tagMovies(tag2))
  common = {}
  for item in tag1movies: 
    if item in tag2movies: 
      common[item] = 1
  return common

# input two tag, return the similarity
def tagSimilar(tag1,tag2):
  (tag1movies,tag2movies) = (tagMovies(tag1),tagMovies(tag2))
  common = getCommonMovies(tag1,tag2)
  if len(common) == 0: return 0

  sum1 = sum([tag1movies[item] for item in common])
  sum2 = sum([tag2movies[item] for item in common])

  sum1sq = sum([pow(tag1movies[item],2) for item in common])
  sum2sq = sum([pow(tag2movies[item],2) for item in common])
  tagsum = sum([tag1movies[item]*tag2movies[item] for item in common])

  # num = tagsum-(sum1*sum2/len(common))
  # den=sqrt((sum1sq-pow(sum1,2)/len(common))*(sum2sq-pow(sum2,2)/len(common)))

  # if den == 0: return 0
  # rate = float(pow(len(common),2))/(len(tag1movies)*len(tag2movies))
  rate = float(len(common))/(len(tag1movies)+len(tag2movies)-len(common))
  return float(tagsum*rate)/sqrt(sum1sq*sum2sq)

#input tag name, return the most similar top n tags
def tagTopSimilarTags(tag,top=50,min=10,taglist=statUserAndTag()[1]):
  simtagdir = []
  for t in taglist:
    if statGlobalTags(t) >= min and t != tag:
      simtagdir.append([tagSimilar(tag,t),t])
  simtagdir.sort()
  simtagdir.reverse()
  return simtagdir[0:top]

# return user-candidate-tags
def getCandidateTags(user,top=20):
  (finaltags,usertags,sorttag) = ({},{},[])
  for t in userTopTags(user,top=50): usertags[t[1]] = t[0]
  for t in usertags: finaltags[t] = usertags[t]
  for t in usertags: finaltags = tagAffinityRecursion(t,usertags,finaltags)

  for tag in finaltags: sorttag.append([finaltags[tag],tag])
  sorttag.sort()
  sorttag.reverse()
  return sorttag[0:top]

def tagAffinityRecursion(tag,usertags,finaltags):
  for t in tagTopSimilarTags(tag,top=10):
    (simscore,simtag) = t[:]
    if simtag in finaltags: finaltags[simtag] += usertags[tag]*simscore
    else: finaltags[simtag] = usertags[tag]*simscore
  return finaltags

def tagTopMovies(tag,top=20):
  moviesort = []
  tagmovies = tagMovies(tag)
  total = sum([tagmovies[m] for m in tagmovies])
  for m in tagmovies: moviesort.append([float(tagmovies[m])/total,m])
  moviesort.sort()
  moviesort.reverse()
  return moviesort[0:top]

# recommend items attach to the tags
def getCandidateMovies(user):
  tags = getCandidateTags(user)
  (movierank,usertags) = ({},{})
  for t in tags: usertags[t[1]] = t[0]
  for t in tags:
    movierank = movieAffinityRecursion(t[1],movierank,usertags)
  return movierank

def movieAffinityRecursion(tag,movierank,usertags):
  ms = tagTopMovies(tag)
  for m in ms:
    (moviescore,movieid) = m[:]
    if movieid in movierank:
      movierank[movieid] += moviescore*usertags[tag]
    else: movierank[movieid] = moviescore*usertags[tag]
  return movierank

def getRecommendMovies(user,top=30):
  movies = getCandidateMovies(user)
  rankmovies = []
  for m in movies: rankmovies.append([movies[m],getMovieById(m)])
  rankmovies.sort()
  rankmovies.reverse()
  return rankmovies[0:top]

##
# 1.user-movie-rating(consider the influence of rating)
#   1.1 need to remove the movies that the given user has seen
# 
# 2.tag duration and tag recency
# 
# 3.tag ambiguity and tag synonyms(using wordNet or wordvector)
#
# 4.what about the user did not tag ? how to recommend for the user?
#
# 5.code need to reorangise
##

