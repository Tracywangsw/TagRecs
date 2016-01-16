import load_data
import csv

class SplitSet:

  def __init__(self):
    self.whole_data = load_data.LoadData().get_whole_set()
    self.set = self.set_whole_dataset(self.whole_data)

  # return hashmap {userid:[record]}
  def set_whole_dataset(self,data):
    fullset = {}
    for row in data:
      (userid,movieid,tag,ts) = (int(row[0]),int(row[1]),row[2],int(row[3]))
      if userid in fullset: fullset[userid].append([ts,userid,movieid,tag])
      else: fullset.setdefault(userid,[[ts,userid,movieid,tag]])
    return fullset

  # return data of single user
  def user_data(self,user):
    userset = self.set[user]
    userset.sort()
    return userset

  def get_user_sum(self,user):
    userset = self.set[user]
    (usertag,usermovie) = ({},{})
    for u in userset:
      (movieid,tag) = (u[2],u[3])
      if movieid not in usermovie:
        usermovie[movieid] = 1
      if tag not in usertag:
        usertag[tag] = 1
    return [len(usertag),len(usermovie)]

  def split(self,tagmin=15,moviemin=50):
    (trainset,testset,fullset) = ([],[],self.set)
    for u in fullset:
      userdata = self.user_data(u)
      addedsum = 0
      (tag_sum,movie_sum) = self.get_user_sum(u)[:]
      if movie_sum>=moviemin and tag_sum>=tagmin:
        for ru in userdata:
          if float(addedsum)/len(userdata) <= 0.8:
            trainset.append(ru)
            addedsum += 1
          else: testset.append(ru)
    return [trainset,testset]


def main():
  s = SplitSet()
  (trainset,testset) = s.split()[:]
  print 'begin to write trainset\n'
  write_file(trainset,'../dataset/outputFile/tag_train_after_cleaning.csv')
  print 'trainset writing end\n'
  print 'begin to write testset\n'
  write_file(testset,'../dataset/outputFile/tag_test_after_cleaning.csv')
  print 'testset writing end'

def write_file(recordlist,path):
  with open(path,'w') as f:
    a = csv.writer(f,delimiter=',')
    a.writerows(recordlist)
