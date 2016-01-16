import db
import user_tags
import json
from math import sqrt
import multiprocessing as mp

db_info = db.info()

def common_sim(set1,set2):
  common = user_tags.get_common_items(set1,set2)
  if len(common) == 0: return 0
  rate = float(len(common))/(len(set1)+len(set2)-len(common))
  return rate

def sim_matrix(person,other):
  sim = {}
  person_items = db_info.user_train_movies(person)
  other_items = db_info.user_train_movies(other)
  sim[str((person,other))] = common_sim(person_items,other_items)
  return sim

def multiprocess(processes, user_list_list):
  pool = mp.Pool(processes=processes)
  results = [pool.apply_async(sim_matrix, args=(l[0],l[1])) for l in user_list_list]
  # results = [p.get() for p in results]
  dest = dict(results[0].get())
  for r in range(1,len(results)):
    dest.update(results[r].get())
  return dest

def main(processes = 8):
  user_list = db_info.user_list
  user_list_list = db.split_item(user_list)
  results = multiprocess(processes,user_list_list)
  json.dump(results,open("matrix/user_items_sim_matrix.txt",'w'))

def get_user_items_sim_matrix(path='matrix/user_items_sim_matrix.txt'):
  return json.load(file(path))