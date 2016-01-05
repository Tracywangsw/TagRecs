import db_util
from math import sqrt


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

class user_sim():
  def __init__(self,userid):
    self.user_tags = generate_tag(userid).user_tags()
    self.user_list = db_util.get_user_list()

  def user_sim(self):
    user_sim_matrix = {}
    for u in self.user_list:
      u_tags = generate_tag(u).user_tags()
      user_sim_matrix[u] = cosine_sim(self.user_tags,u_tags)
      print cosine_sim(self.user_tags,u_tags)
    return user_sim_matrix


def main(id):
  # g = generate_tag(id)
  # print g.user_tags()
  u = user_sim(id)
  u.user_sim()

