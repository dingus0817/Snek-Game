from random import randint
import pygame
pygame.init()
WIDTH = 800
HEIGHT= 600
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))

TOP = 0
BOTTOM = HEIGHT
MIDDLE = int(WIDTH/2.0)
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
GREEN = (0,255,0)
outline=0

headCLR = GREEN
segCLR = WHITE

#---------------------------------------#
# functions                             #
#---------------------------------------#
##def redrawGameWindow():
##    gameWindow.fill(BLACK)

def drawSnake():
    for i in range(len(segX)): 
        pygame.draw.circle(gameWindow, segCLR, (segX[i], segY[i]), SEGMENT_R, outline)
    pygame.draw.circle(gameWindow,headCLR,(segX[0], segY[0]), SEGMENT_R, outline)
    pygame.display.update()

def collision():
     headRect = pygame.Rect(0,0,SEGMENT_R*2,SEGMENT_R*2)
     headCirc = pygame.draw.circle(gameWindow,headCLR,(segX[0], segY[0]), SEGMENT_R, outline)
     headRect.center = headCirc.center 

#---------------------------------------#
# main program                          #
#---------------------------------------#
print ("Use the arrows and the space bar.")
print ("Hit ESC to end the program.")

# snake's properties
SEGMENT_R = 10
HSTEP = 15
VSTEP = 15
stepX = 0
stepY = -VSTEP                         # initially the snake moves upwards
segX = []
segY = []
for i in range(4):                      # add coordinates for the head and 3 segments
    segX.append(MIDDLE)
    segY.append(BOTTOM + i*VSTEP)

clock = pygame.time.Clock()
FPS = 24
    
#---------------------------------------#
inPlay = True
while inPlay:
    gameWindow.fill(BLACK)
    drawSnake()
    clock.tick(FPS)

    pygame.event.clear()
    keys = pygame.key.get_pressed()
    prevKey = keys
    if keys[pygame.K_ESCAPE]:
        inPlay = False
    if keys[pygame.K_LEFT] and stepX != HSTEP:
        stepX = -HSTEP
        stepY = 0
    if keys[pygame.K_RIGHT] and stepX != -HSTEP:
        stepX = HSTEP
        stepY = 0
    if keys[pygame.K_UP] and stepY != VSTEP:
        stepX = 0
        stepY = -VSTEP
    if keys[pygame.K_DOWN] and stepY != -VSTEP:
        stepX = 0
        stepY = VSTEP
    if keys[pygame.K_SPACE]:            # if space bar is pressed, add a segment:
        segX.append(segX[-1])           # assign it the same x and y coordinates
        segY.append(segY[-1])           # as those of the last segment

# move the segments
    lastIndex = len(segX)-1
    for i in range(lastIndex,0,-1):     # starting from the tail, and going backwards:
        segX[i]=segX[i-1]               # every segment takes the coordinates
        segY[i]=segY[i-1]               # of the previous one
# move the head
    segX[0] = segX[0] + stepX
    segY[0] = segY[0] + stepY



#---------------------------------------#    
pygame.quit()
