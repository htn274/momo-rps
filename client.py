import pygame
import math
from UI import Button, InputBox, Color
from network import Network
import pickle
import cv2 
import sys
import argparse

import tensorflow as tf
from keras.preprocessing import image
import tensorflow.keras as k
import numpy as np

pygame.font.init()


parser = argparse.ArgumentParser()
parser.add_argument('--camera', const=None, type=str,
                    help='Ip of camera')

camera = None
width = 750
height = 1000
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
screen = pygame.Surface((300, 300))
uname = ''
choose = ''
predict_sign = ''
model = tf.keras.models.load_model('Model_4_classes.h5')
class_name = ['Nothing', 'Paper', 'Rock', 'Scissors']

# topPlayer = []
# # generate player
# for i in range(55):
#     topPlayer.append(['Player' + str(i), str(i)])

def draw10PlayerBoard(win, scoreBoard):
    for i in range(len(scoreBoard)):
        font = pygame.font.SysFont("comicsans", 30)
        text_name = font.render(scoreBoard[i][0], 1, (255,255,255))
        font = pygame.font.SysFont("comicsans", 30)
        text_score = font.render(scoreBoard[i][1], 1, (255,255,255))
        win.blit(text_name, (round(0.4*width), round(0.2*height) + (30*i)))
        win.blit(text_score, (round(0.4*width)+100, round(0.2*height) + (30*i)))
        pygame.display.update()
        
def drawLeaderBoard(win, topPlayer):
    # Rangkings Chart
    run = True
    clock = pygame.time.Clock()
    numPage = math.ceil(len(topPlayer)/10)
    page = 0
    clock.tick(60)

    while run:
        font = pygame.font.SysFont("comicsans", 40)
        text_BXH = font.render("LEADER BOARD", 1, (255, 255, 255))
        win.blit(text_BXH, (round(0.35*width), round(0.1*height)))

        buttonBefore = Button("<<<", round(0.35*width), round(0.65*height), (255,0,0), 50, 30)
        buttonAfter = Button(">>>", round(0.45*width), round(0.65*height), (255, 0, 0), 50, 30)
        buttonBack = Button("Back", round(0.55*width), round(0.65*height), (255, 0, 0), 60, 30)
        buttonBefore.draw(win, 30)
        buttonAfter.draw(win, 30)
        buttonBack.draw(win, 30)
        draw10PlayerBoard(win, topPlayer[page*10: (page+1)*10])   
        pygame.display.update()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if buttonBefore.click(event.pos) == True and page >= 1:
                    page = page - 1
                    win.fill((30, 30, 30))
                elif buttonAfter.click(event.pos) == True and page < numPage-1:
                    page = page + 1
                    win.fill((30, 30, 30))
                elif buttonBack.click(event.pos) == True:
                    continue


def drawWinLost(win, res, score):
    win.fill((30, 30, 30))
    #You won
    text_Res = "You " + res
    font = pygame.font.SysFont("comicsans", 70)
    text_BXH = font.render(text_Res, 1, (255, 255, 255))
    win.blit(text_BXH, (round(0.5*width) - round(text_BXH.get_width()/2), round(0.2*height)))
    #Score
    font = pygame.font.SysFont("comicsans", 150)
    text_Score = font.render(str(score), 1, (255, 255, 255))
    win.blit(text_Score, (round(0.5*width) - round(text_Score.get_width()/2), round(0.35*height)))

    # two button
    buttonBXH = Button("Leader Board", round(0.25*width), round(0.65*height), (255,0,0), Color.white, 150, 40)
    buttonBack = Button("Play again", round(0.55*width), round(0.65*height), (255, 0, 0), Color.white, 150, 40)
    buttonBXH.draw(win, 30)
    buttonBack.draw(win, 30)

    pygame.display.update()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if buttonBXH.click(event.pos) == True:
                pass
            elif buttonBack.click(event.pos) == True:
                pass

def predict(raw_img):
    img = cv2.resize(raw_img, (150, 150), interpolation=cv2.INTER_AREA)
    img = img/255
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.vstack([x])
    images = np.vstack([x])
    classes = model.predict(images, batch_size=10)
    classes = np.reshape(classes, (4, ))
    idx = np.argmax(classes)
    return class_name[idx]

def redrawWindow(win, game, p):
    global screen, predict_sign
    win.fill((30,30,30))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        player = p
        # print('Current score', (game.player1 if player.id == game.player1.id else game.player2).gamePoints)
        # print('Opponent score', (game.player2 if player.id == game.player1.id else game.player1).gamePoints)
        font = pygame.font.SysFont("comicsans", 60)
        p = game.player1 if player.id == game.player1.id else game.player2
        text_title = font.render(str("You"), 1, (0, 255, 255))
        text_name = font.render(p.name, 1, (0, 255,255))
        text_score = font.render(str(p.gamePoints), 1, (0, 255, 255))
        win.blit(text_title, (80, 100))
        win.blit(text_name, (80, 150))
        win.blit(text_score, (80, 200))

        opponent = game.player2 if game.player1.id == p.id else game.player1
        text_title = font.render("Opponent", 1, (0, 255, 255))
        text_name = font.render(opponent.name, 1, (0, 255,255))
        text_score = font.render(str(opponent.gamePoints), 1, (0, 255, 255))
        win.blit(text_title, (400, 100))
        win.blit(text_name, (400, 150))
        win.blit(text_score, (400, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, Color.white)
            text2 = font.render(move2, 1,  Color.white)
        else:
            if game.player1.playerWent and p.id == game.player1.id:
                text1 = font.render(move1, 1,  Color.white)
            elif game.player1.playerWent:
                text1 = font.render("Locked In", 1, Color.white)
            else:
                text1 = font.render("Waiting...", 1,  Color.white)

            if game.player2.playerWent and p.id == game.player2.id:
                text2 = font.render(move2, 1,  Color.white)
            elif game.player2.playerWent:
                text2 = font.render("Locked In", 1,  Color.white)
            else:
                text2 = font.render("Waiting...", 1,  Color.white)

        if p.id == game.player2.id:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        # for btn_id, btn in enumerate(btns):
        #     if btn_id == choose:
        #         btn.color = Color.red
        #     btn.draw(win)
        #     btn.color = Color.white

        ret, frame = camera.read()
        screen.fill(Color.white)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (300, 300), interpolation=cv2.INTER_AREA)
        frame = cv2.flip(frame, 1)
        # frame = frame.swapaxes(0, 1)
        predict_sign = predict(frame)
        # print('Frame: ', type(frame), frame.dtype)
        img = cv2.UMat(frame)
        cv2.putText(img, predict_sign, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        img = cv2.UMat.get(img)
        img = img.swapaxes(0, 1)
        pygame.surfarray.blit_array(screen, img)
        win.blit(screen, (50, 400))
        # pygame.surfarray.blit_array(screen, frame)
        if choose == '':
            btn_submit.draw(win)
        pygame.display.flip()

    pygame.display.update()

# btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]
btns = [Button("Paper", 450, 500, Color.white),
        Button("Rock", 50, 500, Color.white), 
        Button("Scissors", 250, 500, Color.white), ]
btn_submit = Button('Sumbit', 50, 800, Color.red, Color.white, width=150, height=50)

def main():
    global choose
    run = True
    clock = pygame.time.Clock()
    n = Network(uname)

    player = n.getP()
    
    print("You are player", player)
    
    start_time = pygame.time.get_ticks()

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
            # print('Receive:', type(game))
            if isinstance(game, str):
                # print('Update for new game')
                break
        except:
            run = False
            print("Couldn't get game")
            break
    
        if game.bothWent():
            # redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
                # print('Receive : ', type(game))
                if isinstance(game, str):
                    print('Update for new game')
                    break
            except Exception as ex:
                run = False
                print("Couldn't get game", ex)
                break
            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == player.id):
                text = font.render("You Won!", 1, (255,0,0))
                game = n.send("win")
                print('Get game state from server for player', player.id, 'after winning with new score', (game.player1 if player.id == game.player1.id else game.player2).gamePoints)
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))
                print('Get game state from server')

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(1000)

        if game.finished():
            res, score = game.get_result(player).split()
            print('Ecec, you', res, score)
            # n.send('finish')
            while True:
                drawWinLost(win, res, score)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn_submit.click(pos) and game.connected() and predict_sign != class_name[0]:
                    choose = predict_sign
                # for btn_id, btn in enumerate(btns):
                #     if btn.click(pos) and game.connected():
                #         choose = btn_id

        now = pygame.time.get_ticks()
        # print(now - start_time)
        if (now - start_time >= 20000 or choose != '') and game.connected():
            if choose == '':
                choose = class_name[1]
            game = n.send(choose)
            choose = ''
            start_time = pygame.time.get_ticks()
            # if player.id == game.player1.id:
            #     if not game.player1.playerWent:
            #         game = n.send(btns[choose].text)
            #     else:
            #         if not game.player2.playerWent:
            #             game = n.send(btns[choose].text)

        redrawWindow(win, game, player)

def menu_screen():
    global uname
    run = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 60)
    text_title = font.render("Rock Paper Scissors Game", 1, (255,0,0))
    font = pygame.font.SysFont("comicsans", 30)
    text_enter = font.render("Enter your name:", 1, (255,255,255))
    btn_join = Button("Play game", 150, 450, (255,0,0), Color.white, 300, 80)
    ib_name = InputBox(100, 350, 140, 32)
    while run:
        win.fill((30, 30, 30))
        win.blit(text_title, (80,200))
        win.blit(text_enter, (100,300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if btn_join.click(pos):
                    run = False
            ib_name.handle_event(event)
        ib_name.update()
        ib_name.draw(win)
        btn_join.draw(win)
        pygame.display.flip()

        
        clock.tick(30)
    uname = ib_name.text
    main()

def test_camera():
    win.fill(Color.background)
    screen = pygame.Surface((300, 300))
    try:
        while True:

            ret, frame = camera.read()

            screen.fill(Color.white)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (300, 300), interpolation=cv2.INTER_AREA)
            frame = frame.swapaxes(0, 1)
            pygame.surfarray.blit_array(screen, frame)
            win.blit(screen, (100, 100))
            # pygame.surfarray.blit_array(screen, frame)
            pygame.display.flip()

    except (KeyboardInterrupt, SystemExit):
        pygame.quit()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    url = parser.parse_args().camera
    if url == None:
        camera = cv2.VideoCapture(0)
    else:
        camera = cv2.VideoCapture(url + '/video')
    while True:
        # drawWinLost(win, "lost", 0)
        menu_screen()
        # test_camera()
