import csv

class LoadData:

  def get_test_set(self,path='../dataset/outputFile/tag_test_after_cleaning.csv'):
    return self.read_file(path)

  def get_train_set(self,path='../dataset/outputFile/tag_train_after_cleaning.csv'):
    return self.read_file(path)

  def get_whole_set(self,path='../dataset/full/tags.csv'):
    return self.read_file(path)

  def read_file(self,path):
    data_list = []
    with open(path,'rb') as f:
      has_header = csv.Sniffer().has_header(f.read(1024))
      f.seek(0)
      reader = csv.reader(f)
      if has_header: next(reader)
      for row in reader: data_list.append(row)
    return data_list
