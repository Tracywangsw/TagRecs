import lda
import db_util
import datetime
from imdb import IMDb


class generate_topic():
  def __init__(self,userid):
    imdb_list = db_util.user_info(userid).user_imdb_list
    doc_set = self.get_movie_plot(imdb_list)
    self.lda_model = lda.lda_model_build(doc_set,num_topics=50)


  def get_movie_plot(self,id_list):
    plot_list = []
    plot_str = ''
    print 'get_movie_plot start,datetime:'+ str(datetime.datetime.now())
    for id in id_list:
      movie = IMDb().get_movie(id)
      plot = movie.get('plot')
      # if type(plot) == 'list' and plot:
      #   plot_str = ' '.join(plot)
      for p in plot: plot_str += p
      plot_list.append(plot_str)
    print 'get_movie_plot end,datetime:'+ str(datetime.datetime.now())
    return plot_list

  def user_topics(self):
    topics = self.lda_model.show_topics(num_topics=50,num_words=20)
    return topics

def main():
  print 'estimate start,datetime:'+ str(datetime.datetime.now())
  g = generate_topic(80)
  print g.lda_model.show_topics(num_topics=50,num_words=20)
  print 'estimate end,datetime:'+ str(datetime.datetime.now())


