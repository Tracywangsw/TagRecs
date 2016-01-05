import psycopg2
import sys

def get_cursor():
  conn_str = "host='localhost' dbname='movielen_1m' user='dbuser' password='dbuser'"
  # print "Connecting to database\n ->%s" % (conn_str)
  conn = psycopg2.connect(conn_str)
  cursor = conn.cursor()
  # print "Connected!\n"
  return cursor

# def get_movie_by_id(id):
#   cursor = get_cursor()
#   cursor.execute("select * from movies where movieid = " + str(id))
#   return cursor.fetchone()[1]

def get_imdb_id(movieid):
  cursor = get_cursor()
  cursor.execute("select imdbid from links where movieid = " + str(movieid))
  return cursor.fetchone()[0]

def get_mv_tags(mvid):
  cursor = get_cursor()
  cursor.execute("select tag from tags where movieid = " + str(mvid))
  # print cursor.fetchall()
  return cursor.fetchall()

def get_user_list():
  user_list = []
  cursor = get_cursor()
  cursor.execute("select distinct userid from rating_train")
  return_list = cursor.fetchall()
  for r in return_list:
    user_list.append(r[0])
  return user_list

class user_info():
  def __init__(self,userid):
    self.user_ratings = self.get_user_ratings(userid)
    self.user_mv_list = self.get_user_mv_ids(self.user_ratings)
    self.user_imdb_list = self.get_user_mv_imdbs(self.user_ratings)

  def get_user_ratings(self,userid):
    cursor = get_cursor()
    cursor.execute("select movieid,rating,timestamp from rating_train where rating > 3.5 and userid = " + str(userid))
    rating_list = cursor.fetchall()
    return rating_list

  def get_user_mv_ids(self,ratings):
    mv_list = []
    for r in ratings:
      mv_list.append(r[0])
    return mv_list

  def get_user_mv_imdbs(self,ratings):
    mv_list = []
    for r in ratings:
      mv_list.append(get_imdb_id(r[0]))
    return mv_list


def main():
  # print user_info(id).user_imdb_list
  # get_mv_tags(1)
  print get_user_list()