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
players = []
pid = 0
count_lock = threading.Lock()
barrier = threading.Lock()
barrier.acquire()
count = 0
print_lock = threading.Lock()
def start_game(conn, p, gameId):
    global idCount, count

    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == 'get':
                        conn.sendall(pickle.dumps(game))
                        continue
                    elif data == 'lost':
                        pass
                    elif data == "reset":
                        game.resetWent()
                    elif data == "win":
                        with print_lock:
                            p.gamePoints += 1
                            print('updated point for player', p.id)
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except Exception as ex:
            print(ex)
            break

    print("Lost connection")
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
    global games, players
    pname = conn.recv(4096).decode()
    print('Get pname = ', pname)
    player = Player(pid, pname)
    print('Create new player: ', player)
    conn.sendall(pickle.dumps(player))
    players.append(player)

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

    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    idCount += 1
    pid += 1
    start_new_thread(create_player, (conn, pid))