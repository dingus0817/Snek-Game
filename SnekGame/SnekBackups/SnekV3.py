###########################
#File name: SnekV3.py
#Author: Jamie Zhang
##########################

from random import randint
import pygame
import time
pygame.init()
WIDTH = 800
HEIGHT= 700
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))
 
TOP = 0
BOTTOM = HEIGHT
MIDDLE = int(WIDTH/2.0)
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
GREEN = (0,255,0)
RED = (255,0,0)
outline=0

headCLR = GREEN
segCLR = WHITE

font = pygame.font.SysFont("Arial",80)

#---------------------------------------#
# functions                             #
#---------------------------------------#
##def redrawGameWindow():
##    gameWindow.fill(BLACK)

def drawGrid(gridSize):
    gameWindow.fill(BLACK)
    pygame.draw.rect(gameWindow,RED,(0,600,WIDTH,100),outline)
    for x in range(0,WIDTH,gridSize):
        pygame.draw.line(gameWindow, RED, (x,0),(x,HEIGHT),1)
    for y in range(0,HEIGHT,gridSize):
        pygame.draw.line(gameWindow, RED, (0,y),(WIDTH,y),1)
    scoreText = font.render(str(score),1,WHITE)
    timerText = font.render(str(sec),1,WHITE)
    gameWindow.blit(scoreText,(30,610))
    gameWindow.blit(timerText,(600,610))

def drawSnake():
    for i in range(len(segX)): 
        pygame.draw.circle(gameWindow, segCLR, (segX[i], segY[i]), SEGMENT_R, outline)
    pygame.draw.rect(gameWindow,headCLR,(segX[0] - SEGMENT_R, segY[0] - SEGMENT_R,SEGMENT_R*2,SEGMENT_R*2), outline)


def borders():
    running = False
    if segX[0] >= 0 and segX[0] <= WIDTH and segY[0] >= 0 and segY[0] <= HEIGHT - 100:
        running = True
    return running

def noCollision():
    running = True
    for i in range(1, len(segX)):
        if segX[0] == segX[i] and segY[0] == segY[i]:
            running = False
    return running

def checkTimer():
    running = True
    if sec == 0:
        running = False
    return running

def spawnApple():
    for i in range(len(nom)):
        if nom[i]:
            pygame.draw.circle(gameWindow,RED,(applesX[i],applesY[i]),SEGMENT_R,outline)
    return nom

def drawAppleX():
    appX = randint(0, WIDTH/HSTEP - 1)
    appleX = appX * HSTEP + SEGMENT_R
    return appleX

def drawAppleY():
    appY = randint(0, (HEIGHT - 100)/VSTEP - 1)
    appleY = appY * VSTEP + SEGMENT_R
    return appleY

def snakeSpeed():
    if (len(eatenApples)) % 5 == 0:
        FPSIncrease = 2
    else:
        FPSIncrease = 0
    return FPSIncrease

    
    

#---------------------------------------#
# main program                          #
#---------------------------------------#
print ("Use the arrows keys to move")
print ("Eat as many apples as you can before the time runs out")

# snake's properties
SEGMENT_R = 10
HSTEP = 20
VSTEP = 20
stepX = 0
stepY = -VSTEP                         # initially the snake moves upwards
segX = [MIDDLE - SEGMENT_R]
segY = [BOTTOM - 100 - VSTEP*3 - SEGMENT_R]

# apple properties
applesX = [drawAppleX()]
applesY = [drawAppleY()]
nom = [True]
eatenApples = []

score = 0
totalSec = 60
sec = 60


for i in range(3):                      # add coordinates for the head and 3 segments
    segX.append(MIDDLE - SEGMENT_R)
    segY.append(BOTTOM - 100 - SEGMENT_R*2*3)

# time properties 
clock = pygame.time.Clock()
BEGIN_CLOCK = pygame.time.get_ticks()
BEGIN_APPLE = time.time()
PERIOD = 5
referenceTime = BEGIN_APPLE
FPS = 10

#---------------------------------------#

while noCollision() and borders() and checkTimer():
    elapsedClock = pygame.time.get_ticks() - BEGIN_CLOCK
    sec = totalSec - round(elapsedClock/1000)
    
    drawGrid(SEGMENT_R * 2)
    drawSnake()
    spawnApple()
    pygame.display.update()
    clock.tick(FPS)
    pygame.event.clear()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_LEFT] and stepX != HSTEP:
        stepX = -HSTEP
        stepY = 0
    elif keys[pygame.K_RIGHT] and stepX != -HSTEP:
        stepX = HSTEP
        stepY = 0
    elif keys[pygame.K_UP] and stepY != VSTEP:
        stepX = 0
        stepY = -VSTEP
    elif keys[pygame.K_DOWN] and stepY != -VSTEP:
        stepX = 0
        stepY = VSTEP

# move the segments
    lastIndex = len(segX)-1
    for i in range(lastIndex,0,-1):     # starting from the tail, and going backwards:
        segX[i]=segX[i-1]               # every segment takes the coordinates
        segY[i]=segY[i-1]               # of the previous one
# move the head
    segX[0] = segX[0] + stepX
    segY[0] = segY[0] + stepY

# detects if apple is eaten 
    for i in range(len(nom)):
        if nom[i] and segX[0] == applesX[i] and segY[0] == applesY[i]:
            nom.append(True)
            nom[i] = False
            applesX.append(drawAppleX())
            applesY.append(drawAppleY())
            eatenApples.append(nom[i])
            segX.append(segX[-1])  # if snake ate the apple, add a segment:        
            segY.append(segY[-1])
            score = score + 1
            FPS = FPS + snakeSpeed()
            
    elapsedApple = round(time.time() - referenceTime,1)
    if elapsedApple > PERIOD:
        nom.append(True)
        applesX.append(drawAppleX())
        applesY.append(drawAppleY())
        spawnApple()
        referenceTime = time.time()

            


#---------------------------------------#    
pygame.quit()
