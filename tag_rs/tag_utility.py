import load_data

class TagUtility:

  def __init__(self):
    self.train_set = load_data.LoadData().get_train_set()
    self.list = self.set_list()
    self.tag_count = self.set_tag_count()
    self.user_tags = self.set_user_tags()
    self.tag_movies = self.set_tag_movies()
    self.user_movies = self.set_user_movies()
    self.movie_tags = self.set_movie_tags()

  # return user_list, movie_list, tag_list
  def set_list(self):
    (user_list,movie_list,tag_list) = ({},{},{})
    for r in self.train_set:
      (userid,movieid,tag) = (int(r[1]),int(r[2]),r[3])
      if userid not in user_list: user_list[userid] = 1
      if movieid not in movie_list: movie_list[movieid] = 2
      if tag not in tag_list: tag_list[tag] = 3
    return {'user':user_list,'movie':movie_list,'tag':tag_list}

  def get_user_list(self):
    return self.list['user']

  def get_movie_list(self):
    return self.list['movie']

  def get_tag_list(self):
    return self.list['tag']

  # return the whole tag_count hashmap in the set
  def set_tag_count(self):
    tag_info = {}
    for r in self.train_set:
      tag = r[3]
      if tag in tag_info: tag_info[tag] += 1
      else: tag_info.setdefault(tag,1)
    return tag_info

  # return the given tag count 
  def get_tag_count(self,tag):
    return self.tag_count[tag]


  # tag_movies
  def set_tag_movies(self):
    tag_movies = {}
    for r in self.train_set:
      (movieid,tag) = (int(r[2]),r[3])
      if tag in tag_movies:
        if movieid in tag_movies[tag]: tag_movies[tag][movieid] += 1
        else: tag_movies[tag][movieid] = 1
      else: tag_movies.setdefault(tag,{movieid:1})
    return tag_movies

  def get_tag_movies(self,tag):
    return self.tag_movies[tag]


  # user_tags
  def set_user_tags(self):
    user_tags = {}
    for r in self.train_set:
      (userid,tag,ts) = (int(r[1]),r[3],int(r[0]))
      if userid in user_tags:
        if tag in user_tags[userid]:
          user_tags[userid][tag]['count'] += 1
          if ts<user_tags[userid][tag]['first_ts']: user_tags[userid][tag]['first_ts'] = ts
          if ts>user_tags[userid][tag]['last_ts']: user_tags[userid][tag]['last_ts'] = ts
        else: user_tags[userid].setdefault(tag,{'count':1,'first_ts':ts,'last_ts':ts})
      else: user_tags.setdefault(userid,{tag:{'count':1,'first_ts':ts,'last_ts':ts}})
    return user_tags

  def get_user_tags(self,userid):
    return self.user_tags[userid]


  # user_movies
  def set_user_movies(self):
    user_movies = {}
    for r in self.train_set:
      (userid,movieid) = (int(r[1]),int(r[2]))
      if userid in user_movies:
        if movieid in user_movies[userid]: user_movies[userid][movieid] += 1
        else: user_movies[userid].setdefault(movieid,1)
      else: user_movies.setdefault(userid,{movieid:1})
    return user_movies

  def get_user_movies(self,userid):
    return self.user_movies[userid]

  def set_movie_tags(self):
    movie_tags = {}
    for r in self.train_set:
      (movieid,tag) = (int(r[2]),r[3])
      if movieid in movie_tags:
        if tag in movie_tags[movieid]: movie_tags[movieid][tag] += 1
        else: movie_tags[movieid].setdefault(tag,1)
      else: movie_tags.setdefault(movieid,{tag:1})
    return movie_tags

  def get_movie_tags(self,movieid):
    return self.movie_tags[movieid]

def main():
  t = Calculate()
  s = t.tag_top_movies('romance')
  print t.tag_util.get_tag_movies('romance')[4973]