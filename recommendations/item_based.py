import tag_utility
import calculate

class ItemBased:
  def __init__(self):
    self.tag_util = tag_utility.TagUtility()
    self.operator = calculate.Calculate()
    self.user_list = self.tag_util.get_user_list()
    self.movie_list = self.tag_util.get_movie_list()

  def user_movies(self,user):
    return self.tag_util.get_user_movies(user)


  def movie_similarity(self,m1,m2):
    m1_tags = self.tag_util.get_movie_tags(m1)
    m2_tags = self.tag_util.get_movie_tags(m2)
    return self.operator.cosine_similiarity(m1_tags,m2_tags)

  def user_top_movies(self,user):
    sim_movies = []
    user_movies = self.user_movies(user)
    for m in self.movie_list:
      if m not in user_movies:
        sim_sum = sum([self.movie_similarity(m,user_m) for user_m in user_movies])
        sim_movies.append([sim_sum,m])
    sim_movies.sort()
    sim_movies.reverse()
    return sim_movies

  def user_recommend_movies(self,user,top=100):
    recommend_list = []
    candidate_movies = self.user_top_movies(user)[0:top]
    for m in candidate_movies:
      (score,item) = m[:]
      if m not in recommend_list: recommend_list.append(item)
    return recommend_list

def main():
  i = ItemBased()
  print i.user_recommend_movies(29)