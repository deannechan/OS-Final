import itertools
import numpy as np
from functools import reduce
import heapq
from entity_index import ChannelIndex, Channels

class PotentialMovie:
    
    def __init__(self, movie, score):
        self.movie = movie
        self.score = score
        
    def __cmp__(self, other):
        return cmp(self.score, other.score) 

    def __str__(self):
        return "%s: %f" % (self.movie, self.score)


class Recommender:
    
    graph = None

    def __init__(self, graph):
        self.graph = graph

    def recommend(self, likesModel, moviesModel, user):
        self.likesModel = likesModel
        self.moviesModel = moviesModel
        self.user = user

        (watchedMovies, likedMovies) = likesModel[user]
        allDirs = self.graph.UD[user]
        allActs = self.graph.UA[user]
        allGens = self.graph.UG[user]
        
        #go by actors
        favAct = allActs.argsort()[-30:][::-1]
        favDir = allDirs.argsort()[-30:][::-1]
        favGen = allGens.argsort()[-30:][::-1]
        
        return self.findRecommendedMovies(favDir, favAct, favGen, watchedMovies)  
        
        #while i in range(MAX_LEVEL):
        #    favs = graph.getKHighestAffinityValues(favs)
            
    def findRecommendedMovies(self, favDirs, favActs, favGens, watchedMovies):
        
        movies = []
        count = 0
        
        #level one
        for i in itertools.product(favDirs, favActs, favGens):
            
            score = 0
            score += self.graph.DA[i[0]][i[1]]
            score += self.graph.DG[i[0]][i[2]]
            score += self.graph.AG[i[1]][i[2]]
            
            dMovies = self.moviesModel.dictDirector[i[0]]
            aMovies = self.moviesModel.dictActor[i[1]]
            gMovies = self.moviesModel.dictGenre[i[2]]
            
            # print "dMovies", list(dMovies)
            # print "aMovies", list(aMovies)

            ## potentialMovies = reduce(np.intersect1d, (list(dMovies), list(aMovies)))
            # potentialMovies = np.intersect1d(list(dMovies), list(aMovies))
            # potentialMovies = list(dMovies) + list(aMovies) #+ list(gMovies)

            dgMov = np.intersect1d(list(dMovies), list(gMovies))
            daMov = np.intersect1d(list(dMovies), list(aMovies))
            agMov = np.intersect1d(list(aMovies), list(gMovies))
            potentialMovies = dgMov.tolist() + daMov.tolist() + agMov.tolist()

            potentialMovies = np.setdiff1d(potentialMovies, list(watchedMovies))
            potentialMovies = set(np.setdiff1d(potentialMovies, movies))
            if potentialMovies:
                #print "add potential movie ", potentialMovies#, "-", score
                if(count > 30):
                    heapq.heappushpop(movies, PotentialMovie(potentialMovies.pop(), score).movie)
                else:
                    heapq.heappush(movies, PotentialMovie(potentialMovies.pop(), score).movie)
                    count += 1

            # potentialMovies = np.intersect1d(dMovies, aMovies)
            # potentialMovies = np.setdiff1d(potentialMovies, watchedMovies)
            # for i in potentialMovies:
            #     print "add potential movie ", i
            #     if(count > 10):
            #         heapq.heappushpop(movies, PotentialMovie(i.pop(), score))
            #     else:
            #         heapq.heappush(movies, PotentialMovie(i.pop(), score))
            #         count += 1
        # print movies
        return movies
                
            
            
            
            
            
            
            
                
