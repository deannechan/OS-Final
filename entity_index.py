
class EntityIndex:

    def __init__(self):
        self._index = {}
        self._indexCounter = 0
        self._reverseIndex = {}

    def getEntityIndex(self, name):
        entityIndex = None
        if name:
            if name not in self._index:
                entityIndex = self._indexCounter
                self._index[name] = entityIndex
                self._reverseIndex[entityIndex] = name
                self._indexCounter += 1
            else:
                entityIndex = self._index[name]
        return entityIndex

    def getEntityByIndex(self, entityIndex):
        ret = None
        if entityIndex in self._reverseIndex:
            ret = self._reverseIndex[entityIndex]
        return ret

class ChannelIndex:

    def __init__(self, channels):
        self._channelIndices = {}
        for c in channels:
            self._channelIndices[c] = EntityIndex()

    def getEntityIndex(self, channel, name):
        index = self._channelIndices[channel]
        return index.getEntityIndex(name)

    def getEntityByIndex(self, channel, entityIndex):
        index = self._channelIndices[channel]
        return index.getEntityByIndex(entityIndex)

class Channels:
    DIRECTOR = 'director'
    USER = 'user'
    MOVIE = 'movie'
    ACTOR = 'actor'
    GENRE = 'genre'
    CHANNELS = [DIRECTOR, USER, MOVIE, ACTOR, GENRE]
