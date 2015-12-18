##
# load movie data from file
# 
##

import csv

class movieUtil:
  def __init__(self,path='../dataset/full/'):
    self.movies = self.loadMovieData(path)

  def loadMovieData(self,path):
    # Get movie titles
    movies = {}
    with open(path+'movies.csv','rb') as f:
      has_header = csv.Sniffer().has_header(f.read(1024))
      f.seek(0)
      reader = csv.reader(f)
      if has_header: next(reader)
      for row in reader:
        (id,title) = (int(row[0]),row[1])
        movies[id] = title
    return movies

  def getMovieById(self,id):
    return self.movies[id]