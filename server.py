import socket
from _thread import *
import pickle
from game import Game
from player import Player

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

def threaded_client(conn, p, gameId):
    global idCount

    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        print('Player {}: {}'.format(p.name, data))
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

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
    
    threaded_client(conn, player, gameId)


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    idCount += 1
    pid += 1
    start_new_thread(create_player, (conn, pid))
    # gameId = (idCount - 1)//2
    
    # if idCount % 2 == 1:
    #     games[gameId] = Game(gameId,p)
    #     print("Creating a new game...")
    #     print(idCount,p,gameId)
    # else:
    #     games[gameId].addPlayer(p)
    #     games[gameId].ready = True  
    #     print("Start new game ....")
    #     print(idCount,p,gameId)
    # #print("------")
    # start_new_thread(threaded_client, (conn, p, gameId))
