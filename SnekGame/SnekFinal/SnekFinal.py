###########################
# File name: SnekFinal.py
# Author: Jamie Zhang
##########################

from random import randint
import pygame
import time
pygame.init()
WIDTH = 800
HEIGHT= 700
gameWindow = pygame.display.set_mode((WIDTH,HEIGHT))
 
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
snek1 = pygame.image.load("SnekImages/snek_snek1.png")
snek1 = pygame.transform.scale(snek1,(400,400))
snek2 = pygame.image.load("SnekImages/snek_snek2.png")
snek2 = pygame.transform.scale(snek2,(400,400))
APPLE = pygame.image.load("SnekImages/snek_apple.png")
smallApple = pygame.transform.scale(APPLE,(30,30))
bigApple = pygame.transform.scale(APPLE,(80,80))
hourglass = pygame.image.load("SnekImages/snek_hourglass.png")
hourglass = pygame.transform.scale(hourglass,(90,90))
clockImg = pygame.image.load("SnekImages/snek_clock.png")
clockImg = pygame.transform.scale(clockImg,(150,150))
trophy = pygame.image.load("SnekImages/snek_trophy.png")
trophy = pygame.transform.scale(trophy,(90,90))
FECES = pygame.image.load("SnekImages/snek_obstacle.png")
FECES = pygame.transform.scale(FECES,(40,40))
leaf = pygame.image.load("SnekImages/snek_leaf.png")
leaf = pygame.transform.scale(leaf,(35,35))
night = pygame.image.load("SnekImages/snek_night.png")
night = pygame.transform.scale(night,(550,330))
sunday = pygame.image.load("SnekImages/snek_sunday.png")
sunday = pygame.transform.scale(sunday,(550,330))
feelBetter = pygame.image.load("SnekImages/snek_sunday2.png")
feelBetter = pygame.transform.scale(feelBetter,(550,330))
timeskip = pygame.image.load("SnekImages/snek_grownup.png")
timeskip = pygame.transform.scale(timeskip,(550,330))
coma = pygame.image.load("SnekImages/snek_coma.png")
coma = pygame.transform.scale(coma,(550,330))
finalForm = pygame.image.load("SnekImages/snek_butterfly.png")
finalForm = pygame.transform.scale(finalForm,(550,330))
NOM_SOUND = pygame.mixer.Sound("SnekAudio/snek_nom.wav")
NOM_SOUND.set_volume(1)
TIME_SOUND = pygame.mixer.Sound("SnekAudio/snek_timeIncrease.wav")
TIME_SOUND.set_volume(1)
OOF_SOUND = pygame.mixer.Sound("SnekAudio/snek_oofDeath.wav")
OOF_SOUND.set_volume(3)
HIT_SOUND = pygame.mixer.Sound("SnekAudio/snek_collisionDeath.wav")
HIT_SOUND.set_volume(3)
WOW_SOUND = pygame.mixer.Sound("SnekAudio/snek_victoryWow.wav")
WOW_SOUND.set_volume(5)

# fonts
scoreboardFont = pygame.font.SysFont("Courier New",80)
titleFont = pygame.font.SysFont("Courier New",100)
bigFont = pygame.font.SysFont("Courier New",65)
medFont = pygame.font.SysFont("Courier New",25)
smallFont = pygame.font.SysFont("Courier New",18)

#---------------------------------------#
# functions                             #
#---------------------------------------#

def drawMenu():     # draws the menu screen
    gameWindow.fill(BLACK)
    pygame.draw.rect(gameWindow,BLUE,(25,25,750,650),5)
    titleText = titleFont.render("snek",1,GREEN)
    introText1 = medFont.render("use the arrows keys to move",1,WHITE)
    introText2 = medFont.render("eat as many apples as you can",1,WHITE)
    playText = medFont.render("press and hold SPACE to play",1,WHITE)
    quitText = medFont.render("press and hold ESC to quit",1,WHITE)
    hintText = smallFont.render("* try eating 2 apples in 2 seconds!",1,LIGHT_BLUE)
    gameWindow.blit(titleText,(100,70))
    gameWindow.blit(introText1,(100,180))
    gameWindow.blit(introText2,(100,210))
    gameWindow.blit(playText,(70,350))
    gameWindow.blit(quitText,(70,500))
    gameWindow.blit(hintText,(40,630))

def menuSnekInterval():    # tracking the intervals between snake images in menu
    global snekPeriod,BEGIN_SNEK,refTime
    snekPeriod = 0.5
    BEGIN_SNEK = time.time()
    refTime = BEGIN_SNEK

def initGame():     # game properties 
    global headCLR,segCLR,SEGMENT_R,HSTEP,VSTEP,stepX,stepY,segX,segY,tailX,tailY,eyes,eyeX,eyeY
    global applesX,applesY,nom,leafX,leafY
    global obstaclesX,obstaclesY,score,consecutiveApples,totalSec,sec
    global clock,BEGIN_CLOCK,BEGIN_APPLE,PERIOD_GAME,period_time,referenceTime,begin_time,FPS

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
    for i in range(3):                    # add coordinates for the head and 3 segments
        segX.append(MIDDLE - SEGMENT_R)
        segY.append(BOTTOM - 100 - SEGMENT_R*2*3)

    # apple properties
    applesX = [drawAppleX()]
    applesY = [drawAppleY()]
    nom = [True]         # determines whether to draw apple

    # obstacle properties
    obstaclesX = []
    obstaclesY = []
    for i in range(20):
        obstaclesX.append(drawObstacleX())
        obstaclesY.append(drawObstacleY())

    leafX = drawAppleX()
    leafY = drawAppleY()

    # resetting features
    score = 0
    consecutiveApples = 0
    totalSec = 30
    sec = ""

    # time properties 
    clock = pygame.time.Clock()
    BEGIN_CLOCK = pygame.time.get_ticks()  # starts the clock for the main game
    BEGIN_APPLE = time.time()         # starts the clock for intervals of 5 
    PERIOD_GAME = 5
    period_time = 2
    referenceTime = BEGIN_APPLE
    begin_time = time.time()    # starts the clock to check if 2 apples have been eaten in under 2 seconds
    FPS = 10

def drawGrid(gridSize,sec):     # draw the game grid
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

def drawSnake(x,y):       # draw the snake
    for i in range(len(segX)-1):
        pygame.draw.circle(gameWindow, segCLR, (segX[i], segY[i]), SEGMENT_R, outline)
    pygame.draw.circle(gameWindow,segCLR,(tailX,tailY),SEGMENT_R//1.5,outline)
    pygame.draw.rect(gameWindow,headCLR,(segX[0] - SEGMENT_R, segY[0] - SEGMENT_R,SEGMENT_R*2,SEGMENT_R*2), outline)
    pygame.draw.circle(gameWindow,WHITE,(segX[0] + x,segY[0] + y),8,outline)
    pygame.draw.circle(gameWindow,WHITE,(segX[0] - x,segY[0] - y),8,outline)
    pygame.draw.circle(gameWindow,BLACK,(segX[0] + x,segY[0] + y),5,outline)
    pygame.draw.circle(gameWindow,BLACK,(segX[0] - x,segY[0] - y),5,outline)

# ------ check and run the game if these conditions are true ----- #
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
# ---------------------------------------------- #

def snakeSpeed():      # increase snake speed every 5 apples eaten 
    if score % 5 == 0:
        FPSIncrease = 2
    else:
        FPSIncrease = 0
    return FPSIncrease

# ----------------- get random coordinates ----------------- #
def drawAppleX():   
    foodX = randint(0, WIDTH/HSTEP - 1)
    appleX = foodX * HSTEP + SEGMENT_R
    return appleX

def drawAppleY():
    foodY = randint(0, (HEIGHT - 100)/VSTEP - 1)
    appleY = foodY * VSTEP + SEGMENT_R
    return appleY

def drawObstacleX():
    randomObstacle = randint(0, WIDTH/(HSTEP*2) - 1)
    obstacleX = randomObstacle * HSTEP * 2 + SEGMENT_R
    return obstacleX

def drawObstacleY():
    randomObstacle = randint(0, (HEIGHT - 100)/(VSTEP*2) - 1)
    obstacleY = randomObstacle * VSTEP * 2 + SEGMENT_R
    return obstacleY
# -------------------------------------------------------------- #

def spawnApple():       # draw apples 
    for i in range(len(obstaclesX)):      # if apple spawns in the same position as the obstacle
        for appleIndex in range(len(applesX)):
            if nom[appleIndex] and applesX[appleIndex] == obstaclesX[i] and applesY[appleIndex] == obstaclesY[i]:
                nom[appleIndex] = False      # don't draw that apple
                applesX.append(drawAppleX())
                applesY.append(drawAppleY())
                nom.append(True)            # draw another apple 
    for i in range(len(nom)):
        if nom[i]:
            gameWindow.blit(smallApple,(applesX[i] - 15,applesY[i] - 15))                        
    return nom

def spawnLeaf():  ############ --------- the leaf triggers the secret ending -------- ##############
    global leafSecret, leafX, leafY
    leafSecret = False
    if score == 25:     ########## the leaf only spawns after 25 apples are eaten
        leafSecret = True                
    if leafSecret:
        for i in range(len(obstaclesX)):
            if leafX == obstaclesX[i] and leafY == obstaclesY[i]:
                leafX = drawAppleX()
                leafY = drawAppleY()
        gameWindow.blit(leaf,(leafX - 17,leafY - 17))
    return leafSecret    ################## ----------------------------------- ##################

def spawnObstacle():    # draw obstacles 
    for i in range(len(obstaclesX)):
        gameWindow.blit(FECES,(obstaclesX[i] - 20,obstaclesY[i] - 20))

def playMusic(event_type):      # play the appropriate music
    global eventType
    backgroundMusic = "SnekAudio/snek_theme.wav"
    eventType = event_type
    if event_type == "dead":
        backgroundMusic = "SnekAudio/snek_gameOver_undertale.wav"
    elif event_type == "butterfly":
        backgroundMusic = "SnekAudio/snek_secretMusic_knb.wav"
    pygame.mixer.music.load(backgroundMusic)
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops = -1)

def drawGameOver():         # draw the game over screen
    pygame.draw.rect(gameWindow,BLACK,(50,50,700,600),outline)
    pygame.draw.rect(gameWindow,DARK_GREEN,(70,70,660,560),5)
    gameOverText = bigFont.render(endingText,1,WHITE)
    ggText = medFont.render(postGameText,1,LIGHT_BLUE)
    scoreText = scoreboardFont.render(str(score),1,DARK_GREEN)
    timeText = scoreboardFont.render(str(round(elapsedClock/1000)),1,DARK_GREEN)
    bestScoreText = scoreboardFont.render(str(bestScore),1,DARK_GREEN)
    playAgainText = medFont.render("press SPACE to play again",1,WHITE)
    mainMenuText = medFont.render("press RETURN for main menu",1,WHITE)
    specialText = smallFont.render(loreText,1,LIGHT_BLUE)
    gameWindow.blit(gameOverText,(120,100))
    gameWindow.blit(ggText,(130,200))
    gameWindow.blit(bigApple,(120,300))
    gameWindow.blit(scoreText,(220,300))
    gameWindow.blit(clockImg,(80,390))
    gameWindow.blit(timeText,(220,430))
    gameWindow.blit(bestScoreText,(580,270))
    gameWindow.blit(trophy,(480,270))
    gameWindow.blit(playAgainText,(310,390))
    gameWindow.blit(mainMenuText,(310,520))
    gameWindow.blit(specialText,(100,600))

# ------------------------------- draw the secret ending cutscene ----------------------- #
def drawSecret():   
    global inEnding
    timer = pygame.time.Clock()
    FPS_WORDS = 60
    counter = 0         # keeps track of the number of characters in the message 
    speed = 2           # draws 30 characters per second 
    messages = ["that night, the snek had a stomachache from eating too many apples.",
                "the next day was Sunday. The snek ate one nice green leaf.",
                "after that, he felt much better.",
                "the snek wasn't hungry anymore, and he wasn't a little snek anymore.",
                "he was a big long snek, and he went into a food coma for two weeks.",
                "when he woke up again, he was a beautiful butterfly!"]
    images = [night,sunday,feelBetter,timeskip,coma,finalForm]
    snip = smallFont.render("",1,WHITE)
    activeMessage = 0
    activeImage = 0
    message = messages[activeMessage]
    image = images[activeImage]
    done = False

    running = True
    while running:
        gameWindow.fill(BLACK)
        timer.tick(FPS_WORDS)
        
        # ----- check if the whole message has been written on the screen --- #
        if counter < speed * len(message):   
            counter = counter + 1
        elif counter >= speed * len(message):
            done = True    # flags when message is done
            continueText = smallFont.render("press RIGHT SHIFT to continue ->",1,WHITE)
            gameWindow.blit(continueText,(420,650))
        # ------------------------------- #
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT and done and activeMessage < len(messages) - 1:
                    activeMessage = activeMessage + 1    
                    activeImage = activeImage + 1
                    done = False
                    message = messages[activeMessage]
                    image = images[activeImage]
                    counter = 0
                
                elif event.key == pygame.K_RSHIFT and done and activeMessage == len(messages) - 1:
                    running = False
                    
        snip = smallFont.render(message[0:counter//speed],1,WHITE)   # end position of the characters change
                                                                    # when the counter is divisible by the speed (2)
        gameWindow.blit(snip,(10,500))
        gameWindow.blit(image,(125,50))
        pygame.display.flip()
# ---------------------------------------------------------------------- #
    
#---------------------------------------#
# main program                          #
#---------------------------------------#
playMusic("alive")
menuSnekInterval()
bestScore = 0

inPlay = True
inMenu = True
inGame = False
postGame = False
leafEaten = False

while inPlay:
    # ------------- # MENU # ----------------- #
    while inMenu:
        pygame.event.pump()
        drawMenu()
        
        elapsedSnek = round(time.time() - refTime,1)
        if elapsedSnek > snekPeriod:      # draws animated snake
            gameWindow.blit(snek1,(400,260))
            refTime = time.time()
        else:
            gameWindow.blit(snek2,(400,260))
            pygame.time.delay(500)

        pygame.display.update()
        pygame.event.clear()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            inMenu = False
            inGame = True
            leafEaten = False
            initGame()
        elif keys[pygame.K_ESCAPE]:
            inPlay = False
            inMenu = False
    # ----------------------------------------- #
    
    # --------------------- GAME -------------------------#    
    while inGame and checkBorders() and noCollision() and checkTimer() and checkObstacles() and not leafEaten:
        pygame.event.pump()
        elapsedClock = pygame.time.get_ticks() - BEGIN_CLOCK  # start the clock
        sec = totalSec - round(elapsedClock/1000)
        
        drawGrid(SEGMENT_R * 2,sec)
        spawnObstacle()
        drawSnake(eyeX,eyeY)
        spawnApple()
        spawnLeaf()
        pygame.display.update()
        
        clock.tick(FPS)
        pygame.event.clear()
        
        keys = pygame.key.get_pressed()  
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
                consecutiveApples = consecutiveApples + 1
                nom[i] = False
                segX.append(segX[-1])  # if snake ate the apple, add a segment:        
                segY.append(segY[-1])
                score = score + 1
                FPS = FPS + snakeSpeed()
                nom.append(True)           # draw new apple after previous one is eaten
                applesX.append(drawAppleX())
                applesY.append(drawAppleY())

                if consecutiveApples >= 2 and time.time() - begin_time <= period_time:
                    TIME_SOUND.play()
                    totalSec = totalSec + 5 # increase time by 5 seconds if 2 apples are eaten in under 2 seconds
                    consecutiveApples = 0
                else:
                    consecutiveApples = 1
                begin_time = time.time()

        # spawns random apple every 5 seconds
        elapsedApple = round(time.time() - referenceTime,1)
        if elapsedApple > PERIOD_GAME:
            nom.append(True)
            applesX.append(drawAppleX())
            applesY.append(drawAppleY())
            spawnApple()
            referenceTime = time.time()
            
        # --------- determines game over screen and which sound effect to play -------- #
        if not checkBorders() or not noCollision():
            pygame.mixer.music.stop()
            HIT_SOUND.play()
            pygame.time.delay(1000)
            playMusic("dead")
            endingText = "HOSPITAL ENDING"
            postGameText = "ouch."
            loreText = "* hope you have health insurance"
            postGame = True

        elif not checkObstacles():
            pygame.mixer.music.pause()
            OOF_SOUND.play()
            pygame.time.delay(1000)
            playMusic("dead")
            endingText = "BAD ENDING"
            postGameText = "oof. that's rough, buddy"
            loreText = "* hm. wonder where all these turds came from anyway..."
            postGame = True

        elif not checkTimer():
            pygame.mixer.music.pause()
            WOW_SOUND.play()
            pygame.time.delay(1000)
            endingText = "GOOD ENDING"
            postGameText = "wow!"
            loreText = "* you can go home safely! or try going for 25 apples..."
            postGame = True

        elif leafSecret and segX[0] == leafX and segY[0] == leafY:
            leafEaten = True
            pygame.mixer.music.stop()
            NOM_SOUND.play()
            pygame.time.delay(1000)
            playMusic("butterfly")
            drawSecret()
            endingText = "SECRET ENDING"
            postGameText = "sneks can metamorphosize too!"
            loreText = "* the real name of the game is 'the very hungry snek'!"
            postGame = True
        # -----------------------------#
    # ---------------------------------------#
            
    # ------------- GAME OVER ------------#
    while postGame:
        pygame.event.pump()
        if score > bestScore:   # store the high score  
            bestScore = score
            
        pygame.mixer.music.unpause()
        drawGameOver()
        pygame.display.update()
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if eventType != "alive":
                playMusic("alive")
            initGame()
            postGame = False
            leafEaten = False
            inGame = True
        if keys[pygame.K_RETURN]:
            if eventType != "alive":
                playMusic("alive")
            postGame = False
            inMenu = True
        
    # --------------------------------#
#---------------------------------------#    
pygame.quit()
