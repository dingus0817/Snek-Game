###########################
#File name: SnekV5.2.py
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
DARK_GREEN = (0,150,0)
RED = (255,0,0)
BLUE = (0,0,255)
outline=0

# loaded images and audio
APPLE = pygame.image.load("../SnekImages/snek_apple.png")
smallApple = pygame.transform.scale(APPLE,(30,30))
bigApple = pygame.transform.scale(APPLE,(80,80))
hourglass = pygame.image.load("../SnekImages/snek_hourglass.png")
hourglass = pygame.transform.scale(hourglass,(90,90))
NOM_SOUND = pygame.mixer.Sound("../SnekAudio/snek_nom.wav")
NOM_SOUND.set_volume(1)


#---------------------------------------#
# functions                             #
#---------------------------------------#
##def redrawGameWindow():
##    gameWindow.fill(BLACK)

def drawGrid(gridSize,sec):
    gameWindow.fill(BLACK)
    pygame.draw.rect(gameWindow,BLUE,(0,600,WIDTH,100),outline)
    for x in range(0,WIDTH,gridSize):
        pygame.draw.line(gameWindow, BLUE, (x,0),(x,HEIGHT),1)
    for y in range(0,HEIGHT,gridSize):
        pygame.draw.line(gameWindow, BLUE, (0,y),(WIDTH,y),1)
    scoreText = font.render(str(score),1,WHITE)
    timerText = font.render(str(sec),1,WHITE)
    gameWindow.blit(scoreText,(120,610))
    gameWindow.blit(timerText,(680,610))
    gameWindow.blit(bigApple,(20,610))
    gameWindow.blit(hourglass,(580,610))

def drawSnake(x,y):
    for i in range(len(segX)-1):
        pygame.draw.circle(gameWindow, segCLR, (segX[i], segY[i]), SEGMENT_R, outline)
    pygame.draw.circle(gameWindow,segCLR,(tailX,tailY),SEGMENT_R//1.5,outline)
    pygame.draw.rect(gameWindow,headCLR,(segX[0] - SEGMENT_R, segY[0] - SEGMENT_R,SEGMENT_R*2,SEGMENT_R*2), outline)
    pygame.draw.circle(gameWindow,WHITE,(segX[0] + x,segY[0] + y),8,outline)
    pygame.draw.circle(gameWindow,WHITE,(segX[0] - x,segY[0] - y),8,outline)
    pygame.draw.circle(gameWindow,BLACK,(segX[0] + x,segY[0] + y),5,outline)
    pygame.draw.circle(gameWindow,BLACK,(segX[0] - x,segY[0] - y),5,outline)

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
            gameWindow.blit(smallApple,(applesX[i] - 15,applesY[i] - 15))
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

def spawnObstacle():
    for i in range(len(obstaclesX)):
        pygame.draw.rect(gameWindow,WHITE,(obstaclesX[i]-SEGMENT_R,obstaclesY[i]-SEGMENT_R,20,20),outline)

def drawObstacleX():
    randomObstacle = randint(0, WIDTH/(HSTEP*2) - 1)
    obstacleX = randomObstacle * HSTEP * 2 + SEGMENT_R
    return obstacleX

def drawObstacleY():
    randomObstacle = randint(0, (HEIGHT - 100)/(VSTEP*2) - 1)
    obstacleY = randomObstacle * VSTEP * 2 + SEGMENT_R
    return obstacleY
    

    
    

    
    

#---------------------------------------#
# main program                          #
#---------------------------------------#
print ("Use the arrows keys to move")
print ("Eat as many apples as you can before the time runs out")

# snake's properties
headCLR = GREEN
segCLR = DARK_GREEN
SEGMENT_R = 10
HSTEP = 20
VSTEP = 20
stepX = 0
stepY = -VSTEP                         # initially the snake moves upwards
segX = [MIDDLE - SEGMENT_R]
segY = [BOTTOM - 100 - VSTEP*3 - SEGMENT_R]
tailX = segX[0]
tailY = segY[0]
eyes = [0,8]
eyeX = eyes[1]
eyeY = eyes[0]

for i in range(3):                      # add coordinates for the head and 3 segments
    segX.append(MIDDLE - SEGMENT_R)
    segY.append(BOTTOM - 100 - SEGMENT_R*2*3)

print(MIDDLE - SEGMENT_R)

# apple properties
applesX = [drawAppleX()]
applesY = [drawAppleY()]
nom = [True]
eatenApples = []

# obstacle properties
obstaclesX = []
obstaclesY = []
for i in range(20):
    obstaclesX.append(drawObstacleX())
    obstaclesY.append(drawObstacleY())

score = 0
count = 0
totalSec = 60 
sec = ""

font = pygame.font.SysFont("Arial",80)

# time properties 
clock = pygame.time.Clock()
BEGIN_CLOCK = pygame.time.get_ticks()
BEGIN_APPLE = time.time()
PERIOD = 5
referenceTime = BEGIN_APPLE
begin_time = time.time()
ref_time = begin_time
#start_time = 0
nom_timer = False
elapsed_nom = 0
FPS = 10

#---------------------------------------#

while noCollision() and borders() and checkTimer():
    pygame.event.pump()
    elapsedClock = pygame.time.get_ticks() - BEGIN_CLOCK
    sec = totalSec - round(elapsedClock/1000)
    
    drawGrid(SEGMENT_R * 2,sec)
    drawSnake(eyeX,eyeY)
    spawnObstacle()
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
        eyeX = eyes[0]
        eyeY = eyes[1]
    elif keys[pygame.K_RIGHT] and stepX != -HSTEP:
        stepX = HSTEP
        stepY = 0
        eyeX = eyes[0]
        eyeY = eyes[1]
    elif keys[pygame.K_UP] and stepY != VSTEP:
        stepX = 0
        stepY = -VSTEP
        eyeX = eyes[1]
        eyeY = eyes[0]
    elif keys[pygame.K_DOWN] and stepY != -VSTEP:
        stepX = 0
        stepY = VSTEP
        eyeX = eyes[1]
        eyeY = eyes[0]

# move the segments
    lastIndex = len(segX)-1
    for i in range(lastIndex,0,-1):     # starting from the tail, and going backwards:
        segX[i]=segX[i-1]               # every segment takes the coordinates
        segY[i]=segY[i-1]               # of the previous one
        tailX = segX[lastIndex]
        tailY = segY[lastIndex] 
# move the head
    segX[0] = segX[0] + stepX
    segY[0] = segY[0] + stepY

    begin_time = time.time()
    ref_time = begin_time
    start_time = 0 
# detects if apple is eaten
    for i in range(len(nom)):
        if nom[i] and segX[0] == applesX[i] and segY[0] == applesY[i]:
            count = count + 1
            NOM_SOUND.play()
            nom[i] = False
            segX.append(segX[-1])  # if snake ate the apple, add a segment:        
            segY.append(segY[-1])
            eatenApples.append(nom[i])
            score = score + 1
            FPS = FPS + snakeSpeed()
            nom.append(True)
            applesX.append(drawAppleX())
            applesY.append(drawAppleY())
            
    if count == 1:
        nom_timer = True
        import SnekV5TimeBoost as timeBoost
        elapsed_nom = timeBoost.boostTime()
    if count == 2:
        print(elapsed_nom, "seconds in total")
        count = 0
        totalSec = totalSec + 10
##    
##        #elapsed_nom = time.time() - begin_time
##        #print(elapsed_nom, "seconds")
##
##            #ref_time = time.time()


    elapsedApple = round(time.time() - referenceTime,1)
    if elapsedApple > PERIOD:
        nom.append(True)
        applesX.append(drawAppleX())
        applesY.append(drawAppleY())
        spawnApple()
        referenceTime = time.time()

            


#---------------------------------------#    
pygame.quit()
