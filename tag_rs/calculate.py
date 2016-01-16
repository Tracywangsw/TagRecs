import tag_utility
import time
from math import sqrt
from nltk.corpus import wordnet

class Calculate:
  def __init__(self):
    self.tag_util = tag_utility.TagUtility()
    self.user_list = self.tag_util.get_user_list()
    self.movie_list = self.tag_util.get_movie_list()

  # swith to hash table and normalization 
  def switch_list_to_dir(self,sort_list):
    total = sum([item[0] for item in sort_list])
    dir = {}
    if total != 0:
      for i in sort_list:
        (score,item) = i[:]
        dir[item] = score/total
    return dir

  ## need to optimize ##  ## tf-idf? or tf? ##
  def user_top_tags(self,userid,min=10,top=50):
    tag_sort = []
    user_tags_list = self.tag_util.get_user_tags(userid)
    for tag in user_tags_list:
      tag_count = self.tag_util.get_tag_count(tag)
      if tag_count >= min: #tag-movies count >= min
        tag_time_factor = self.cal_time_factor(user_tags_list[tag]['first_ts'],user_tags_list[tag]['last_ts'])
        tag_frequency = float(user_tags_list[tag]['count'])*tag_time_factor
        tag_sort.append([tag_frequency,tag])
    tag_sort.sort()
    tag_sort.reverse()
    return self.switch_list_to_dir(tag_sort[0:top])

  ## need to optimize ## ## how to design time-factor function ##
  def cal_time_factor(self,first,last):
    current = time.time()
    return (current-first)/(current-last)

  # input tag name, return the most similar top n tags
  def tag_top_similar_tags(self,tag,top=20,min=10):
    tag_list = self.tag_util.get_tag_list()
    sim_tag_dir = []
    for t in tag_list:
      if self.tag_util.get_tag_count(t) >= min and t != tag:
        sim_tag_dir.append([self.tag_similarity(tag,t),t])
    sim_tag_dir.sort()
    sim_tag_dir.reverse()
    # top_sim_tag_list = sim_tag_dir[0:top]
    return self.switch_list_to_dir(sim_tag_dir[0:top])

  def cosine_similiarity(self,set1,set2):
    common = self.get_common_items(set1,set2)
    if len(common) == 0: return 0

    sum1 = sum([set1[item] for item in common])
    sum2 = sum([set2[item] for item in common])

    sum1_sq = sum([pow(set1[item],2) for item in common])
    sum2_sq = sum([pow(set2[item],2) for item in common])
    set_sum = sum([set1[item]*set2[item] for item in common])

    rate = float(len(common))/(len(set1)+len(set2)-len(common))
    return float(set_sum*rate)/sqrt(sum1_sq*sum2_sq)

  def syn_similarity(self,tag1,tag2):
    # tag1 = tag1.decode('utf8').encode('ascii')
    # tag2 = tag2.decode('utf8').encode('ascii')
    wordset1 = wordnet.synsets(tag1)
    wordset2 = wordnet.synsets(tag2)
    if wordset1 and wordset2:
      s = wordset1[0].wup_similarity(wordset2[0])
      if s: return s
    return 0

  # input two tag, return the similarity
  ## choose which similiarity method? ##
  def tag_similarity(self,tag1,tag2):
    # print tag1 +"##"+ tag2
    (tag1_movies,tag2_movies) = (self.tag_util.get_tag_movies(tag1),self.tag_util.get_tag_movies(tag2))
    data_similarity = self.cosine_similiarity(tag1_movies,tag2_movies)
    text_similarity = self.syn_similarity(tag1,tag2)
    similiarity = data_similarity + text_similarity
    return similiarity


  # return common movies of the two tags
  def get_common_items(self,set1,set2):
    common = {}
    for item in set1: 
      if item in set2: 
        common[item] = 1
    return common


  # return user-candidate-tags
  def user_candidate_tags(self,user,top=50):
    user_top_tags = self.user_top_tags(user,min=10,top=50) ## adjust parameters
    (candidate_tags,sort_tag) = ({},[])
    for t in user_top_tags: candidate_tags[t] = user_top_tags[t]
    for t in user_top_tags: candidate_tags = self.tag_affinity_recursion(t,user_top_tags,candidate_tags)
    for tag in candidate_tags: sort_tag.append([candidate_tags[tag],tag])
    sort_tag.sort()
    sort_tag.reverse()
    return self.switch_list_to_dir(sort_tag[0:top])

  def tag_affinity_recursion(self,tag,origin_tags,final_tags):
    similar_tags = self.tag_top_similar_tags(tag,top=20,min=10) ## adjust parameters
    for t in similar_tags:
      (sim_score,sim_tag) = (similar_tags[t],t)
      if sim_tag in final_tags: final_tags[sim_tag] += origin_tags[tag]*sim_score
      else: final_tags[sim_tag] = origin_tags[tag]*sim_score
    return final_tags

  # return tag top movies according to movie frequency
  ## how to select movies attached to the given tag? ##
  def tag_top_movies(self,tag,top=20):
    movie_sort = []
    tag_movies = self.tag_util.get_tag_movies(tag)
    total = sum([tag_movies[m] for m in tag_movies])
    for m in tag_movies: movie_sort.append([float(tag_movies[m])/total,m])
    movie_sort.sort()
    movie_sort.reverse()
    return self.switch_list_to_dir(movie_sort[0:top])

  # recommend items attach to the tags for the user
  def user_candidate_movies(self,user):
    (movie_rank,candidate_tags) = ({},self.user_candidate_tags(user,top=50)) ## adjust parameters
    for t in movie_rank: movie_rank[t] = candidate_tags[t]
    for t in candidate_tags: movie_rank = self.movie_affinity_recursion(t,candidate_tags,movie_rank)
    return movie_rank

  def movie_affinity_recursion(self,tag,user_tags,movie_rank):
    ms = self.tag_top_movies(tag,top=50) ## adjust parameters
    for m in ms:
      (movie_score,movieid) = (ms[m],m)
      if movieid in movie_rank: movie_rank[movieid] += movie_score*user_tags[tag]
      else: movie_rank[movieid] = movie_score*user_tags[tag]
    return movie_rank

  def user_recommend_movies(self,user,top=100): ## adjust parameters
    movie_score_map = self.user_candidate_movies(user)
    movie_sort_list = []
    movie_list = []
    user_movies_list = self.tag_util.get_user_movies(user)
    for m in movie_score_map:
      if m not in user_movies_list: movie_sort_list.append([movie_score_map[m],m])
      # movie_sort_list.append([movie_score_map[m],m])
    movie_sort_list.sort()
    movie_sort_list.reverse()
    for m in movie_sort_list[0:top]: movie_list.append(m[1])
    return movie_list


def main():
  t = Calculate()
  s = t.tag_top_similar_tags('romance')
  print t.tag_similarity('romance','virginity')
  print s
