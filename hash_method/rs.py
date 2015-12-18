import tagUtil
import movieUtil
# import ratingUtil

class rs:

  def __init__(self):
    self.moviemap = movieUtil.movieUtil()
    self.tagutil = tagUtil.tagUtil()


  # return user-candidate-tags
  def getCandidateTags(self,user,top=50):
    (finaltags,usertags,sorttag) = ({},{},[])
    for t in self.tagutil.userTopTags(user,top=50): usertags[t[1]] = t[0]
    for t in usertags: finaltags[t] = usertags[t]
    for t in usertags: finaltags = self.tagAffinityRecursion(t,usertags,finaltags)

    for tag in finaltags: sorttag.append([finaltags[tag],tag])
    sorttag.sort()
    sorttag.reverse()
    return sorttag[0:top]

  def tagAffinityRecursion(self,tag,usertags,finaltags):
    for t in self.tagutil.tagTopSimilarTags(tag,top=10):
      (simscore,simtag) = t[:]
      if simtag in finaltags: finaltags[simtag] += usertags[tag]*simscore
      else: finaltags[simtag] = usertags[tag]*simscore
    return finaltags


  # recommend items attach to the tags for the user
  def getCandidateMovies(self,user):
    (movierank,usertags,tags) = ({},{},self.getCandidateTags(user))
    for t in tags: usertags[t[1]] = t[0]
    for t in tags: movierank = self.movieAffinityRecursion(t[1],movierank,usertags)
    return movierank

  def movieAffinityRecursion(self,tag,movierank,usertags):
    ms = self.tagutil.tagTopMovies(tag,top=50)
    for m in ms:
      (moviescore,movieid) = m[:]
      if movieid in movierank: movierank[movieid] += moviescore*usertags[tag]
      else: movierank[movieid] = moviescore*usertags[tag]
    return movierank


  # final recommendations for user
  def getRecommendMovies(self,user,top=30):
    # moviemap = movieUtil.movieUtil()
    movies = self.getCandidateMovies(user)
    bingo = 0
    (rankmovies,usermovies) = ([],self.tagutil.userMovies(user))
    for m in movies:
      if m not in usermovies: rankmovies.append([movies[m],self.moviemap.getMovieById(m)])
      else: bingo += 1
    rankmovies.sort()
    rankmovies.reverse()
    print "count of bingo: " + str(bingo)
    return [rankmovies[0:top],bingo]

def main(user):
  res = rs()
  print res.getRecommendMovies(user)[0]