
# load ratings data from file
# find out {user,{movie:rating}}
# find out the top n user fravorite movies according to ratings

import csv
from datetime import datetime
import psycopg2
import sys

def getCursor():
  conn_str = "host='localhost' dbname='tagrecsys' user='dbuser' password='dbuser'"
  print "Connecting to database\n ->%s" % (conn_str)
  conn = psycopg2.connect(conn_str)
  cursor = conn.cursor()
  print "Connected!\n"
  return cursor

# def getRatings(path='../dataset/full/'):
#   ratings = {}
#   print str(datetime.now())
#   with open(path+'ratings.csv','rb') as f:
#     reader = csv.reader(f)
#     for row in reader:
#       (userid,movieid,rating,timestamp) = row[:]
#       if userid in ratings:
#         ratings[userid][movieid] = [rating,timestamp]
#       else: ratings.setdefault(userid,{movieid:[rating,timestamp]})
#   print datetime.now()
#   return ratings

def getUserRatings(user):
  cursor = getCursor()
  cursor.execute("select rating,time,movieid from ratings where userid = " + str(user))
  rows = cursor.fetchall()
  rows.sort()
  rows.reverse()
  return rows

def userMovieAffinity(user):
  mlist = getUserRatings(user)
  timemax = mlist[0][1]
  movieaffinity = {}
  for m in mlist:
    if m[1]>timemax: timemax = m[1]
  for m in mlist:
    movieaffinity[m[2]] = m[0]*m[1]/timemax
  print "user rating count:"+str(len(movieaffinity))
  return movieaffinity

