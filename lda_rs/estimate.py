import db
import recommendation
import json

db_info = db.info()

def common_list_len(list1,list2):
  common = {}
  for i in list1:
    if i in list2: common[i] = 0
  return len(common)

def cal_precise(recm,testm):
  if len(recm) == 0:
    print 'recommend list is null'
    return 0
  return float(common_list_len(recm,testm))/len(recm)

def cal_recall(recm,testm):
  if len(testm) == 0:
    print 'test list is null'
    return 0
  return float(common_list_len(recm,testm))/len(testm)

def cal_f1(recm,testm):
  precise = cal_precise(recm,testm)
  recall = cal_recall(recm,testm)
  average = (precise+recall)/2
  if average == 0: return 0
  return precise*recall/average

def estimate_recommender():
  estimate_json = {}
  user_list = db_info.user_list
  (total_pre,total_recall,total_f1) = (0,0,0)
  for u in user_list:
    recommend_list = recommendation.recommend_for_user(u,100,30)
    test_list = db_info.user_test_movies(u)
    precision = cal_precise(recommend_list,test_list)
    recall = cal_recall(recommend_list,test_list)
    f1 = cal_f1(recommend_list,test_list)
    print 'userid : ' + str(u)
    print 'precision : ' + str(precision)
    print 'recall : ' + str(recall)
    print 'f1 : ' + str(f1)
    total_pre += precision
    total_recall += recall
    total_f1 += f1

    u_str = str(u)
    precision_str = str(precision)
    recall_str = str(recall)
    f1_str = str(f1)
    estimate_json[u_str] = {}
    estimate_json[u_str]['precision'] = precision_str
    estimate_json[u_str]['recall'] = recall_str
    estimate_json[u_str]['f1'] = f1_str
  json.dump(estimate_json,open("result/result.txt",'w'))
  print 'average precision of hybird recommend method : ' + str(total_pre/len(user_list))
  print 'average recall of hybird recommend method : ' + str(total_recall/len(user_list))
  print 'average f1 of hybird recommend method : ' + str(total_f1/len(user_list))

def main():
  estimate_recommender()