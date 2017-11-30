class Movie:
    
    def __init__(self, movie_id, name):
        self.name = name
        self.movie_id = movie_id
        self.actors = []
        self.director = ""
        self.genre = ""
        self.rating = 0
        
    def add_rating(self, rating):
        self.rating = rating    
    
    def add_actor(self, actor):
        self.actors.append(actor)
    
    def add_director(self, director):
        self.director = director
        
    def add_genre(self, genre):
        self.genre = genre
        
class Actor:
    
    def __init__(self, name):
        self.name = name
        self.worked_in = []
    
    def add_worked_in(self, movie):
        self.worked_in.append(movie)
        
class Director:
    
    def __init__(self, name):
        self.name = name
        self.worked_in = []
    
    def add_worked_in(self, movie):
        self.worked_in.append(movie)
        
class Genre:
    
    def __init__(self, name):
        self.name = name
        self.worked_in = []
        
class User:
    
    def __init__(self, name):
        self.name = name
        self.likes = {}
        
    def add_movie(self, movie, rating):
        self.likes.append(movie, rating)
        

