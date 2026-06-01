import os, sys, pygame, numpy, time, random
import functions_test as fc_t
sys.path.append("imgs/spr_test1")

# pygame setup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                  pygame.display.Info().current_h),
                                  pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 64)
plr = pygame.image.load("final_project/imgs/spr_test1.jpg")

# vars
running = True
fc = 0

# Grid variables
camPos = [0, 0]

while running:
    
    ### SCREEN WIPE ###
    screen.fill("purple")
    
    ### EVENTS ###
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    ### INPUT ###
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        camPos[0] -= 1
    if keys[pygame.K_w]:
        camPos[0] += 1
    if keys[pygame.K_a]:
        camPos[1] -= 1
    if keys[pygame.K_d]:
        camPos[1] += 1
    
    # Background
    # will do this later
    
    ### RENDER ###
    # Text
    fpsTest = font.render("frame " + str(fc), True, (0, 0, 0))
    gridText = font.render("pos: " + str(camPos), True, (0, 0, 0))
    # Sprite
    
    # later use class and pygame.sprite.Sprite.__init__() to get all the attributes of a sprite
    
    # Incrementaal
    fc += 1
    
    # Blit
    screen.blit(fpsTest, (0, 0))
    screen.blit(gridText, fc_t.scale_to_pixel((0.25, 0.25)))
    screen.blit(plr, fc_t.scale_to_pixel((0.5, 0.5)))
    
    # flip() display
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60