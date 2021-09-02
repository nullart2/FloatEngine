#Uses Python with SDL2
#C++/C# is Not Yet Supported

class Level:
    #store functions
    def __init__(self, platforms = None, entities = None, winFunc = None, loseFunc = None):
        self.platforms = platforms
        self.entities = entities
        self.winFunc = winFunc
        self.loseFunc = loseFunc
    #win condition
    def isWon(self):
        if self.winFunc is None:
            return False #have not won yet
        return self.winFunc(self)
    #lose condition
    def isLost(self):
        if self.loseFunc is None:
            return False #have not lost yet
        return self.loseFunc(self)