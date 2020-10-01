import socket
from _thread import *
import pickle
from game import Game

server = "192.168.194.152"
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

def threaded_client(conn, p, gameId):
    global idCount
    #Send playerID to client
    conn.send(str.encode(str(p)))
    ###
    reply = ""
    
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

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    ###Getting name
    
    ###
    idCount += 1
    p = len(players) + 1
    players.append(p)
    gameId = (idCount - 1)//2
    
    if idCount % 2 == 1:
        games[gameId] = Game(gameId,p)
        print("Creating a new game...")
        print(idCount,p,gameId)
    else:
        games[gameId].addPlayer(p)
        games[gameId].ready = True  
        print("Start new game ....")
        print(idCount,p,gameId)
    #print("------")
    start_new_thread(threaded_client, (conn, p, gameId))
