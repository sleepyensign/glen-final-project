import os, sys, pygame, numpy, time, random
import functions_test as fc_t
import sprite as spr
import maps

# Env Vars
MOVE_SPEED = 2
RENDER_W = 320 * 2
RENDER_H = 180 * 2

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

charBobImgDict = {
    "idle": "final_project/imgs/spr_bob_idle.png",
    "left": "final_project/imgs/spr_bob_left.png",
    "right": {"img": "final_project/imgs/spr_bob_left.png", "flip": True},
    "up": "final_project/imgs/spr_bob_up.png",
    "down": "final_project/imgs/spr_bob_down.png"
    }
charTestImgDict = {
    "idle": "final_project/imgs/spr_test1.png"
}
charBob = spr.CharSprite(charBobImgDict)
charTest = spr.CharSprite(charTestImgDict)
sprWorldDrawList.extend([charBob, charTest])

theMap = maps.load_map()

# vars
running = True
frame_count = 0
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
    charBobOldPos = (charBob.x, charBob.y)
    
    ### INPUT ###
    keys = pygame.key.get_pressed()
    if takeInput == True:
        if keys[pygame.K_s]:
            charBob.y += MOVE_SPEED
        if keys[pygame.K_w]:
            charBob.y -= MOVE_SPEED
        if keys[pygame.K_a]:
            charBob.x -= MOVE_SPEED
        if keys[pygame.K_d]:
            charBob.x += MOVE_SPEED
    
    # Camera
    tempCamAdd = (RENDER_W / 2, RENDER_H / 2)
    camPos[0] = charBob.x - tempCamAdd[0]
    camPos[1] = charBob.y - tempCamAdd[1]
    
    # Background
    # will do this later
    
    ### RENDER ###
    # Text
    fpsTest = font.render("frame " + str(frame_count), True, (0, 0, 0))
    gridText = font.render("pos: " + str(camPos), True, (0, 0, 0))
    # Sprite
    # Update chars based off cam movement -- later change to a list or smth not just bob maybe
    if charBobOldPos[1] > charBob.y:
        charBob.update(charBobImgDict["up"])
    elif charBobOldPos[1] < charBob.y:
        charBob.update(charBobImgDict["down"])
    else:
        charBob.update(charBobImgDict["idle"])
    if charBobOldPos[0] > charBob.x:
        charBob.update(charBobImgDict["left"])
    elif charBobOldPos[0] < charBob.x:
        charBob.update(charBobImgDict["right"])
    
    # Incrementaal
    frame_count += 1
    
    ### BLIT ###
    ## Render Screen ##
    # Map
    renderScreen.blit(theMap, (-camPos[0], -camPos[1]))
    # Sprite - we are doing a loop & blit because sprite.Group.draw() did NOT work for some reason
    for sprObj in sprWorldDrawList:
        renderScreen.blit(sprObj.image, (sprObj.x - camPos[0], sprObj.y - camPos[1]))

    ## Screen Blit ##
    # scale render screen and blit to actual screen
    renderScreenScaled = pygame.transform.scale(renderScreen, screen.get_size())
    screen.blit(renderScreenScaled, (0, 0))
    # Text
    screen.blit(fpsTest, (0, 0))
    screen.blit(gridText, (0, 60))
    
    # flip() display
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60