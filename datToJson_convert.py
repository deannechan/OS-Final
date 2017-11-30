import numpy as np
import csv
import json
from objects import *
import codecs


#this function returns the column name using the header variable and the values using the dataNumpy variable
def read_data(filename):
    newLines = []
    with open(filename, 'r') as input_file: 
            heading = input_file.readline().split("\t")
            heading = [x.rstrip() for x in heading]
            for line in input_file.readlines()[0:]:
                read_data = line.split("\t")
                read_data = [x.rstrip() for x in read_data]
                newLines.append(read_data)
    header = np.asarray(heading, dtype=np.str_)        
    dataNumpy =  np.asarray(newLines, dtype=np.str_)  
    return header, dataNumpy


def getObjectDictionary(obj):
    return obj.__dict__    
    
def ensure_unicode(v):
    if isinstance(v, str):
        v = v.decode('utf8')
    return unicode(v)
"""
movies : id:0, title:1, aud_rating:17
"""    
def dataFromFiles(heading_mov, dataNumpy_mov, heading_act, dataNumpy_act, heading_dir, dataNumpy_dir, heading_gen, dataNumpy_gen, heading_rat, dataNumpy_rat): 
    #create a JSON file of likes(user, movie):        
    userID_r = dataNumpy_rat[:,0].tolist()
    movieID_r = dataNumpy_rat[:,1].tolist()
    rating_r = dataNumpy_rat[:,2].tolist()

    with open('json/movies.json', 'w') as outfile:
        
        movies = {}
        
        mov_ids = dataNumpy_mov[:,0].tolist()
        mov_names = dataNumpy_mov[:,1].tolist()
        mov_ratings = dataNumpy_mov[:,17].tolist()
        
        #create dictionary of movies
        for i in range(50):
            movie = Movie(mov_ids[i], mov_names[i])
            movie.add_rating(mov_ratings[i])
            
            #add object to dictionary
            movies[mov_ids[i]] = movie
        
        #add actors to movies
        for i in range(len(dataNumpy_act[:,0])):
            movieId = dataNumpy_act[i][0]
            if movieId in movies:
                movie = movies[movieId]
                movie.add_actor(dataNumpy_act[i][1])
            
        #add director in movies
        for i in range(len(dataNumpy_dir[:,0])):
            movieId = dataNumpy_dir[i][0]
            if movieId in movies:
                movie = movies[movieId]
                movie.add_director(dataNumpy_dir[i][1])
            
        #add genre in movies
        for i in range(len(dataNumpy_gen[:,0])):
            movieId = dataNumpy_gen[i][0]
            if movieId in movies:
                movie = movies[movieId]
                movie.add_genre(dataNumpy_gen[i][1]) 
        
        #for m in movies.values():
        #    print getObjectDictionary(m)
               
        json.dump(movies.values(), outfile, default=getObjectDictionary, encoding='latin-1')

    outArr = []
    # print len(userID_r)/8
    for i in range(len(userID_r)/4): #len(userID_r)
        data = {heading_rat[0]: userID_r[i], heading_rat[1]: movieID_r[i], heading_rat[2]: rating_r[i]}
        outArr.append(data)

    with open('json/likes.json', 'w') as outfile:
        json.dump(outArr, outfile)

    #create a JSON file of likes(user, movie):        

   
########################################################################################################    
    
if __name__=="__main__":
    print "Reading the data...\n"
    head_mov, data_mov = read_data('data/movies.dat')
    head_act, data_act = read_data('data/movie_actors.dat')
    head_dir, data_dir = read_data('data/movie_directors.dat')
    head_gen, data_gen = read_data('data/movie_genres.dat')
    head_rat, data_rat = read_data('data/user_ratedmovies.dat')
    
    dataFromFiles(head_mov, data_mov, head_act, data_act, head_dir, data_dir, head_gen, data_gen, head_rat, data_rat)
