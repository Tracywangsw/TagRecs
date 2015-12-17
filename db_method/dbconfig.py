import psycopg2
import sys

def getCursor():
  conn_str = "host='localhost' dbname='tagrecsys' user='dbuser' password='dbuser'"
  print "Connecting to database\n ->%s" % (conn_str)
  conn = psycopg2.connect(conn_str)
  cursor = conn.cursor()
  print "Connected!\n"
  return cursor