import pygame
import random 
import math 
from pygame import mixer 

pygame.init()

# creating a screen for the game 
screen = pygame.display.set_mode((800,600))

# Background 
bg = pygame.image.load("bg.png")

# Background Music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and display icon 
pygame.display.set_caption("Space Monsters")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)

# Player Image 
playerImage = pygame.image.load("arcadegame.png")
playerX = 368
playerY = 500
playerXchange = 0

# Enemy Image 
enemyImage = []
enemyX = []
enemyY = []
enemyXchange = []
enemyYchange = []
num = 6 
for i in range (num) :
    enemyImage.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyXchange.append(4)
    enemyYchange.append(40)

# Bullet 

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 500
bulletXchange = 0
bulletYchange = 10
bulletstate = "ready"

#Score 

score_value = 0 
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10

# Game Over
over_font = pygame.font.Font('freesansbold.ttf', 64)

def showscore(x,y) :
    score = font.render("Score : " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def player(x,y) :
    screen.blit(playerImage,(x,y))

def enemy(x,y,i) :
    screen.blit(enemyImage[i],(x,y))

def firebullet(x,y) :
    global bulletstate
    bulletstate = "fire"
    screen.blit(bulletImg,(x + 16, y + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY) :
    distance = math.sqrt(math.pow(enemyX - bulletX,2) + math.pow(enemyY - bulletY,2))
    if distance < 27 :
        return True 
    return False 

def gameOverText():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Game Loop
running = True 
while running :

    #Adding background colour
    screen.fill((0,0,0))
    screen.blit(bg,(0,0))
    

    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False

    # Moving the spaceship on pressing the left or right arrow key 
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
                playerXchange = -5
            if event.key == pygame.K_RIGHT :
                playerXchange = 5
            if event.key == pygame.K_SPACE :
                if bulletstate == "ready" :
                    bulletsound = mixer.Sound("laser.wav")
                    bulletsound.play()
                    bulletX = playerX
                    firebullet(bulletX,bulletY)
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXchange = 0


    playerX = playerX + playerXchange
    # Making sure that our spaceship stays within the game screen 
    if playerX < 0:
        playerX = 0
    if playerX > 736 :
        playerX = 736
    
    
    # Enemy Movement 
    for i in range(num) :
        if enemyY[i] > 460 :
            for j in range(num) :
                enemyY[j] = 2000
            gameOverText()
            break
        if enemyX[i] <= 0:
            enemyXchange[i] = 4
            enemyY[i] = enemyY[i] + enemyYchange[i]

        elif enemyX[i] >= 736 :
            enemyXchange[i] = -4
            enemyY[i] = enemyY[i] + enemyYchange[i]

        enemyX[i] = enemyX[i] + enemyXchange[i]

        # Check for collision 
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision :
            explosionsound = mixer.Sound("explosion.wav")
            explosionsound.play()
            bulletY = 500
            bulletstate = "ready"
            score_value += 1 
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i],i)

    # Bullet Movement
    if bulletY < 0 :
        bulletY = 500
        bulletstate = "ready"
    if bulletstate == "fire" :
        firebullet(bulletX,bulletY)
        bulletY -= bulletYchange

    

    player(playerX,playerY)
    showscore(textX,textY)
    pygame.display.update()
    
    