from likes_parser import LikesParser
from moviesParser import MoviesParser
from graph import Graph
from entity_index import ChannelIndex, Channels
from recommend import Recommender, PotentialMovie

def creatingTrainingData(likesMap):
    #print likesMap
    print "Exit"


moviesParser = None
likesMap = None

def main(likesJson, moviesJson):
    global moviesParser
    global likesMap
    channelIndex = ChannelIndex(Channels.CHANNELS)
    likesParser = LikesParser(channelIndex, likeThreshold=3) #out of 5
    likesMap = likesParser.getUserDict(likesJson, build = True, count = None)
    
    creatingTrainingData(likesMap)
    
    moviesParser = MoviesParser(channelIndex)
    moviesParser.parseMoviesObjects(moviesJson, parse = True)

    userCount = len(likesMap)
    actorsCount = len(moviesParser.dictActor)
    directorsCount = len(moviesParser.dictDirector)
    genreCount = len(moviesParser.dictGenre)
    print "userCount-", userCount, ";actorsCount-", actorsCount, ";directorsCount-", directorsCount, ";genreCount-", genreCount
    # print("%d,%d,%d,%d" % (userCount, actorsCount, directorsCount, genreCount))
    graph = Graph(userCount, actorsCount, directorsCount, genreCount)
    print "likesMap", likesMap[3]
    graph.calculateUserAffinity(moviesParser.dictDirector, moviesParser.dictActor, moviesParser.dictGenre, likesMap)
    graph.calculateAffinityBetweenEntities()
    graph.calculateSelfAffinity()

    reco = Recommender(graph)
    movies = reco.recommend(likesParser.model, moviesParser, 3)
    print("Recommendations: ")
    for m in movies:
        movieObj = moviesParser.movies[m]
        movieName = movieObj['name']
        print "ID:", m, "-", movieName
        # print(movieName)

if __name__ == "__main__":
    main('json/likes.json', 'json/movies.json')