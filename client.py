import pygame
import math
from UI import Button, InputBox
from network import Network
import pickle
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

topPlayer = []
# generate player
for i in range(55):
    topPlayer.append(['Player' + str(i), str(i)])

def draw10PlayerBoard(win, scoreBoard):
    print("lent board", len(scoreBoard))
    for i in range(len(scoreBoard)):
        print(i)
        font = pygame.font.SysFont("comicsans", 30)
        text_name = font.render(scoreBoard[i][0], 1, (255,255,255))
        font = pygame.font.SysFont("comicsans", 30)
        text_score = font.render(scoreBoard[i][1], 1, (255,255,255))
        win.blit(text_name, (250, 200 + (30*i)))
        win.blit(text_score, (350, 200 + (30*i)))
        pygame.display.update()
        


def drawLeaderBoard(win, topPlayer):
    # Rangkings Chart
    run = True
    clock = pygame.time.Clock()
    print("len top", len(topPlayer))
    numPage = math.ceil(len(topPlayer)/10)
    print("numpage", numPage)
    page = 0
    clock.tick(60)


    while run:
        font = pygame.font.SysFont("comicsans", 30)
        text_BXH = font.render("Rankings Chart", 1, (255, 255, 255))

        win.blit(text_BXH, (100,50))

        buttonBefore = Button("Before", 300, 50, (255,0,0), 50, 20)
        buttonAfter = Button("After", 360, 50, (255, 0, 0), 50, 20)
        buttonBefore.draw(win, 20)
        buttonAfter.draw(win, 20)
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
                
    
                    

def redrawWindow(win, game, p):
    win.fill((128,128,128))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()

btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You Won!", 1, (255,0,0))
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))

            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    drawLeaderBoard(win, topPlayer)



    # font = pygame.font.SysFont("comicsans", 60)
    # text_title = font.render("Rock Paper Scissors Game", 1, (255,0,0))
    # font = pygame.font.SysFont("comicsans", 30)
    # text_enter = font.render("Enter your name:", 1, (255,255,255))
    # btn_join = Button("Play game", 150, 450, (255,0,0), 300, 80)
    # ib_name = InputBox(100, 350, 140, 32)
    # while run:
    #     win.fill((30, 30, 30))
    #     win.blit(text_title, (80,200))
    #     win.blit(text_enter, (100,300))
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             run = False
    #         ib_name.handle_event(event)
    #     ib_name.update()
    #     ib_name.draw(win)
    #     btn_join.draw(win)
    #     pygame.display.flip()
        # clock.tick(30)

    # input_box1 = InputBox(100, 100, 140, 32)
    # input_box2 = InputBox(100, 300, 140, 32)
    # input_boxes = [input_box1, input_box2]
    # done = False

    # while not done:
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             done = True
    #         for box in input_boxes:
    #             box.handle_event(event)

    #     for box in input_boxes:
    #         box.update()

    #     win.fill((30, 30, 30))
    #     for box in input_boxes:
    #         box.draw(win)

    #     pygame.display.flip()
    #     clock.tick(30)

    # while run:
    #     clock.tick(60)
    #     win.fill((128, 128, 128))
    #     font = pygame.font.SysFont("comicsans", 60)
    #     text = font.render("Click to Play!", 1, (255,0,0))
    #     win.blit(text, (100,200))
    #     pygame.display.update()

    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             pygame.quit()
    #             run = False
    #         if event.type == pygame.MOUSEBUTTONDOWN:
    #             run = False

    # main()

# while True:
menu_screen()


