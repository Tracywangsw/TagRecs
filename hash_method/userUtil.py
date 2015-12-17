import csv
import movieUtil

def loadRatingdata(path='./dataset/full/'):
  ratings = {}
  with open(path+'ratings.csv','rb') as f:
    reader = csv.reader(f)
    for row in reader:
      (userid,movieid,rating) = row[0:3]
      ratings.setdefault(userid,{})
      ratings[userid][movieUtil.getMovieById(movieid)] = rating
  return ratings

def userMovies(user):
  return loadRatingdata()[user]