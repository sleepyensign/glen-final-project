import os, sys, pygame, time, random
import sprite as spr
import maps, collision, keypress
from pathlib import Path

# Env Vars
GAME_DIR = Path(__file__).resolve().parent
IMG_DIR = GAME_DIR / "imgs"
DIAL_DIR = GAME_DIR / "dialogue"
MOVE_SPEED = 1
RENDER_W = 320
RENDER_H = 180
FRAMERATE = 60
DEBUG_COLOR = (64, 64, 64)

# pygame setup
pygame.init()
pygame.font.init()
pygame.display.set_caption("The Final")
screen = pygame.display.set_mode(
    (pygame.display.Info().current_w, pygame.display.Info().current_h),
    pygame.FULLSCREEN,
)
renderScreen = pygame.Surface((RENDER_W, RENDER_H), pygame.SRCALPHA)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 64)

import dialogue # after so display module is loaded

# Functions

def debugSurface(obj, color):
    newSurface = pygame.Surface((obj.width, obj.height), pygame.SRCALPHA)
    newSurface.fill(color)
    return newSurface

def executeEvent(event):
    if event[0] == "dialogue":
        dialogueBox.say(event[1])

# Sprite setup
UIDrawList = []  # later implement

plr = spr.PlayerSprite(str(IMG_DIR / "David" / "animStruct.json"))
charTest = spr.GameSprite(str(IMG_DIR / "spr_test1.png"))
charBobNpc = spr.GameSprite(str(IMG_DIR / "Bob" / "animStruct.json"))

plr.rect.center = (200, 200)
charBobNpc.rect.center = (300, 200)

# Map setup
theMap, colliderList, overlayMap, interactorList = maps.load_map("map_final_test_1.json")

# vars
running = True
fc = 0
camPos = [0, 0]
takeInput = True
inDialogue = False
debugMenu = False

# old vars
oldKeys = pygame.key.get_pressed()

testTextJson = "David-dlg_david_intro"
testText2 = "This is a string I made to test several systems in this stupid game."
dialogueBox = dialogue.Dialoguer((0.5 * RENDER_W, 0.25 * RENDER_H), fc)

while running:

    ### SCREEN WIPE ###
    renderScreen.fill("black")

    ### EVENTS ###
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    camPosOld = camPos
    plrOldPos = (plr.rect.centerx, plr.rect.centery)
    
    # Input control
    if len(dialogueBox.queue) > 0:
        inDialogue = True
    else:
        inDialogue = False
        
    if inDialogue:
        takeInput = False
    else:
        takeInput = True

    ### INPUT ###
    keys = pygame.key.get_pressed()
    if takeInput == True:
        if keys[pygame.K_s]:
            plr.rect.centery += MOVE_SPEED
        if keys[pygame.K_w]:
            plr.rect.centery -= MOVE_SPEED
        if keys[pygame.K_a]:
            plr.rect.centerx -= MOVE_SPEED
        if keys[pygame.K_d]:
            plr.rect.centerx += MOVE_SPEED
        
        if keypress.getKeyDown(pygame.K_F3, keys, oldKeys):
            debugMenu = not debugMenu
    
    # Bypass takeInput  
    interactKey = keypress.getKeyDown(pygame.K_RETURN, keys, oldKeys)
    
    plrInteractHits = plr.interactor.collidelistall(interactorList)
    if interactKey and not inDialogue and len(plrInteractHits) > 0:
        executeEvent(interactorList[plrInteractHits[0]].event)
    
    # After all key stuff
    oldKeys = keys

    ### COLLISION ###
    plrCollisionHits = plr.rect.collidelistall(colliderList)
    for item in plrCollisionHits:
        collision.plrColStatic(plr.rect, colliderList[item], plrOldPos)

    # Camera
    tempCamAdd = (RENDER_W / 2, RENDER_H / 2)
    camPos[0] = plr.rect.centerx - tempCamAdd[0]
    camPos[1] = plr.rect.centery - tempCamAdd[1]

    # Maps ._.

    ### RENDER ###
    ## Text ##
    # Debug #
    debugText = []
    if debugMenu == True:
        fpsTest = font.render("frame " + str(fc), True, DEBUG_COLOR)
        tickText = font.render("second " + str(pygame.time.get_ticks() / 1000), True, DEBUG_COLOR)
        gridText = font.render("pos: " + str(camPos), True, DEBUG_COLOR)
        collisionText = font.render("colliding: " + str(plrCollisionHits), True, DEBUG_COLOR)
        interactorText = font.render("interact: " + str(plrInteractHits), True, DEBUG_COLOR)
        textText = font.render("text: " + str(dialogueBox.text[:10] + "..."), True, DEBUG_COLOR)
        debugQueue = [queueItem[:5] + "..." for queueItem in dialogueBox.queue]
        queueText = font.render("queue: " + str(debugQueue), True, DEBUG_COLOR)
        debugText.extend([fpsTest, tickText, gridText, collisionText, interactorText, textText, queueText])
    
    ## Sprite ##
    # PlayerSprites
    for instance in spr.PlayerSprite.instances:
        instance.direct(fc, plrOldPos)
    
    # testing dialogue
    if fc == 0:
        dialogueBox.say("Try interacting with some signs!")
        dialogueBox.say("Some text will run off screen from an unpatched bug.")

    # Frame counter
    fc += 1

    ### BLIT ###
    ## Render Screen ##
    # Map
    renderScreen.blit(theMap, (-camPos[0], -camPos[1]))
    # Sprite
    for sprObj in spr.GameSprite.instances:
        renderScreen.blit(sprObj.image, (sprObj.rect.x - camPos[0], sprObj.rect.y - camPos[1]))
    # Map Overlay
    renderScreen.blit(overlayMap, (-camPos[0], -camPos[1]))
    # UI
    renderScreen.blit(dialogueBox.update(fc, interactKey), (0.25 * RENDER_W, 0.75 * RENDER_H))
    # Debug Colliders
    if debugMenu:
        for colObj in colliderList:
            renderScreen.blit(debugSurface(colObj, (0, 0, 150, 125)), (colObj.x - camPos[0], colObj.y - camPos[1]))
        for intObj in interactorList:
            renderScreen.blit(debugSurface(intObj, (150, 0, 0, 125)), (intObj.x - camPos[0], intObj.y - camPos[1]))
        for spriteObj in spr.GameSprite.instances:
            renderScreen.blit(debugSurface(spriteObj.rect, (0, 0, 150, 125)), (spriteObj.rect.x - camPos[0], spriteObj.rect.y - camPos[1]))
        for spriteObj in spr.PlayerSprite.instances:
            renderScreen.blit(debugSurface(spriteObj.interactor, (150, 0, 0, 125)), (spriteObj.rect.x - camPos[0], spriteObj.rect.y - camPos[1]))

    ## Screen ##
    # Render screen -> screen
    renderScreenScaled = pygame.transform.scale(renderScreen, screen.get_size())
    screen.blit(renderScreenScaled, (0, 0))
    # Debug menu
    for i in range(len(debugText)):
        screen.blit(debugText[i], (0, 60 * i))

    # flip() display
    pygame.display.flip()

    clock.tick(FRAMERATE)
