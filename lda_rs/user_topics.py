import lda
import db_util
import datetime
import numpy as np
import scipy.stats as stats
import math
import pdb
import json

# lda_loaded_model = lda.load_lda('model/50_topics_lda.txt')

def movieid_plot_map(return_list):
  mv_plot = {}
  for r in return_list:
    (mvid,plot) = r[:]
    if plot:
      if type(plot) is tuple:
        plot_str = ''
        for p in plot:
          if p: plot_str += p
        mv_plot[mvid] = plot_str
      else: mv_plot[mvid] = plot
    else: print "##!!!"
  return mv_plot

plot_map = movieid_plot_map(db_util.get_all_plots())

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
  movie_list = db_util.user_info(userid).user_mv_list
  plot_list = user_movie_plots(movie_list)
  user_doc = get_plot_doc(plot_list)
  return lda.doc_topic_distribution(model,user_doc)

def topic_sim(topic_a,topic_b):
  kl = kl_divergence(topic_a,topic_b)
  return math.exp(-1*kl)

def kl_divergence(p,q):
  return np.sum([stats.entropy(p,q),stats.entropy(q,p)])

# def topic_fill(topic,len):

def topic_sim_matrix(model):
  user_list = db_util.get_user_list()
  sim_matrix = {}
  for i in range(0,len(user_list)):
    person = user_list[i]
    topic_person = user_topics(person,model)
    for j in range(i+1,len(user_list)):
      other = user_list[j]
      topic_other = user_topics(other,model)
      print str(person) + " ## " + str(other)
      key = (person,other)
      sim_matrix[str(key)] = topic_sim(topic_person,topic_other)
      print sim_matrix[str(key)]
  json.dump(sim_matrix,open("matrix/50_topics_sim_matrix.txt",'w'))
  return sim_matrix

def get_topic_sim_matrix(path="matrix/50_topics_sim_matrix.txt"):
  return json.load(file(path))


def main():
  lda_loaded_model = lda.load_lda('model/50_topics_lda.txt')
  topic_sim_matrix(lda_loaded_model)
  # item_lda_model(num_topics=50,path='model/50_topics_lda.txt')