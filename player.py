class Player:
    def __init__(self, id, name):
        self.id = id 
        self.name = name
        self.numTurns = 20
        self.totalPoints = 0
        self.gamePoints = 0
        self.status = True
        self.playerWent = False
    def __str__(self):
        return str(self.id) + ' ' + self.name
        

if __name__ == '__main__':
    p = Player(1, 'n1')