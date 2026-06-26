import pygame, json, sys
from pathlib import Path

if getattr(sys, "frozen", False):
    GAME_DIR = Path(sys.executable).resolve().parent
else:
    GAME_DIR = Path(__file__).resolve().parent
IMG_DIR = GAME_DIR / "imgs"

# Handles anims for standard sprites and stuff idk yet

class GameSprite(pygame.sprite.Sprite):
    instances = []
    
    def __init__(self, imgSrc):
        super().__init__()
        self.images = {}
        self.image = pygame.image.load(IMG_DIR / "spr_test1.png").convert_alpha()
        GameSprite.instances.append(self)
        
        # check for string & json or png
        if isinstance(imgSrc, str):
            
            if imgSrc[-5:] == ".json":
                # give json to charsprite class
                with open(imgSrc, "r") as file:
                    self.animData = json.load(file)
                
                # ONLY LOADS IMAGES INTO MEMORY
                if isinstance(self.animData, dict):
                    if "anims" in self.animData:
                        for k, v in self.animData["anims"].items():
                            self.images[k] = pygame.image.load(str(IMG_DIR) + "/" + self.animData["folderName"] + "/" + str(v["src"])).convert_alpha()
                        self.image = self.images["idle"]
                    if "sheets" in self.animData:
                        for k, v in self.animData["sheets"].items():
                            self.images[k] = pygame.image.load(str(IMG_DIR) + "/" + self.animData["folderName"] + "/" + str(v["src"])).convert_alpha()
                    
            elif imgSrc[-4:] == ".png":
                # 1 image sprite
                self.image = pygame.image.load(imgSrc).convert_alpha()
        
        self.rect = self.image.get_rect()
        self.lastFrameUpdate = 0
        self.curAnim = "idle"
        self.curAnimIndex = 0
        self.flipped = False
        
    def update(self, frameCount, anim=None, sheet=None): # ran every frame for every
        if anim:
            if sheet:
                self.image = self.images[sheet]
                if self.flipped == True and anim + "_flipped" in self.animData["sheets"][sheet]["anims"]:
                    anim = anim + "_flipped"
                    flipAnim = True
                else:
                    flipAnim = False
                
                spriteAnimData = self.animData["sheets"][sheet]["anims"][anim]
                spriteW, spriteH = self.animData["sheets"][sheet]["w"], self.animData["sheets"][sheet]["h"]
                spriteRow = 0
                spriteFr = 5
                
                # if new anim reset index
                if self.curAnim != anim:
                    self.curAnimIndex = 0
                    self.curAnim = anim
                    if "flip" in spriteAnimData:
                        self.flipped = spriteAnimData["flip"]
                    
                if "row" in spriteAnimData:
                    spriteRow = spriteAnimData["row"]
                if "fr" in spriteAnimData:
                    spriteFr = spriteAnimData["fr"]
                
                if "from" and "to" in spriteAnimData:
                    # animation stuff
                    
                    if (frameCount - self.lastFrameUpdate) > spriteFr:
                        self.curAnimIndex = (
                            self.curAnimIndex + 1
                        ) % (spriteAnimData["to"] - spriteAnimData["from"] + 1)
                        self.lastFrameUpdate = frameCount
                        
                    # apply the image from sprs
                    imgSurface = pygame.Surface((spriteW, spriteH), pygame.SRCALPHA)
                    imgSurface.blit(self.image, (0, 0), ((spriteAnimData["from"] * spriteW) + (self.curAnimIndex * spriteW), spriteRow * spriteH, spriteW, spriteH))
                    self.image = imgSurface
                
                self.rect.width, self.rect.height = spriteW, spriteH
            else:
                self.image = self.images[anim]
                self.curAnim = anim
                
                if "flip" in self.animData["anims"][anim] and self.animData["anims"][anim]["flip"] == True:
                    self.flipped = True
                
                imgRect = self.image.get_rect()
                self.rect.width, self.rect.height = imgRect.width, imgRect.height
    
        # universal
        if self.flipped == True and flipAnim == False:
            self.image = pygame.transform.flip(self.image, True, False)
            
class PlayerSprite(GameSprite):
    instances = []
    
    def __init__(self, imgSrc):
        super().__init__(imgSrc)
        PlayerSprite.instances.append(self)
        self.direction = "left"
        self.interactor = self.rect
        self.colliderect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, self.rect.h)
    
    def direct(self, fc, plrOldPos):
        self.colliderect.w, self.colliderect.h = self.rect.w / 1.5, self.rect.h / 8

        if plrOldPos[0] > self.rect.centerx:
            newDirection = "left"
        elif plrOldPos[0] < self.rect.centerx:
            newDirection = "right"
        elif plrOldPos[1] > self.rect.centery:
            newDirection = "up"
        elif plrOldPos[1] < self.rect.centery:
            newDirection = "down"
        else:
            newDirection = "idle"
        
        if newDirection == "idle": # why do i have to make things complicated
            newDirection = self.direction + "_idle"
        else:
            self.direction = newDirection
            
        self.update(fc, newDirection, "regular")