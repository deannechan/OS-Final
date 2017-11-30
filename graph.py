import numpy as np
import gc
import h5py

class Graph:
    
    def __init__(self, usersCount, actorsCount, directorsCount, genreCount):
        #Storing weights as matrix
        self.usersCount = usersCount
        self.actorsCount = actorsCount
        self.directorsCount = directorsCount
        self.genreCount = genreCount
         
    """
    all lists are represented as sets
    
    dirMap = {dir -> list of movies}
    actorMap = similar
    genreMap = similar
    
    likesMap = {user -> ([all movies], [liked movies])}
    
    """
    def calculateUserAffinity(self, dirMap, actorMap, genreMap, likesMap):
        print "%d %d %d %d" % (len(dirMap.keys()), len(actorMap.keys()), len(genreMap.keys()), len(likesMap.keys()))
        
        self.UD = np.ndarray((self.usersCount, self.directorsCount))
        self.UG = np.ndarray((self.usersCount, self.genreCount))
        self.UA = np.ndarray((self.usersCount, self.actorsCount))
        
        for user_id, ratedMovies in likesMap.items():
            # print "User id, ", user_id
            
            for dir_id, movies in dirMap.items():
                #print "Dir id %s ", dir_id
                dirLike = len(movies.intersection(ratedMovies[1])) / float(len(movies.intersection(ratedMovies[0]))+1)
                self.UD[user_id][dir_id] = dirLike
            
            for act_id, movies in actorMap.items():
                actLike = len(movies.intersection(ratedMovies[1])) /float(len(movies.intersection(ratedMovies[0]))+1)
                self.UA[user_id][act_id] = actLike
                
            for genre_id, movies in genreMap.items():
                genreLike = len(movies.intersection(ratedMovies[1])) / float(len(movies.intersection(ratedMovies[0]))+1)
                self.UG[user_id][genre_id] = genreLike
                
        #self.writeFile("model/ud.h5", self.UD)
        #self.writeFile("model/ua.h5", self.UA)
        #self.writeFile("model/ug.h5", self.UG)
        
    
    """
    Calculate affinity between DxA, DxG and AxG
    """
    def calculateAffinityBetweenEntities(self):
        
        self.DA = np.ndarray((self.directorsCount, self.actorsCount))
        self.DG = np.ndarray((self.directorsCount, self.genreCount))
        self.AG = np.ndarray((self.actorsCount, self.genreCount))
        
        # affinity between directors and actors
        self.DA = np.dot(self.UD.T, self.UA)
        # self.writeFile("model/da.h5", self.DA)
        
        # affinity between directors and genre
        self.DG = np.dot(self.UD.T, self.UG)
        # self.writeFile("model/dg.h5", self.DG)
        
        # affinity between actors and genre 
        self.AG = np.dot(self.UA.T, self.UG)
        # self.writeFile("model/ag.h5", self.AG)
        
    """
    Calculate affinity between DxD, AxA and GxG
    """    
    def calculateSelfAffinity(self):
        
        self.DD = np.ndarray((self.directorsCount, self.directorsCount))
        self.GG = np.ndarray((self.genreCount, self.genreCount))
        self.AA = np.ndarray((self.usersCount, self.actorsCount))
        
        print "Self affinity of DD"
        # affinity between directors
        self.DD = np.dot(np.dot(self.DA, self.AG), self.DG.T)
        #self.writeFile("model/dd.h5", self.DD)
        
        print "Self affinity of AA"
        # affinity between actors
        self.AA = np.dot(np.dot(self.AG, self.DG.T), self.DA)
        #self.writeFile("model/aa.h5", self.AA)
        
        print "Self affinity of GG"
        # affinity between genres
        self.GG = np.dot(np.dot(self.DG.T, self.DA), self.AG)
        #self.writeFile("model/gg.h5", self.GG)
        
    def writeFile(self, filename, obj):
        with h5py.File(filename, 'w') as hf:
            hf.create_dataset('data', data=obj)
            
    def readFile(self, filename):
        read = None
        with h5py.File(filename, 'r') as hf:
            read = np.array(hf.get('data'))
        return read
        
    
