import psycopg2
from imdb import IMDb
import re

def get_cursor():
  conn_str = "host='localhost' dbname='movielen_1m' user='dbuser' password='dbuser'"
  # print "Connecting to database\n ->%s" % (conn_str)
  conn = psycopg2.connect(conn_str)
  cursor = conn.cursor()
  # print "Connected!\n"
  return cursor

def get_null_list():
  cursor = get_cursor()
  cursor.execute("select imdbid from plots where (plot <> '') IS NOT TRUE")
  return cursor.fetchall()

def insert_role(plot,imdbid):
  conn_str = "host='localhost' dbname='movielen_1m' user='dbuser' password='dbuser'"
  # print "Connecting to database\n ->%s" % (conn_str)
  conn = psycopg2.connect(conn_str)
  cursor = conn.cursor()
  cursor.execute("update plots set plot = '"+plot+"' where imdbid='"+imdbid+"'")
  conn.commit()

def get_plot_for_null(null_list):
  imdb_list = []
  for l in null_list:
    plot_str = ''
    id = l[0]
    print id
    movie = IMDb().get_movie(id)
    plot = movie.get('plot')
    if plot:
      for p in plot: plot_str += p
      plot_str = plot_str.replace("\'", "")
      plot_str = plot_str.replace("\"", "")
      print plot_str
      insert_role(plot_str,id)



def main():
  # print len(get_null_list())
  null_list = get_null_list()
  get_plot_for_null(null_list)