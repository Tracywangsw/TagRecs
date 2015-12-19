# estimate tag-based collaborative flitering method

# e = user-tag-movie

# r = user-movie

# precise = e/r

# import psycopg2
import rs
import tagUtil
import csv
import datetime

class estimate:

  # def __init__(self):


  # def getCursor(self):
  #   conn_str = "host='localhost' dbname='tagrecsys' user='dbuser' password='dbuser'"
  #   print "Connecting to database\n ->%s" % (conn_str)
  #   conn = psycopg2.connect(conn_str)
  #   cursor = conn.cursor()
  #   print "Connected!\n"
  #   return cursor

  def recordUserRecommends(self):
    user = tagUtil.tagUtil()
    userlist = user.userlist()
    res = rs.rs()
    recordlist = []
    print 'estimate start,datetime:'+ str(datetime.datetime.now())

    for u in userlist:
      r = len(user.userMovies(u))
      e = res.getRecommendMovies(u)[1]
      recordlist.append([u,float(e)/r,r,e])

    print 'estimate end,datetime:'+ str(datetime.datetime.now())

    self.writeFile(recordlist)

  def writeFile(self,recordlist):
    # recordlist=[[1,2,3],[2,2,3]]
    with open('./estimate.csv','w') as f:
      a = csv.writer(f,delimiter=',')
      a.writerows(recordlist)

def main():
  es = estimate()
  es.recordUserRecommends()





