import json
import pickle
import time
from entity_index import ChannelIndex, Channels

PICKLE_FILE = 'likes.model'

class UserMovieRel:

    def __init__(self, userId, movieId, rating):
        self._movie = movieId
        self._user = userId
        self._rating = float(rating)

    @property
    def user(self):
        return self._user
    
    @property
    def movie(self):
        return self._movie
    
    @property
    def rating(self):
        return self._rating

'''
    userID: [UserMovieRel(userID, movieID, rating)]
'''
class LikesParser:

    def __init__(self, indexProvider, likeThreshold = 3):
        self._likeThreshold = likeThreshold
        self._model = None # userID: ([watched movieID], [liked movieID])
        self._userMoviesDict = None # userID: [movieObject]
        self._indexProvider = indexProvider

    @property
    def model(self):
        # print "likesparser.model",self._model
        return self._model
    
    @property
    def userMoviesDict(self):
        return self._userMoviesDict

    def _parseFileMod(self, filepath, count = None):
        maxRating = 0
        with open(filepath, 'r') as f:
            fileStr = f.read()
            fileJsonArr = json.loads(fileStr)
            idx = 0
            for jsonObj in fileJsonArr:
                # print "jsonObj", jsonObj
                userMovieRel = UserMovieRel(self._indexProvider.getEntityIndex(Channels.USER, jsonObj['userID']), 
                    self._indexProvider.getEntityIndex(Channels.MOVIE, jsonObj['movieID']), 
                    jsonObj['rating'])
        
                if userMovieRel.rating > maxRating:
                    maxRating = userMovieRel.rating
                yield userMovieRel
                idx += 1
                if count:
                    if idx >= count:
                        break
            print("Parsed %d likes" % idx)
            print("MaxRating: %f" % maxRating)
    
    def _parseFile(self, filepath, count = None):
        with open(filepath, 'r') as f:
            fileStr = f.read()
            fileJsonArr = json.loads(fileStr)
            idx = 0
            for jsonObj in fileJsonArr:
                userMovieRel = UserMovieRel(self._indexProvider.getEntityIndex(Channels.USER, jsonObj['userID']), 
                    self._indexProvider.getEntityIndex(Channels.MOVIE, jsonObj['movieID']), 
                    jsonObj['rating'])
                                
                yield userMovieRel
                idx += 1
                if count:
                    if idx >= count:
                        break
            print("Parsed %d likes" % idx)


    def _buildUserMoviesDict(self, filepath, count = None):
        retDict = {}
        for userMovieRel in self._parseFileMod(filepath, count):
            if userMovieRel.user != None:
                if userMovieRel.user not in retDict:
                    retDict[userMovieRel.user] = []
                retDict[userMovieRel.user].append(userMovieRel)
        
        return retDict

    def _buildUserLikesTupleDict(self, userMoviesDict):
        for user, moviesList in userMoviesDict.items():
            watchedSet = set()
            likedSet = set()
            for userMovieRel in moviesList:
                if userMovieRel.rating >= self._likeThreshold:
                    likedSet.add(userMovieRel.movie)
                watchedSet.add(userMovieRel.movie)
            yield (user, watchedSet, likedSet)

    def getUserDict(self, filepath, build = False, count = None):
        startTime = time.time()
        if not build:
            with open(PICKLE_FILE, 'r') as f:
                s = f.read()
                self._model = pickle.loads(s)
            print("Model loaded from pickle in %f seconds" % (time.time() - startTime))
        else:
            self._model = {}
            self._userMoviesDict = self._buildUserMoviesDict(filepath, count)
            # print(userMoviesDict)
            for (user, watchedSet, likedSet) in self._buildUserLikesTupleDict(self._userMoviesDict):
                self._model[user] = (watchedSet, likedSet)
            print("Parser completed in %f seconds" % (time.time() - startTime))
            s = pickle.dumps(self._model)
            with open(PICKLE_FILE, 'w') as f:
                f.write(s)
        return self._model

def main():
    filepath = 'json/likes.json'
    channelIndex = ChannelIndex(Channels.CHANNELS)
    parser = LikesParser(channelIndex, 3)
    userDict = parser.getUserDict(filepath, build = True, count = None)
    likeProbs = []
    for user, items in userDict.items():
        print("%s: %d->%d" % (user, len(items[0]), len(items[1])))
        likeProbs.append(len(items[1]) / float(len(items[0])))
    print("Average Like prob: %f" % (sum(likeProbs) /float(len(likeProbs))))
if __name__ == "__main__":
    main()
