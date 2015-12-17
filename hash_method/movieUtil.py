##
# load movie data from file
# 
##

import csv

def loadMovieData(path='../dataset/full/'):
  # Get movie titles
  movies = {}
  with open(path+'movies.csv','rb') as f:
    line = csv.reader(f)
    for row in line:
      (id,title) = row[0:2]
      movies[id] = title
  return movies

def getMovieById(id):
  return loadMovieData()[id]