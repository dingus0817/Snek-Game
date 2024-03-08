#File name: SnekV4TimeBoost.py
#Author: Jamie Zhang

import pygame
import time


def boostTime(eaten,num):
##    pygame.init()
##    WIDTH  = 300
##    HEIGHT = 100
##    gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))
##
##    BLACK = [  0,  0,  0]
##    GREY  = [192,192,192]
##    font = pygame.font.SysFont("Arial",36)
    
    clock = pygame.time.Clock()
    ##FPS = 24
    running = True

    PERIOD = 2
    BEGIN = time.time()
    referenceTime = BEGIN
    elapsed = 0

    while running:
##        gameWindow.fill(BLACK)
##        # the following two lines are for visualization purpose only
##        graphics = font.render(str(elapsed),1,GREY)
##        gameWindow.blit(graphics,(32,32))
##        #-----------------------------------------------------------
##        pygame.display.update()
##        clock.tick(FPS)

        #pygame.event.clear()
##        keys = pygame.key.get_pressed()
##        if keys[pygame.K_ESCAPE]:
##            running = False
##        if keys[pygame.K_SPACE]:
##            triggered = True
##            referenceTime = time.time() 
        
        if eaten:
            elapsed = round(time.time() - referenceTime,1)
            if num == 2 and elapsed > PERIOD:
                secIncrease = 10
                running = False
        else:
            secIncrease = 0

    #pygame.quit()
    return secIncrease


#print(boostTime(True,2))

    
