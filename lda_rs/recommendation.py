import user_topics
import user_tags
import db_util
import json

def user_sim_matrix():
  topic_matirx = user_topics.get_topic_sim_matrix()
  tag_matrix = user_tags.get_tag_sim_matrix()
  sim_matrix = {}
  for m in topic_matirx:
    if m in tag_matrix:
      sim_matrix[m] = topic_matirx[m]*tag_matrix[m]
  json.dump(sim_matrix,open("matrix/sim_matrix.txt",'w'))
  return sim_matrix

# global_sim_matrix = user_sim_matrix()
def get_sim_matrix(path='matrix/sim_matrix.txt'):
  return json.load(file(path))

def get_user_neighbors(userid,top):
  user_rank = []
  global_sim_matrix = get_sim_matrix()
  for other in db_util.get_user_list():
    if other == userid: break
    key1 = str((userid,other))
    key2 = str((other,userid))
    if key1 in global_sim_matrix:
      user_rank.append([global_sim_matrix[key1],other])
    elif key2 in global_sim_matrix:
      user_rank.append([global_sim_matrix[key1],other])
    else: print "can not find similarity between"+ key1
  user_rank.sort(reverse=True)
  neighbor_list = user_tags.list2hash(movies_count)
  return neighbor_list.keys()[0:top]


def recommend_for_user(userid,top):
  neighbors = get_user_neighbors(userid)
  neighbor_movies = db_util.get_movie_from_users(neighbors)
  movies_count = list_count(neighbor_movies)
  filter_item_for_user(movies_count)
  candidate_list = user_tags.hash2list(movies_count)
  recommend_list = [candidate_list[i][1] for i in range(0,top)]
  return recommend_list


def filter_item_for_user(origin_items,userid):
  for m in origin_items:
      if m in db_util.user_info(userid).user_mv_list:
        origin_items.delete(m)
  return origin_items

def list_count(tuple_list):
  dic = {}
  for t in tuple_list:
    (userid,movieid) = t[:]
    if movieid not in dic: dic.setfault(movieid,1)
    else: dic[movieid] += 1
  return dic

def main():
  user_tags.main()
  user_topics.main()
  user_sim_matrix()
