import dbconfig

def getMovieById(id):
  cursor = dbconfig.getCursor()
  cursor.execute("select * from movies where movieid = " + str(id))
  print cursor.fetchone()[1]
