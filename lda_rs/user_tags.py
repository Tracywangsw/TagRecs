import db_util
from math import sqrt
import multiprocessing as mp
import json


def hash2list(map):
  sort_tag = []
  for tag in map: sort_tag.append([map[tag],tag])
  sort_tag.sort()
  sort_tag.reverse()
  return sort_tag

def list2hash(list):
  hashmap = {}
  for l in list:
    (count,item) = l[:]
    hashmap[item] = count
  return hashmap

class generate_tag():
  def __init__(self,userid):
    self.mv_list = db_util.user_info(userid).user_mv_list

  def mv_top_tags(self,mvid,top=10):
    tag_list = db_util.get_mv_tags(mvid)
    hash_tag = {}
    tags = []
    count = 0

    for t in tag_list:
      tag = t[0]
      if tag not in hash_tag: hash_tag.setdefault(tag,1)
      else: hash_tag[tag] += 1

    sort_tag = hash2list(hash_tag)
    for t in sort_tag: 
      if count >= top: break
      tags.append(t[1])
      count += 1

    return tags

  def user_tags(self,top=50):
    tag_count = {}
    for m in self.mv_list:
      for t in self.mv_top_tags(m):
        if t not in tag_count: tag_count.setdefault(t,1)
        else: tag_count[t] += 1
    return list2hash(hash2list(tag_count)[0:top])

def get_common_items(set1,set2):
  common = {}
  for item in set1: 
    if item in set2: 
      common[item] = 1
  return common

def cosine_sim(set1,set2):
  common = get_common_items(set1,set2)
  if len(common) == 0: return 0

  sum1 = sum([set1[item] for item in common])
  sum2 = sum([set2[item] for item in common])

  sum1_sq = sum([pow(set1[item],2) for item in common])
  sum2_sq = sum([pow(set2[item],2) for item in common])
  set_sum = sum([set1[item]*set2[item] for item in common])

  rate = float(len(common))/(len(set1)+len(set2)-len(common))
  return float(set_sum*rate)/sqrt(sum1_sq*sum2_sq)


def tag_sim_matrix(user_list):
  # user_list = db_util.get_user_list()
  sim_matrix = {}
  for i in range(0,len(user_list)):
    person = user_list[i]
    person_tags = generate_tag(person).user_tags()
    for j in range(i+1,len(user_list)):
      other = user_list[j]
      other_tags = generate_tag(other).user_tags()
      sim_matrix[str((person,other))] = cosine_sim(person_tags,other_tags)
      print sim_matrix[str((person,other))]
  # json.dump(sim_matrix,open("matrix/tags_sim_matrix.txt",'w'))
  return sim_matrix

def get_tag_sim_matrix(path='matrix/tags_sim_matrix.txt'):
  return json.load(file(path))

def multiprocess(processes, user_list_list):
  pool = mp.Pool(processes=processes)
  results = [pool.apply_async(tag_sim_matrix, args=(l,)) for l in user_list_list]
  results = [p.get() for p in results]
  dest = dict(results[0].get())
  for r in range(1,len(results)):
    data = r.get()
    dest.update(data)
  return dest

def split_item(item,n=8):
  l = len(item)
  item_list = []
  item_list.append(item[0:l/n])
  for i in range(1,n):
    s = i*l/n
    item_list.append(item[s:(i+1)*l/n])
  return item_list


def main():
  processes = 20
  user_list = db_util.get_user_list()
  user_list_list = split_item(user_list,n=processes)
  results = multiprocess(processes,user_list_list)
  json.dump(sim_matrix,open("matrix/tags_sim_matrix.txt",'w'))