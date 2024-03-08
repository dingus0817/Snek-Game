###########################
#File name: SnekV4.py
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

def nomCheck():
    global nommed
    nommed = True
    #print(count)
    BEGIN_NOM = time.time()
    if nommed:
        
        start_time = time.time() - BEGIN_NOM
        #testSec = 2 - start_time/1000
        if count == 2 and start_time < 2:
            secIncrease = 10
        else:
            secIncrease = 0
    #nommed = False
    return secIncrease

def nomTimer():
    global nommed
    
    

    
    

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

# apple properties
applesX = [drawAppleX()]
applesY = [drawAppleY()]
nom = [True]
eatenApples = []
nommed = False

score = 0
count = 0
totalSec = 60 
sec = ""
testSec = ""

font = pygame.font.SysFont("Arial",80)

# time properties 
clock = pygame.time.Clock()
BEGIN_CLOCK = pygame.time.get_ticks()
BEGIN_APPLE = time.time()
PERIOD = 5
referenceTime = BEGIN_APPLE
FPS = 10

#---------------------------------------#

while noCollision() and borders() and checkTimer():
    pygame.event.pump()
    elapsedClock = pygame.time.get_ticks() - BEGIN_CLOCK
    sec = totalSec - round(elapsedClock/1000)
    
    drawGrid(SEGMENT_R * 2,sec)
    drawSnake(eyeX,eyeY)
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

    #start_time=""
    #start_time = time.time()
# detects if apple is eaten
    for i in range(len(nom)):
        if nom[i] and segX[0] == applesX[i] and segY[0] == applesY[i]:
            #start_time = pygame.time.get_ticks() - BEGIN_CLOCK 
            #testSec = 2 - start_time/1000
            #start_time = time.time()
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
            nommed = True
            ref_time = time.time()
            print(nommed)
##            sec = sec + nomCheck()
##            print(nomCheck())
##            PERIOD_NOM = 2
##            BEGIN_NOM = pygame.time.get_ticks()
##            elapsedNom = pygame.time.get_ticks() - BEGIN_NOM
##            if nom[i] and segX[0] == applesX[i] and segY[0] == applesY[i] and elapsedNom < PERIOD_NOM:
##                sec = sec + 3
##                elapsedNom = pygame.time.get_ticks()
        #print("xxxx", pygame.time.get_ticks() - BEGIN_CLOCK) 
    #if count == 2 and time.time()-start_time <= 2:


##    if count == 2 and testSec > 0:
##        print("x")
        #totalSec = totalSec + 10
##        count = 0
##        start_time = pygame.time.get_ticks() - BEGIN_CLOCK
    begin_time = time.time()
    ref_time = begin_time
    start_time = 0        
    end_time = False
    if nommed and count == 1:
        import SnekV5TimeBoost as timeBoost
        print(timeBoost.boostTime(nommed,count))
        secIncrease = timeBoost.boostTime(nommed,count)
        totalSec = totalSec + secIncrease

        
        start_time = round(time.time() - ref_time,1)
        print(start_time)
        if count == 2 and start_time <= 2:
            #end_time = True
            totalSec = totalSec + 10
            count = 0
            print("hi")

    if end_time and count == 2:
        totalSec = totalSec + 10
        count = 0
        nommed = False


    elapsedApple = round(time.time() - referenceTime,1)
    if elapsedApple > PERIOD:
        nom.append(True)
        applesX.append(drawAppleX())
        applesY.append(drawAppleY())
        spawnApple()
        referenceTime = time.time()

            


#---------------------------------------#    
pygame.quit()
