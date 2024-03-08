#File name: SnekV6Init.py


from random import randint
import time
import pygame

# snake properties
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
