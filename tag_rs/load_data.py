import csv
import psycopg2

class LoadData:

  def get_test_set(self,path='../dataset/outputFile/tag_test_after_cleaning.csv'):
    return self.read_file(path)

  def get_train_set(self,path='../dataset/outputFile/tag_train_after_cleaning.csv'):
    return self.read_file(path)

  def get_whole_set(self,path='../dataset/movielen/tags.csv'):
    return self.read_file(path)

  def read_file(self,path):
    data_list = []
    if path.endswith('.csv'):
      with open(path,'rb') as f:
        has_header = csv.Sniffer().has_header(f.read(1024))
        f.seek(0)
        reader = csv.reader(f)
        if has_header: next(reader)
        for row in reader: data_list.append(row)
      return data_list
    elif path.endswith('.dat'):
      with open(path,'rb') as f:
        next(f)
        for row in f:
          row = row.strip()
          row = row.split("\t")
          data_list.append(row)
      return data_list

def main():
  lists = LoadData().read_file('../dataset/movielen/links.csv')
  conn_str = "host='localhost' dbname='tagrecsys' user='dbuser' password='dbuser'"
  print "Connecting to database\n ->%s" % (conn_str)
  conn = psycopg2.connect(conn_str)
  cursor = conn.cursor()
  # cursor.execute("select * from movies where movieid=1")
  # print cursor.fetchone()
  for l in lists:
    (movieid,imdbid) = (int(l[0]),l[1])
    cursor.execute("update movies set imdbid = '"+imdbid + "' where movieid ="+str(movieid))
  conn.commit()