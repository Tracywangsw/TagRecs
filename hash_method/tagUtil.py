##
#
# load tag data from dataset
# figure out two relations:
# 1. tag-movies
# 2. user-tags
#
##

import csv
from math import sqrt

## Stat tags of users and movies of tags
def statUserAndTag(path='../dataset/full/'):
  (user,taglist,usermovies) = ({},{},{})
  with open(path+'tags.csv','rb') as f:
    has_header = csv.Sniffer().has_header(f.read(1024))
    f.seek(0)
    reader = csv.reader(f)
    if has_header: next(reader)
    for row in reader:
      (userid,movieid,tag,ts) = (int(row[0]),int(row[1]),row[2],int(row[3]))

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

      if userid in usermovies:
        usermovies[userid].append(movieid)
      else: usermovies.setdefault(userid,[movieid])
  return [user,taglist,usermovies]


## tag-movies relation

# input tag name,return tag count
def statGlobalTags(tag,taglist=statUserAndTag()[1]):
  return taglist[tag]['count']

# input tag name,return tag-movies
def tagMovies(tag,taglist=statUserAndTag()[1]):
  return taglist[tag]['movielist']

# return common movies of the two tags
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

  rate = float(len(common))/(len(tag1movies)+len(tag2movies)-len(common))
  return float(tagsum*rate)/sqrt(sum1sq*sum2sq)

# input tag name, return the most similar top n tags
def tagTopSimilarTags(tag,top=50,min=10,taglist=statUserAndTag()[1]):
  simtagdir = []
  for t in taglist:
    if statGlobalTags(t) >= min and t != tag: simtagdir.append([tagSimilar(tag,t),t])
  simtagdir.sort()
  simtagdir.reverse()
  return simtagdir[0:top]

# return tag top movies according to movie frequency
def tagTopMovies(tag,top=20):
  moviesort = []
  tagmovies = tagMovies(tag)
  total = sum([tagmovies[m] for m in tagmovies])
  for m in tagmovies: moviesort.append([float(tagmovies[m])/total,m])
  moviesort.sort()
  moviesort.reverse()
  return moviesort[0:top]


## user-tags relation

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

## user-movies relation

def userMovies(user):
  usermovies = statUserAndTag()[2][user]
  print "user tagging movie count:"+str(len(usermovies))
  return usermovies

