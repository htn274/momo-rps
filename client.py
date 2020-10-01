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

# topPlayer = []
# # generate player
# for i in range(55):
#     topPlayer.append(['Player' + str(i), str(i)])

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
        text_name = font.render(p.name, 1, (0, 255,255))
        text_score = font.render(str(p.gamePoints), 1, (0, 255, 255))
        win.blit(text_name, (80, 200))
        win.blit(text_score, (80, 250))

        opponent = game.player2 if game.player1.id == p.id else game.player1
        text_name = font.render(opponent.name, 1, (0, 255,255))
        text_score = font.render(str(opponent.gamePoints), 1, (0, 255, 255))
        win.blit(text_name, (400, 200))
        win.blit(text_score, (400, 250))

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

    player = n.getP()
    
    print("You are player", player)
    
    while run:
        clock.tick(60)
        try:
            game = n.send("get")
            assert game is not None
        except:
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            # redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except Exception as ex:
                run = False
                print("Couldn't get game", ex)
                break
            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == player.id):
                text = font.render("You Won!", 1, (255,0,0))
                game = n.send('win')
                print('Get game state from server for player', player.id, 'after winning with new score', (game.player1 if player.id == game.player1.id else game.player2).gamePoints)
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, (255,0,0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))
                game = n.send('lost')
                print('Get game state from server')

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
                        if player.id == game.player1.id:
                            if not game.player1.playerWent:
                                game = n.send(btn.text)
                        else:
                            if not game.player2.playerWent:
                                game = n.send(btn.text)

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
