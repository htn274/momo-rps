import socket
from _thread import *
import pickle
from game import Game
from player import Player
import threading

server = "localhost"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0
players = {}
pid = 0
count_lock = threading.Lock()
barrier = threading.Lock()
barrier.acquire()
count = 0
print_lock = threading.Lock()
turn = 2
def start_game(conn, p, gameId):
    global idCount, count, turn

    while True:
        try:
            data = conn.recv(4096).decode()
            print('Get {} from {}'.format(data, p.name))
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                        # with count_lock:
                        #     turn -= 1
                        #     print(p.name, turn)
                        #     if turn == 0:
                        #         if games[gameId].player1.gamePoints > games[gameId].player2.gamePoints:
                        #             games[gameId].player1.totalPoints += 3
                        #         else:
                        #             games[gameId].player2.totalPoints += 3

                        #         if p.gamePoints > min(games[gameId].player1.gamePoints, games[gameId].player2.gamePoints):
                        #             mess = 'WON ' + str(p.totalPoints)
                        #         else:
                        #             mess = 'LOST ' + str(p.totalPoints)
                        #         conn.sendall(str.encode(mess))
                        #         break
                    elif data == "win":
                        p.gamePoints += 1
                    elif data != "get":
                        game.play(p, data)

                    print('Send game to ', p.name)
                    conn.sendall(str.encode('game', 'utf-8'))
                    conn.recv(4096).decode()
                    print('Send Game Object to ', p.name)
                    conn.sendall(pickle.dumps(game))
            else:
                break
        except Exception as ex:
            print(ex)
            break

    
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    
def findGame():
    for gameId, game in games.items():
        if game.player1 == None or game.player2 == None:
            return gameId
    return None

def create_player(conn, pid):
    global games, players, idCount
    pname = conn.recv(4096).decode()
    print('Get pname = ', pname)
    player = Player(pid, pname)
    print('Create new player: ', player)
    conn.sendall(pickle.dumps(player))
    players[pid]= player

    while True:
        idCount += 1
        gameId = findGame()
        if gameId == None:
            gameId = (idCount - 1)//2
            games[gameId] = Game(gameId, player)
            print("Creating a new game...", gameId)
        else:
            games[gameId].addPlayer2(player)
            games[gameId].ready = True
            print("Start a game...", gameId)
        
        start_game(conn, player, gameId)
        break

    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    pid += 1
    start_new_thread(create_player, (conn, pid))