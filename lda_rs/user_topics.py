import lda
import db
import datetime
import numpy as np
import scipy.stats as stats
import multiprocessing as mp
import math
import pdb
import json

# lda_loaded_model = lda.load_lda('model/50_topics_lda.txt')
db_info = db.info()

def movieid_plot_map(return_list):
  mv_plot = {}
  for r in return_list:
    # (mvid,plot) = r[:]
    (mvid,plot) = (r,return_list[r])
    if plot:
      if type(plot) is tuple:
        plot_str = ''
        for p in plot:
          if p: plot_str += p
        mv_plot[mvid] = plot_str
      else: mv_plot[mvid] = plot
    else: print "##!!!"
  return mv_plot

plot_map = movieid_plot_map(db_info.mv_plots_set)

def item_lda_model(num_topics=500,path='model/whole_movie_lda.txt'):
  print 'load plots start,datetime:'+ str(datetime.datetime.now())
  # all_plots = db_util.get_all_plots()
  print 'load plots end,datetime:'+ str(datetime.datetime.now())
  # plot_map = movieid_plot_map(all_plots)
  whole_doc = plot_map.values()
  lda_model = lda.lda_model_build(whole_doc,num_topics)
  lda_model.save(path)
  return lda_model

def get_plot_doc(return_list):
  str_list = []
  for r in return_list:
    if type(r) is tuple:
      plot_str = ''
      for p in r:
        if p: plot_str += p
      str_list.append(plot_str)
    else: str_list.append(r)
  return str_list

def user_movie_plots(mvlist,plot_set=plot_map):
  user_plots = []
  for m in mvlist:
    if m in plot_set: user_plots.append(plot_set[m])
    else: print str(m)+" has no plot"
  return user_plots

def user_topics(userid,model):
  movie_list = db_info.user_train_movies(userid)
  plot_list = user_movie_plots(movie_list)
  user_doc = get_plot_doc(plot_list)
  topic_dis = lda.doc_topic_distribution(model,user_doc)
  return topic_dis

def user_topic_dic(model=lda.load_lda('model/100_topics_lda.txt')):
  topic_dic = {}
  for u in db_info.user_list:
    topic_dic[u] = user_topics(u,model)
  return topic_dic

# user_topic_map = user_topic_dic()

def topic_sim(topic_a,topic_b):
  kl = kl_divergence(topic_a,topic_b)
  return math.exp(-1*kl)

def kl_divergence(p,q):
  return np.sum([stats.entropy(p,q),stats.entropy(q,p)])

def topic_sim_matrix(model,person,other):
  sim_matrix = {}
  # topic_person = user_topics(person,model)
  # topic_other = user_topics(other,model)
  topic_person = user_topic_map[person]
  topic_other = user_topic_map[other]
  sim_matrix[str((person,other))] = topic_sim(topic_person,topic_other)
  print sim_matrix
  return sim_matrix

def get_topic_sim_matrix(path="matrix/50_topics_sim_matrix.txt"):
  return json.load(file(path))

def multiprocess(processes, model, user_list_list):
  pool = mp.Pool(processes=processes)
  results = [pool.apply_async(topic_sim_matrix, args=(model,l[0],l[1])) for l in user_list_list]
  dest = dict(results[0].get())
  for r in range(1,len(results)):
    dest.update(results[r].get())
  return dest

def split_item(item,n=8):
  l = len(item)
  item_list = []
  item_list.append(item[0:l/n])
  for i in range(1,n):
    s = i*l/n
    item_list.append(item[s:(i+1)*l/n])
  return item_list

def save_lda():
  item_lda_model(num_topics=100,path='model/100_topics_lda.txt')

def main(processes = 8):
  lda_loaded_model = lda.load_lda('model/100_topics_lda.txt')
  user_list = db_info.user_list
  user_list_list = db.split_item(user_list)
  results = multiprocess(processes,lda_loaded_model,user_list_list)
  json.dump(results,open("matrix/100_topics_sim_matrix.txt",'w'))
  # topic_sim_matrix(lda_loaded_model)
  # item_lda_model(num_topics=50,path='model/50_topics_lda.txt')