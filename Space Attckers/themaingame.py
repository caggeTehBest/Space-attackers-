
import math
import random
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect
import pygame_menu
import time





from pygame.locals import *

BLUE = (106, 159, 181)
WHITE = (255, 255, 255)

is_paused = False
import pygbutton

import pygame
from pygame import mixer
with open("hiscore.txt", "r") as f:
    hiscore = f.read()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
# Intialize the pygame
pygame.init()


screen = pygame.display.set_mode((800, 600))



# Background
background = pygame.image.load('background.jpg')



# Caption and Icon
pygame.display.set_caption("Space Attackers")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('spaceship1.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)



def show_score(x, y):
    score = over_font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
def show_hiscore(x, y):
    global hiscore
    hiscore_show = over_font.render("Hiscore : " + str(hiscore), True, (255, 255, 255))
    screen.blit((hiscore_show), (x, y))
def Write_Line(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font("freesansbold.ttf", textSize)
    newText=newFont.render(message, 0, textColor)
 
    return newText

 
 
# Colors

 
# Game Fonts
font = "Retro.ttf"
 
 
# Game Framerate

  # Sound
mixer.music.load("bgmusic.mp3")
mixer.music.play(-1)
     



# Game Loop
running = True
while running == True:
    if not is_paused:
      

        if score_value  > int(hiscore):
            hiscore = score_value
        

        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_change = -6
                if event.key == pygame.K_RIGHT:
                    playerX_change = 6
                if event.key == pygame.K_SPACE:
                    if bullet_state is "ready":
                        bulletSound = mixer.Sound("bullet_sound.wav")
                        bulletSound.play()
                        # Get the current x cordinate of the spaceship
                        bulletX = playerX
                        fire_bullet(bulletX, bulletY)
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 4 or event.button == 5:
                        if bullet_state is "ready":
                            bulletSound = mixer.Sound("laser.wav")
                            bulletSound.play()
                            # Get the current x cordinate of the spaceship
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)
                if event.type == pygame.JOYHATMOTION:
                    if event.value[0] == 1:
                        playerY_change = -5
                    if event.value[0] == -1:
                        playerX_change = 5
                    if event.value[0] == 0:
                        playerX_change = 0
                        playerY_change = 0

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change = 0

        # 5 = 5 + -0.1 -> 5 = 5 - 0.1
        # 5 = 5 + 0.1

        playerX += playerX_change
        if playerX <= 0:
            playerX = 0
        elif playerX >= 736:
            playerX = 736

        # Enemy Movement
        for i in range(num_of_enemies):

            # Game Over
            if enemyY[i] > 440:
                for j in range(num_of_enemies):
                    enemyY[j] = 2000
                with open("hiscore.txt", "w") as f:
                    f.write(str(hiscore))
                game_over_text()
                break

            enemyX[i] += enemyX_change[i]
            if enemyX[i] <= 0:
                enemyX_change[i] = 4
                enemyY[i] += enemyY_change[i]
            elif enemyX[i] >= 736:
                enemyX_change[i] = -4
                enemyY[i] += enemyY_change[i]

            # Collision
            collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
            if collision:
                
                explosionSound = mixer.Sound("Explosion+3.wav")
                explosionSound.play()
                bulletY = 480
                bullet_state = "ready"
                score_value += 1
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)

            enemy(enemyX[i], enemyY[i], i)

        # Bullet Movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"

        if bullet_state is "fire":
            fire_bullet(bulletX, bulletY)
            bulletY -= bulletY_change

        player(playerX, playerY)
        show_score(textX, testY)
        show_hiscore(textX, testY + 47)
        pygame.display.update()




    

#menu = pygame_menu.Menu(300, 400, 'Welcome',
 #                theme=pygame_menu.themes.THEME_BLUE)
#menu.add_text_input('Name :', default='Reyansh Kumar')
#menu.add_selector('Difficulty :', [('Hard', 1), ('Easy', 2)])
#menu.add_button('Play', start_game())
#menu.add_button('Quit', pygame_menu.events.EXIT)
#menu.mainloop(screen)

    
