import pygame, json
import functions_test as fc_t

# Handles anims for standard sprites and stuff idk yet

class CharSprite(pygame.sprite.Sprite): # FIX FOR NEW CODE AND FEATURES
    def __init__(self, imgSrc):
        super().__init__()
        self.images = {}
        self.image = pygame.image.load("final_project/imgs/spr_test1.png")
        
        # check for string & json or png
        if isinstance(imgSrc, str):
            if imgSrc[-5:] == ".json":
                # give json to charsprite class
                with open(imgSrc, "r") as file:
                    self.animData = json.load(file)
                
                # load all images once
                if isinstance(self.animData, dict):
                    for k, v in self.animData["anims"].items():
                        self.images[k] = pygame.image.load("final_project/imgs/" + self.animData["folderName"] + "/" + str(v["src"]))
                    self.image = self.images["idle"]
            elif imgSrc[-4:] == ".png":
                self.image = pygame.image.load(imgSrc)
        
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 500

    def update(self, anim):
        print(self.images)
        self.image = self.images[anim]
        if "flip" in self.animData["anims"][anim]:
            self.image = pygame.transform.flip(self.image, True, False)
        if "from" and "to" in self.animData["anims"][anim]:
            print("ahhhh")
            # will allow for animations and stuff, thinking lastAnimUpdate += 1 at framerate, default 30 or something unless def in json