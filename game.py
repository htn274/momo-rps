from player import Player
class Game:
    def __init__(self, id, player1, player2 = None):
        self.player1 = player1
        self.player2 = player2
        self.ready = False
        self.id = id
        self.moves = [[], []] #{player1: None, player2: None}
        self.wins = [0,0]
        self.ties = 0
        self.num_players = 1

    #check in server.py
    def addPlayer2(self, player2):
        if self.player2 == None:
            self.player2 = player2
            self.ready = True
            self.num_players += 1
            return True
        return False

    def get_player_move(self, p):
        """
        :param p: [0, 1]
        :return: Move
        """
        if self.moves[p]:
            return self.moves[p][-1]
        return None

    def finished(self):
        return len(self.moves[0]) == len(self.moves[1]) == 3

    def get_result(self, p):
        print('Game points', self.player1.gamePoints, self.player2.gamePoints)
        if self.player1.gamePoints == self.player2.gamePoints:
            return 'TIE ' + str(p.gamePoints)
        if p.id == self.player1.id:
            self.player1.totalPoints += 3
            return 'WIN ' + str(self.player1.totalPoints) if self.player1.gamePoints > self.player2.gamePoints else 'LOST'
        else:
            self.player2.totalPoints += 3
            return 'LOST ' + str(self.player1.totalPoints)  if self.player1.gamePoints > self.player2.gamePoints else 'WIN'

    def play(self, player, move):
        if player.id == self.player1.id:
            self.moves[0].append(move)
            self.player1.playerWent = True
        else:
            self.moves[1].append(move)
            self.player2.playerWent = True

    def connected(self):
        return self.ready

    def bothWent(self):
        return self.player1.playerWent and self.player2.playerWent

    def winner(self):

        p1 = self.moves[0][-1].upper()[0]
        p2 = self.moves[1][-1].upper()[0]

        winner = -1
        if p1 == "R" and p2 == "S":
            winner = self.player1.id
        elif p1 == "S" and p2 == "R":
            winner = self.player2.id
        elif p1 == "P" and p2 == "R":
            winner = self.player1.id
        elif p1 == "R" and p2 == "P":
            winner = self.player2.id
        elif p1 == "S" and p2 == "P":
            winner = self.player1.id
        elif p1 == "P" and p2 == "S":
            winner = self.player2.id

        return winner

    def resetWent(self):
        self.player1.playerWent = False
        self.player2.playerWent = False

if __name__ == '__main__':
    p1 = Player(1, 'n1')
    game = Game(1, p1)
    print(game.ready)
    p2 = Player(2, 'n2')
    print(game.addPlayer2(p2))
    # Play
    game.play(p1, 'S')
    game.play(p2, 'R')
    print(game.winner())