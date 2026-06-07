import os, sys, pygame, numpy, time, random
import functions_test as fc_t
import sprite as spr
import maps
from pathlib import Path

# Env Vars
GAME_DIR = Path(__file__).resolve().parent
IMG_DIR = GAME_DIR / "imgs"
MOVE_SPEED = 1
RENDER_W = 320
RENDER_H = 180

# pygame setup
pygame.init()
pygame.font.init()
pygame.display.set_caption("The Finals")
screen = pygame.display.set_mode((pygame.display.Info().current_w,
                                  pygame.display.Info().current_h),
                                  pygame.FULLSCREEN)
renderScreen = pygame.Surface((RENDER_W, RENDER_H))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 64)

# Sprite setup
sprWorldDrawList = []
sprUIDrawList = [] # later implement

charPlr = spr.GameSprite(str(IMG_DIR / "David" / "animStruct.json" ))
charTest = spr.GameSprite(str(IMG_DIR / "spr_test1.png"))
sprWorldDrawList.extend([charPlr, charTest])

theMap = maps.load_map("map_final_test_1.tmj")

# vars
running = True
fc = 0
camPos = [0, 0]
takeInput = True

# Current issues: Y grid values are inverted because screen space goes positive right and down, not sure if it's worth fixing

while running:
    
    ### SCREEN WIPE ###
    renderScreen.fill("purple")
    
    ### EVENTS ###
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    camPosOld = camPos
    charPlrOldPos = (charPlr.rect.centerx, charPlr.rect.centery)
    
    ### INPUT ###
    keys = pygame.key.get_pressed()
    if takeInput == True:
        if keys[pygame.K_s]:
            charPlr.rect.centery += MOVE_SPEED
        if keys[pygame.K_w]:
            charPlr.rect.centery -= MOVE_SPEED
        if keys[pygame.K_a]:
            charPlr.rect.centerx -= MOVE_SPEED
        if keys[pygame.K_d]:
            charPlr.rect.centerx += MOVE_SPEED
    
    ### COLLISION ###
    debugAreColliding = theMap.get_rect().colliderect(charPlr.rect)
    
    # Camera
    tempCamAdd = (RENDER_W / 2, RENDER_H / 2)
    camPos[0] = charPlr.rect.centerx - tempCamAdd[0]
    camPos[1] = charPlr.rect.centery - tempCamAdd[1]
    
    # Maps ._.
    
    ### RENDER ###
    # Text
    fpsTest = font.render("frame " + str(fc), True, (0, 0, 0))
    gridText = font.render("pos: " + str(camPos), True, (0, 0, 0))
    collisionText = font.render("colliding: " + str(debugAreColliding), True, (0, 0, 0))
    tickText = font.render("second: " + str(pygame.time.get_ticks() / 1000), True, (0, 0, 0))
    # Sprite
    # Update chars based off cam movement -- later change to a list or smth not just bob maybe
    if charPlrOldPos[0] > charPlr.rect.centerx:
        charPlr.update(fc, "left", "regular")
    elif charPlrOldPos[0] < charPlr.rect.centerx:
        charPlr.update(fc, "right", "regular")
    elif charPlrOldPos[1] > charPlr.rect.centery:
        charPlr.update(fc, "up", "regular")
    elif charPlrOldPos[1] < charPlr.rect.centery:
        charPlr.update(fc, "down", "regular")
    else:
        charPlr.update(fc, "idle", "regular")
    
    # Incrementaal
    fc += 1
    
    ### BLIT ###
    ## Render Screen ##
    # Map
    renderScreen.blit(theMap, (-camPos[0], -camPos[1]))
    # Sprite - we are doing a loop & blit because sprite.Group.draw() did NOT work for some reason
    for sprObj in sprWorldDrawList:
        renderScreen.blit(sprObj.image, (sprObj.rect.x - camPos[0], sprObj.rect.y - camPos[1]))

    ## Screen ##
    # scale render screen and blit to actual screen
    renderScreenScaled = pygame.transform.scale(renderScreen, screen.get_size())
    screen.blit(renderScreenScaled, (0, 0))
    # Text
    screen.blit(fpsTest, (0, 0))
    screen.blit(gridText, (0, 60))
    screen.blit(collisionText, (0, 120))
    screen.blit(tickText, (0, 180))
    
    # flip() display
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60