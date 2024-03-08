import pygame
pygame.init()
smallFont = pygame.font.SysFont("Courier New",18)
WIDTH = 800
HEIGHT = 700
gameWindow = pygame.display.set_mode((WIDTH,HEIGHT))
WHITE = (255,255,255)
BLACK = (0,0,0)
timer = pygame.time.Clock()
FPS_WORDS = 60
messages = ["that night, the snek had a stomachache from eating too many apples.",
            "the next day was Sunday. The snek ate one nice green leaf.",
            "after that, he felt much better.",
            "the snek wasn't hungry anymore, and he wasn't a little snek anymore.",
            "he was a big long snek, and he went into a food coma for two weeks.",
            "when he woke up again...",
            "he was a beautiful butterfly!"
            ]
snip = smallFont.render("",1,WHITE)
counter = 0
speed = 2
activeMessage = 0
message = messages[activeMessage]
done = False

running = True
while running:
    gameWindow.fill(BLACK)
    timer.tick(FPS_WORDS)
    if counter < speed * len(message):
        counter = counter + 1
    elif counter >= speed * len(message):
        done = True
        continueText = smallFont.render("press SPACE to continue ->",1,WHITE)
        gameWindow.blit(continueText,(480,650))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and done and activeMessage < len(messages):
                activeMessage = activeMessage + 1
                done = False
                message = messages[activeMessage]
                counter = 0
                

    snip = smallFont.render(message[0:counter//speed],1,WHITE)
    gameWindow.blit(snip,(10,500))

    pygame.display.flip()
pygame.quit()
