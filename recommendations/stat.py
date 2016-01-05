import load_data

class Stat(object):
  """Stat for the dataset of origin, train and test"""
  def __init__(self,whole_path='../dataset/delicious/user_taggedbookmarks-timestamps.dat',train_path='../dataset/outputFile/delicious_train_set.csv',test_path='../dataset/outputFile/delicious_test_set.csv'):
    super(Stat, self).__init__()
    data = load_data.LoadData()
    self.origin_set = data.get_whole_set(whole_path)
    self.train_set = data.get_train_set(train_path)
    self.test_set = data.get_test_set(test_path)
    self.origin_count_stat = self.origin_count_stat()
    self.train_count_stat = self.train_count_stat()
    self.test_count_stat = self.test_count_stat()

  def origin_count_stat(self):
    data = self.origin_set
    (tag_set,user_set,movie_set) = ({},{},{})
    for row in data:
      (userid,movieid,tag) = (int(row[0]),int(row[1]),row[2])
      if tag not in tag_set: tag_set[tag] = 1
      if userid not in user_set: user_set[userid] = 1
      if movieid not in movie_set: movie_set[movieid] = 1
    return {'user':len(user_set),'tag':len(tag_set),'movie':len(movie_set)}

  def train_count_stat(self):
    data = self.train_set
    (tag_set,user_set,movie_set) = ({},{},{})
    for row in data:
      (userid,movieid,tag) = (int(row[1]),int(row[2]),row[3])
      if tag not in tag_set: tag_set[tag] = 1
      if userid not in user_set: user_set[userid] = 1
      if movieid not in movie_set: movie_set[movieid] = 1
    return {'user':len(user_set),'tag':len(tag_set),'movie':len(movie_set)}

  def test_count_stat(self):
    data = self.test_set
    (tag_set,user_set,movie_set) = ({},{},{})
    for row in data:
      (userid,movieid,tag) = (int(row[1]),int(row[2]),row[3])
      if tag not in tag_set: tag_set[tag] = 1
      if userid not in user_set: user_set[userid] = 1
      if movieid not in movie_set: movie_set[movieid] = 1
    return {'user':len(user_set),'tag':len(tag_set),'movie':len(movie_set)}

def main():
  s = Stat()
  print 'origin:'+str(s.origin_count_stat)
  print 'train:'+str(s.train_count_stat)
  print 'test:'+str(s.test_count_stat)