##
#
# load tag data from database
# figure out two relations:
# 1. tag-movies
# 2. user-tags
#
##

import dbconfig
from math import sqrt

# return all tags
def getTaglist():
  cursor = dbconfig.getCursor()
  cursor.execute("select distinct tag from tags")
  rows = cursor.fetchall()
  taglist = []
  for r in rows: taglist.append(r[0])
  return taglist

# return sum of tag count 
def tagSum(tag):
  cursor = dbconfig.getCursor()
  cursor.execute("select * from tags where tag = '" + tag.replace("'","''") +"'")
  return cursor.rowcount

# return tag-movies
def tagMovies(tag):
  cursor = dbconfig.getCursor()
  cursor.execute("select movieid from tags where tag = '" + tag.replace("'","''") +"'")
  rows = cursor.fetchall()
  tag_movies = {}
  for r in rows:
    if r[0] in tag_movies: tag_movies[r[0]] += 1
    else: tag_movies[r[0]] = 1
  return tag_movies

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
def tagTopSimilarTags(tag,top=50,min=10):
  simtagdir = []
  for t in getTaglist():
    if tagSum(t) >= min and t != tag: simtagdir.append([tagSimilar(tag,t),t])
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