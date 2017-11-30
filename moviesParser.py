import json
import pickle
import time
from entity_index import ChannelIndex, Channels

MOVIES_PICKLE_FILE = 'movies.model'

'''
        {director : [movieID]}
        {actor : [movieID]}
        {genre : [movieID]}
        {movieID: movieObject{"rating": str, 
                                "movie_id": "60141", 
                                "name": str, 
                                "director": str, 
                                "actors": [], 
                                "genre": str
                            }}
'''
class MoviesParser:

    def __init__(self, indexProvider):
        self.dictDirector = {} # {director : [movieID]}
        self.dictActor = {} # {actor : [movieID]}
        self.dictGenre = {} # {genre : [movieID]}
        self.movies = {} # movieID: movieObject
        self._indexProvider = indexProvider

    def returnMovieID(self, movieObject):
        ret = self._indexProvider.getEntityIndex(Channels.MOVIE, movieObject['movie_id'])
        return ret

    #method that checks if ID of dict contains directors: if not, create one dict with dir as ID and movieID as value                                
    def updateDictOfDirectors(self, movieObject):
        director = movieObject['director']
        if director:
            director = self._indexProvider.getEntityIndex(Channels.DIRECTOR, director)
            if director not in self.dictDirector:
                self.dictDirector[director] = set()
            self.dictDirector[director].add(self.returnMovieID(movieObject))
        
    #method that checks if ID of dict contains actors: if not, create one dict with actor as ID and set of movieIDs as value    
    def updateDictOfActors(self, movieObject):
        listOfActors = movieObject['actors']
        for actor in listOfActors:
            if actor:
                actor = self._indexProvider.getEntityIndex(Channels.ACTOR, actor)
                if actor not in self.dictActor:
                    self.dictActor[actor] = set()
                self.dictActor[actor].add(self.returnMovieID(movieObject))
        
    #method that checks if ID of dict contains genres: if not, create one dict with genre as ID and set of movieIDs as value        
    def updateDictOfGeneres(self, movieObject):
        genre = movieObject['genre']
        if genre:
            genre = self._indexProvider.getEntityIndex(Channels.GENRE, genre)
            if genre not in self.dictGenre:
                self.dictGenre[genre] = set()  
            self.dictGenre[genre].add(self.returnMovieID(movieObject))

    def parseMoviesObjects(self, filename,  parse = True):
        start_time = time.time()
        if parse:
            json_data =  open(filename, 'r').read() 
            jsonData = json.loads(json_data) 
                                  
            for movieObject in jsonData: 
                if self.returnMovieID(movieObject):
                    self.movies[self.returnMovieID(movieObject)] = movieObject
                    self.updateDictOfDirectors(movieObject)
                    self.updateDictOfActors(movieObject)
                    self.updateDictOfGeneres(movieObject)
                    # print(movieObject['name'])
            print("Parsed movies.json in %f seconds" % (time.time() - start_time))
            s = pickle.dumps(self)
            with open(MOVIES_PICKLE_FILE, 'w') as f:
                f.write(s)
        else:
            with open(MOVIES_PICKLE_FILE, 'r') as f:
                s = f.read()
                mov = pickle.loads(s)
                self.dictActor = mov.dictActor
                self.dictDirector = mov.dictDirector
                self.dictGenre = mov.dictDirector
            print("Loaded pickled movies model in %f seconds" % (time.time() - start_time))
        return self

#main function to parse a json file of movies:
def main(moviesJson):  
    channelIndex = ChannelIndex(Channels.CHANNELS)
    mov = MoviesParser(channelIndex)
    mov.parseMoviesObjects(moviesJson, parse = True)
    print(len(mov.dictActor))
    print(len(mov.dictDirector))
    print(len(mov.dictGenre))

if __name__ == "__main__":
    moviesJson = 'json/movies.json'
    main(moviesJson)
