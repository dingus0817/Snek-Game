###########################
#File name: SnekV6.py
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
BLUE = (0,0,255)
LIGHT_BLUE = (135,206,235)
outline=0

# loaded images and audio
APPLE = pygame.image.load("../SnekImages/snek_apple.png")
smallApple = pygame.transform.scale(APPLE,(30,30))
bigApple = pygame.transform.scale(APPLE,(80,80))
hourglass = pygame.image.load("../SnekImages/snek_hourglass.png")
hourglass = pygame.transform.scale(hourglass,(90,90))
clockImg = pygame.image.load("../SnekImages/snek_clock.png")
clockImg = pygame.transform.scale(clockImg,(150,150))
FECES = pygame.image.load("../SnekImages/snek_obstacle.png")
FECES = pygame.transform.scale(FECES,(40,40))
CONFETTI = pygame.image.load("../SnekImages/snek_confetti.png")
CONFETTI = pygame.transform.scale(CONFETTI,(WIDTH,HEIGHT))
NOM_SOUND = pygame.mixer.Sound("../SnekAudio/snek_nom.wav")
NOM_SOUND.set_volume(1)
TIME_SOUND = pygame.mixer.Sound("../SnekAudio/snek_timeIncrease.wav")
TIME_SOUND.set_volume(1.5)
OOF_SOUND = pygame.mixer.Sound("../SnekAudio/snek_oofDeath.wav")
OOF_SOUND.set_volume(2)
HIT_SOUND = pygame.mixer.Sound("../SnekAudio/snek_collisionDeath.wav")
HIT_SOUND.set_volume(2)
WOW_SOUND = pygame.mixer.Sound("../SnekAudio/snek_victoryWow.wav")
WOW_SOUND.set_volume(1)

# fonts
scoreboardFont = pygame.font.SysFont("Courier New",80)
titleFont = pygame.font.SysFont("Courier New",100)
meFont =  pygame.font.SysFont("Courier New",35)
smallFont = pygame.font.SysFont("Courier New",25)

#---------------------------------------#
# functions                             #
#---------------------------------------#

def drawMenu():
    gameWindow.fill(BLACK)
    titleText = titleFont.render("Snek",1,BLUE)
    gameWindow.blit(titleText,(100,70))

def drawGrid(gridSize,sec):
    gameWindow.fill(BLACK)
    pygame.draw.rect(gameWindow,BLUE,(0,600,WIDTH,100),outline)
    for x in range(0,WIDTH,gridSize):
        pygame.draw.line(gameWindow, BLUE, (x,0),(x,HEIGHT),1)
    for y in range(0,HEIGHT,gridSize):
        pygame.draw.line(gameWindow, BLUE, (0,y),(WIDTH,y),1)
    scoreText = scoreboardFont.render(str(score),1,WHITE)
    timerText = scoreboardFont.render(str(sec),1,WHITE)
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

def checkBorders():
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

def checkObstacles():
    running = True
    for i in range(len(obstaclesX)):
        if segX[0] == obstaclesX[i] and segY[0] == obstaclesY[i]:
            running = False
    return running

def spawnApple():
    for i in range(len(obstaclesX)):
        for appleIndex in range(len(applesX)):
            if nom[appleIndex] and applesX[appleIndex] == obstaclesX[i] and applesY[appleIndex] == obstaclesY[i]:
                nom[appleIndex] = False
                applesX.append(drawAppleX())
                applesY.append(drawAppleY())
                nom.append(True)
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
        gameWindow.blit(FECES,(obstaclesX[i] - 20,obstaclesY[i] - 20))

def drawObstacleX():
    randomObstacle = randint(0, WIDTH/(HSTEP*2) - 1)
    obstacleX = randomObstacle * HSTEP * 2 + SEGMENT_R
    return obstacleX

def drawObstacleY():
    randomObstacle = randint(0, (HEIGHT - 100)/(VSTEP*2) - 1)
    obstacleY = randomObstacle * VSTEP * 2 + SEGMENT_R
    return obstacleY

def playMusic(event_type):
    backgroundMusic = "../SnekAudio/snek_theme.wav"
    if event_type == "die":
        backgroundMusic = "../SnekAudio/snek_gameOver_undertale.wav"
    pygame.mixer.music.load(backgroundMusic)
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops = -1)

def drawGameOver():
    pygame.draw.rect(gameWindow,BLACK,(50,50,700,600),outline)
    pygame.draw.rect(gameWindow,DARK_GREEN,(70,70,660,560),5)
    gameOverText = titleFont.render("GAME OVER!",1,WHITE)
    ggText = meFont.render(postGameText,1,LIGHT_BLUE)
    scoreText = scoreboardFont.render(str(score),1,DARK_GREEN)
    timeText = scoreboardFont.render(str(round(elapsedClock/1000)),1,DARK_GREEN) 
    playAgainText = smallFont.render("press A to play again",1,WHITE)
    mainMenuText = smallFont.render("press RETURN for main menu",1,WHITE)
    gameWindow.blit(gameOverText,(120,100))
    gameWindow.blit(ggText,(130,200))
    gameWindow.blit(bigApple,(120,300))
    gameWindow.blit(scoreText,(220,300))
    gameWindow.blit(clockImg,(80,390))
    gameWindow.blit(timeText,(220,430))
    gameWindow.blit(playAgainText,(340,390))
    gameWindow.blit(mainMenuText,(310,520))
    if not checkTimer():
        gameWindow.blit(CONFETTI,(0,0))
    
    
    

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

# obstacle properties
obstaclesX = []
obstaclesY = []
for i in range(20):
    obstaclesX.append(drawObstacleX())
    obstaclesY.append(drawObstacleY())

score = 0
count = 0
totalSec = 30 
sec = ""

# time properties 
clock = pygame.time.Clock()
BEGIN_CLOCK = pygame.time.get_ticks()
BEGIN_APPLE = time.time()
PERIOD = 5
referenceTime = BEGIN_APPLE
FPS = 10
begin_time = time.time()

#---------------------------------------#

inPlay = True
inMenu = True
if checkBorders() and noCollision() and checkTimer() and checkObstacles():
    running = True
postGame = False

playMusic("alive")

while inPlay:
##    while inMenu:
##        pygame.event.pump()
##        drawMenu()
##        pygame.display.update()
    while checkBorders() and noCollision() and checkTimer() and checkObstacles():
        pygame.event.pump()
        elapsedClock = pygame.time.get_ticks() - BEGIN_CLOCK
        sec = totalSec - round(elapsedClock/1000)
        
        drawGrid(SEGMENT_R * 2,sec)
        spawnObstacle()
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

    # detects if apple is eaten
        
        for i in range(len(nom)):
            if nom[i] and segX[0] == applesX[i] and segY[0] == applesY[i]:
                NOM_SOUND.play()
                count = count + 1
                nom[i] = False
                segX.append(segX[-1])  # if snake ate the apple, add a segment:        
                segY.append(segY[-1])
                eatenApples.append(nom[i])
                score = score + 1
                FPS = FPS + snakeSpeed()
                nom.append(True)
                applesX.append(drawAppleX())
                applesY.append(drawAppleY())

                if count >= 2 and time.time() - begin_time <= 2:
                    TIME_SOUND.play()
                    totalSec = totalSec + 5
                    count = 0
                else:
                    count = 1
                begin_time = time.time()


        elapsedApple = round(time.time() - referenceTime,1)
        if elapsedApple > PERIOD:
            nom.append(True)
            applesX.append(drawAppleX())
            applesY.append(drawAppleY())
            spawnApple()
            referenceTime = time.time()

        if not checkBorders() or not noCollision():
            pygame.mixer.music.stop()
            HIT_SOUND.play()
            pygame.time.delay(1000)
            playMusic("die")
            postGameText = "ouch."
            postGame = True

        if not checkObstacles():
            pygame.mixer.music.pause()
            OOF_SOUND.play()
            pygame.time.delay(1000)
            playMusic("die")
            postGameText = "LOL THAT'S ROUGH, BUDDY"
            postGame = True

        if not checkTimer():
            pygame.mixer.music.pause()
            WOW_SOUND.play()
            pygame.time.delay(1000)
            postGameText = "wow!"
            postGame = True
            

    while postGame:
        pygame.event.pump()
        pygame.mixer.music.unpause()
        drawGameOver()
        pygame.display.update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            playMusic("alive")
            
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

            # obstacle properties
            obstaclesX = []
            obstaclesY = []
            for i in range(20):
                obstaclesX.append(drawObstacleX())
                obstaclesY.append(drawObstacleY())

            score = 0
            count = 0
            totalSec = 30 
            sec = ""

            # time properties 
            clock = pygame.time.Clock()
            BEGIN_CLOCK = pygame.time.get_ticks()
            BEGIN_APPLE = time.time()
            PERIOD = 5
            referenceTime = BEGIN_APPLE
            FPS = 10
            begin_time = time.time()

            postGame = False


            


#---------------------------------------#    
pygame.quit()
