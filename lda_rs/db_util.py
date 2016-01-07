import psycopg2
import sys

def get_cursor():
  conn_str = "host='localhost' dbname='movielen_1m' user='dbuser' password='dbuser'"
  # print "Connecting to database\n ->%s" % (conn_str)
  conn = psycopg2.connect(conn_str)
  cursor = conn.cursor()
  # print "Connected!\n"
  return cursor

def get_all_plots():
  cursor = get_cursor()
  cursor.execute("select movieid,plot from plots")
  return cursor.fetchall()

def get_imdb_id(movieid):
  cursor = get_cursor()
  cursor.execute("select imdbid from links where movieid = " + str(movieid))
  return cursor.fetchone()[0]

def get_mv_tags(mvid):
  cursor = get_cursor()
  cursor.execute("select tag from tags where movieid = " + str(mvid))
  return cursor.fetchall()

def get_user_list():
  user_list = []
  cursor = get_cursor()
  cursor.execute("select distinct userid from rating_train where rating > 3.0")
  return_list = cursor.fetchall()
  for r in return_list:
    user_list.append(r[0])
  return user_list

def get_movie_plots(mvid_list):
  list_query_str = ''
  c = 0
  for m in mvid_list:
    c += 1
    if c < len(mvid_list): s = "movieid="+str(m) + " or "
    else: s = "movieid="+str(m).strip()
    list_query_str += s
  cursor = get_cursor()
  print list_query_str
  cursor.execute("select plot from plots where "+ list_query_str)
  return cursor.fetchall() 

def get_movie_list():
  mv_list = []
  cursor = get_cursor()
  cursor.execute("select distinct movieid from rating_train")
  return_list = cursor.fetchall()
  for r in return_list:
    mv_list.append(r[0])
  return mv_list

def get_test_movie_list():
  mv_list = []
  cursor = get_cursor()
  cursor.execute("select distinct movieid from rating_test")
  return_list = cursor.fetchall()
  for r in return_list:
    mv_list.append(r[0])
  return mv_list

def get_movie_from_users(user_list):
  tuple_str = str(user_list)
  cursor = get_cursor()
  cursor.execute("select userid,movieid from rating_train where rating>3.0 and userid in "+ tuple_str)
  return_list = cursor.fetchall()
  return return_list

def non_common(set1,set2):
  common_item = {}
  no_item = []
  for s in set1:
    if s not in set2:
      # common_item[s] = 1
      no_item.append(s)
  return no_item

class user_info():
  def __init__(self,userid):
    self.user_ratings = self.get_user_ratings(userid)
    self.user_mv_list = self.get_user_mv_ids(self.user_ratings)
    # self.user_imdb_list = self.get_user_mv_imdbs(self.user_ratings)

  def get_user_ratings(self,userid):
    cursor = get_cursor()
    cursor.execute("select movieid,rating,timestamp from rating_train where rating > 3.0 and userid = " + str(userid))
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
  # train = get_movie_list()
  # test = get_test_movie_list()
  # no_list = non_common(test,train)
  # print no_list
  print get_movie_from_users((1,2,3))