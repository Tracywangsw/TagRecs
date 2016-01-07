from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim
import datetime

class corpora_build():
  def __init__(self,doc_set):
    doc = self.clean_doc(doc_set)
    self.dictionary = corpora.Dictionary(doc)
    self.corpora = [self.dictionary.doc2bow(text) for text in doc]

  def clean_doc(self,doc_set):
    tokenizer = RegexpTokenizer(r'\w+')
    en_stop = get_stop_words('en')
    en_stop += ['t','s','u','can','d','ve','isn','didn','wouldn','don','shouldn','haven','hadn','doesn','couldn']
    p_stemmer = PorterStemmer()
    texts = []
    for i in doc_set:
      raw = i.lower()
      tokens = tokenizer.tokenize(raw)
      stopped_tokens = [i for i in tokens if not i in en_stop]
      stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]
      texts.append(stemmed_tokens)
    return texts

def lda_model_build(doc_set,num_topics):
  print 'lda_model_build start,datetime:'+ str(datetime.datetime.now())
  util = corpora_build(doc_set)
  ldamodel = gensim.models.ldamodel.LdaModel(util.corpora, num_topics, id2word = util.dictionary, passes=20, minimum_probability=0)
  print 'lda_model_build end,datetime:'+ str(datetime.datetime.now())
  return ldamodel


def doc_topic_distribution(lda,doc):
  texts = corpora_build(doc)
  test = lda[texts.corpora][0]
  # a = list(sorted(test, key=lambda x: x[1], reverse=True)) #rank distribution
  # print lda.print_topic(a[-1][0]) # the least relative
  # print lda.print_topic(a[0][0]) # the most relative
  return test

def load_lda(path='../lda.txt'):
  return gensim.models.ldamodel.LdaModel.load(path,mmap='r')

def main():
  doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
  doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
  doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
  doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
  doc_e = "Health professionals say that brocolli is good for your health." 
  doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]
  lda = lda_model_build(doc_set,num_topics=20)
  # lda.save('../lda.txt')
  # lda = load_lda()
  test_doc = ["My mother likes to eat good brocolli. "]
  print doc_topic_distribution(lda,test_doc)
  # print lda.show_topics()
