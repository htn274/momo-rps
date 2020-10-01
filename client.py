import pygame
from UI import Button, InputBox, Color
from network import Network
import pickle
pygame.font.init()

width = 700
height = 700
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")
uname = ''

def redrawWindow(win, game, p):
    win.fill((30,30,30))

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Waiting for Player...", 1, (255,0,0), True)
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render(p.name, 1, (0, 255,255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

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

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 50, 500, (0,0,0)), Button("Scissors", 250, 500, (255,0,0)), Button("Paper", 450, 500, (0,255,0))]
def main():
    run = True
    clock = pygame.time.Clock()
    n = Network(uname)

    # print('Send {} to server'.format(uname))
    # n.send(uname)

    player = n.getP()
    
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
            if (game.winner() == player.id):
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
                            if not game.player1.playerWent:
                                n.send(btn.text)
                        else:
                            if not game.player2.playerWent:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    global uname
    run = True
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("comicsans", 60)
    text_title = font.render("Rock Paper Scissors Game", 1, (255,0,0))
    font = pygame.font.SysFont("comicsans", 30)
    text_enter = font.render("Enter your name:", 1, (255,255,255))
    btn_join = Button("Play game", 150, 450, (255,0,0), 300, 80)
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

while True:
    menu_screen()
