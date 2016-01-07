import db_util
from imdb import IMDb
import csv

def get_mv_plot(mvid):
  imdbid = db_util.get_imdb_id(mvid)
  movie = IMDb().get_movie(id)
  plot = movie.get('plot')
  return plot

def plot_list():
  train = db_util.get_movie_list()
  test = db_util.get_test_movie_list()
  mv_list = db_util.non_common(test,train)
  # mv_list = db_util.get_movie_list()
  record_list = []
  i = 0
  record_list.append(['movieid','imdbid','plot'])
  for m in mv_list:
    # plot_str = ''
    imdbid = db_util.get_imdb_id(m)
    movie = IMDb().get_movie(imdbid)
    plot = movie.get('plot')
    # for p in plot: plot_str += p
    print [m,imdbid,plot]
    record_list.append([m,imdbid,plot])
  return record_list

def write_file(recordlist,path):
  with open(path,'w') as f:
    a = csv.writer(f,delimiter=',')
    a.writerows(recordlist)

def read_file(path):
  data_list = []
  if path.endswith('.csv'):
    with open(path,'rb') as f:
      # has_header = csv.Sniffer().has_header(f.read(1024))
      # f.seek(0)
      reader = csv.reader(f)
      # if has_header: next(reader)
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
  write_file(plot_list(),path='../dataset/outputFile/plot2.csv')
  # data = read_file(path='../dataset/outputFile/plot.csv')
  # print data[1][2]