import random   
import sys
import pygame
from pygame.locals import *

# global vriables for the game
fps = 30
screen_width = 289
screen_height = 511
screen = pygame.display.set_mode((screen_width, screen_height))
#screen = pygame.display.set_mode((screen_width,screen_height), pygame.SCALED | pygame.FULLSCREEN)
ground_y = screen_height * 0.82

# game dictionaries
game_sprites = {}
game_sounds = {}



player = 'gallery/sprites/bird2.png'



def welcomescreen():
    playerx = int(screen_width / 5)
    playery = int((screen_height - game_sprites['player'].get_height())/2)
    messagex = int((screen_width - game_sprites['message'].get_width()) / 2)
    messagey = 0
    basex = 0
    while True:
        a=random.randint(1,2)
        background = 'gallery/sprites/background'+str(a)+'.png'
        game_sprites['background'] = pygame.image.load(background).convert()
        b= random.randint(1,2)
        pipe = 'gallery/sprites/pipe'+str(b)+'.png'
        game_sprites['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(),180),
        pygame.image.load(pipe).convert_alpha())
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) or event.type == MOUSEBUTTONDOWN:
                return
            else:
                screen.blit(game_sprites['background'], (0,0))
                screen.blit(game_sprites['message'], (messagex, messagey))
                screen.blit(game_sprites['player'],(playerx,playery))
                screen.blit(game_sprites['base'],(basex,ground_y))
                pygame.display.update()
                fpsclock.tick(fps)
def maingame():
    score = 0
    playerx = int(screen_width/5)
    playery = int(screen_width/2)
    basex = 0

    # pipes
    newpipe1 = getrandompipe()
    newpipe2 = getrandompipe()

    # upper pipes
    upperpipes=[
        {'x': screen_width + 200, 'y': newpipe1[0]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': newpipe2[0]['y']}
        ]
    # lower pipes
    lowerpipes=[
        {'x': screen_width + 200, 'y': newpipe1[1]['y']},
        {'x': screen_width + 200 + (screen_width / 2), 'y': newpipe2[1]['y']}
        ]

    pipevelx = -4

    playervely = -9
    playermaxvely = 10
    playerminvely = -8
    playeraccy = 1

    playerflapaccv = -8
    playerflapped = False


    while True:
        a=random.randint(1,2)
        background = 'gallery/sprites/background'+str(a)+'.png'
        
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP) or event.type == MOUSEBUTTONDOWN:
                if playery > 0:
                    playervely = playerflapaccv
                    playerflapped = True
                    game_sounds['wing'].play()

        crashtest = isCollide(playerx, playery, upperpipes, lowerpipes)
        
        
        if crashtest:
            f=open('gallery/highscore/highscore',"r")
            highscore = f.read()
            if int(highscore) < score:
        	    highscore = str(score)
            
            
            f.close()
            f=open('gallery/highscore/highscore',"w")
            f.write(highscore)
            f.close()
            myhs = [int(x) for x in list(highscore)]
            width = 0
            for digit in myhs:
                width += game_sprites['numbers'][digit].get_width()
        
                xoffset = (screen_width - width) / 2
            for digit in myhs:
                screen.blit(game_sprites['numbers'][digit], (xoffset, screen_height * 0.32))
                xoffset += game_sprites['numbers'][digit].get_width()
            
            screen.blit(game_sprites['yourscore'],(0,0))
            screen.blit(game_sprites['highscore'],(screen_width - game_sprites['highscore'].get_width(), game_sprites['highscore'].get_height()))
            
            pygame.display.update()
            return

        # score
        playermidpos = playerx + game_sprites['player'].get_width() / 2
        for pipe in upperpipes:
            pipemidpos = pipe['x'] + game_sprites['pipe'][0].get_width() / 2
            if pipemidpos <= playermidpos < pipemidpos + 4:
                score += 1
                print("your score is",score)
                game_sounds['point'].play()

        if playervely < playermaxvely and not playerflapped:
            playervely += playeraccy
            
        if playerflapped:
            playerflapped = False

        playerheight = game_sprites['player'].get_height()
        playery = playery + min(playervely, ground_y - playery - playerheight)
        
        #move pipes to left
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            upperpipe['x'] += pipevelx
            lowerpipe['x'] += pipevelx

        if 0 < upperpipes[0]['x'] < 5:
            newpipe = getrandompipe()
            upperpipes.append(newpipe[0])
            lowerpipes.append(newpipe[1])

        if upperpipes[0]['x'] < -game_sprites['pipe'][0].get_width():
            upperpipes.pop(0)
            lowerpipes.pop(0)
            
          
 # blit sprites
        screen.blit(game_sprites['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upperpipes, lowerpipes):
            screen.blit(game_sprites['pipe'][0], (upperpipe['x'], upperpipe['y']))
            screen.blit(game_sprites['pipe'][1], (lowerpipe['x'], lowerpipe['y']))        
        
        screen.blit(game_sprites['base'], (basex, ground_y))
        screen.blit(game_sprites['player'], (playerx, playery))
        mydigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in mydigits:
            width += game_sprites['numbers'][digit].get_width()
        
        xoffset = (screen_width - width) / 2
        
        for digit in mydigits:
            screen.blit(game_sprites['numbers'][digit], (xoffset, screen_height * 0.12))
            xoffset += game_sprites['numbers'][digit].get_width()
        
        pygame.display.update()
        fpsclock.tick(fps)

def isCollide(playerx, playery, upperpipes, lowerpipes):
    if playery > ground_y - 25 or playery < 0:
        game_sounds['hit'].play()
        screen.blit(game_sprites['game_over'],(0,(screen_height/2)-50))
        pygame.display.update()
        
        
        return True
        
        

    for pipe in upperpipes:
        pipeheight = game_sprites['pipe'][0].get_height()
        if(playery <= pipeheight + pipe['y'] and abs(playerx - pipe['x'])+20 < game_sprites['pipe'][0].get_width()):
            game_sounds['hit'].play()
            screen.blit(game_sprites['game_over'],(0,(screen_height/2)-50))
            pygame.display.update()
            return True

    for pipe in lowerpipes:
        if (playery + game_sprites['player'].get_height() >= pipe['y']) and abs(playerx - pipe['x'])+20 < game_sprites['pipe'][0].get_width():
            game_sounds['hit'].play()
            screen.blit(game_sprites['game_over'],(0,(screen_height/2)-50))
            pygame.display.update()
            return True

    
    return False

def getrandompipe():
    pipeheight = game_sprites['pipe'][0].get_height()
    offset = screen_height/3
    y2 = offset + random.randrange(0, int(screen_height - game_sprites['base'].get_height() - 1.2*offset))
    pipex = screen_width + 10
    y1 = pipeheight - y2 + offset
    pipe = [
        {"x": pipex, 'y': -y1},
        {"x": pipex, 'y': y2}
    ]
    return pipe

if __name__ == "__main__":
    a = random.randint(1, 2)
    b= random.randint(1,2)
    pipe = 'gallery/sprites/pipe'+str(b)+'.png'
    background = 'gallery/sprites/background'+str(a)+'.png'
    pygame.init()
    fpsclock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    game_sprites['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    )

    game_sprites['message'] = pygame.image.load('gallery/sprites/message1.png').convert_alpha()
    game_sprites['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    game_sprites['pipe'] = (pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(),180),

                pygame.image.load(pipe).convert_alpha()
    )

    game_sounds['die'] = pygame.mixer.Sound('gallery/audio/die.ogg')
    game_sounds['hit'] = pygame.mixer.Sound('gallery/audio/hit.ogg')
    game_sounds['point'] = pygame.mixer.Sound('gallery/audio/point.ogg')
    game_sounds['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.ogg')
    game_sounds['wing'] = pygame.mixer.Sound('gallery/audio/wing.ogg')

    game_sprites['background'] = pygame.image.load(background).convert()
    game_sprites['player'] = pygame.image.load(player).convert_alpha()
    game_sprites['game_over'] = pygame.image.load("gallery/sprites/gameover.png").convert_alpha()
    game_sprites['yourscore'] = pygame.image.load("gallery/sprites/yourscore.png").convert_alpha()
    game_sprites['highscore'] = pygame.image.load("gallery/sprites/highscore.png").convert_alpha()

    while True:
        welcomescreen()
        maingame()
