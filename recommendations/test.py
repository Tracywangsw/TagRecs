import load_data
import calculate
import random
import item_based

class Test:
  def __init__(self):
    self.test_data = load_data.LoadData().get_test_set()
    self.operator = calculate.Calculate()
    self.item_based = item_based.ItemBased()

  def test_user_movies(self,id):
    user_movies = []
    for r in self.test_data:
      (userid,movieid) = (int(r[1]),int(r[2]))
      if (id == userid) and (movieid not in user_movies): user_movies.append(movieid)
    return user_movies

  def user_hybrid_recommend_movies(self,userid):
    return self.operator.user_recommend_movies(userid)

  def item_based_recommend_movies(self,userid):
    return self.item_based.user_recommend_movies(userid)

  def common_list_len(self,list1,list2):
    common = {}
    for i in list1:
      if i in list2: common[i] = 0
    return len(common)

  def cal_precise(self,recm,testm):
    if len(recm) == 0:
      print 'recommend list is null'
      return 0
    return float(self.common_list_len(recm,testm))/len(recm)

  def cal_recall(self,recm,testm):
    if len(testm) == 0:
      print 'test list is null'
      return 0
    return float(self.common_list_len(recm,testm))/len(testm)

  def cal_f1(self,recm,testm):
    precise = self.cal_precise(recm,testm)
    recall = self.cal_recall(recm,testm)
    average = (precise+recall)/2
    if average == 0: return 0
    return precise*recall/average


  def estimate_hybird_recommend(self):
    user_list = self.operator.user_list
    (total_pre,total_recall,total_f1) = (0,0,0)
    for u in user_list:
      recommend_list = self.user_hybrid_recommend_movies(u)
      test_list = self.test_user_movies(u)
      precision = self.cal_precise(recommend_list,test_list)
      recall = self.cal_recall(recommend_list,test_list)
      f1 = self.cal_f1(recommend_list,test_list)
      print 'userid : ' + str(u)
      print 'precision : ' + str(precision)
      print 'recall : ' + str(recall)
      print 'f1 : ' + str(f1)
      total_pre += precision
      total_recall += recall
      total_f1 += f1
    print 'average precision of hybird recommend method : ' + str(total_pre/len(user_list))
    print 'average recall of hybird recommend method : ' + str(total_recall/len(user_list))
    print 'average f1 of hybird recommend method : ' + str(total_f1/len(user_list))

  def estimate_random_recommend(self):
    user_list = self.operator.user_list
    (total_pre,total_recall,total_f1) = (0,0,0)
    for u in user_list:
      recommend_list = random.sample(self.operator.movie_list,100)
      test_list = self.test_user_movies(u)
      precision = self.cal_precise(recommend_list,test_list)
      recall = self.cal_recall(recommend_list,test_list)
      f1 = self.cal_f1(recommend_list,test_list)
      # print 'userid : ' + str(u)
      # print 'precision : ' + str(precision)
      # print 'recall : ' + str(recall)
      # print 'f1 : ' + str(f1)
      total_pre += precision
      total_recall += recall
      total_f1 += f1
    print 'average precision of random recommend method : ' + str(total_pre/len(user_list))
    print 'average recall of random recommend method : ' + str(total_recall/len(user_list))
    print 'average f1 of random recommend method : ' + str(total_f1/len(user_list))

  def estimate_item_based_recommend(self):
    user_list = self.operator.user_list
    (total_pre,total_recall,total_f1) = (0,0,0)
    for u in user_list:
      recommend_list = self.item_based_recommend_movies(u)
      test_list = self.test_user_movies(u)
      precision = self.cal_precise(recommend_list,test_list)
      recall = self.cal_recall(recommend_list,test_list)
      f1 = self.cal_f1(recommend_list,test_list)
      # print 'userid : ' + str(u)
      # print 'precision : ' + str(precision)
      # print 'recall : ' + str(recall)
      # print 'f1 : ' + str(f1)
      total_pre += precision
      total_recall += recall
      total_f1 += f1
    print 'average precision of item_based recommend method : ' + str(total_pre/len(user_list))
    print 'average recall of item_based recommend method : ' + str(total_recall/len(user_list))
    print 'average f1 of item_based recommend method : ' + str(total_f1/len(user_list))

def main():
  t = Test()
  t.estimate_hybird_recommend()
  t.estimate_item_based_recommend()
  t.estimate_random_recommend()
