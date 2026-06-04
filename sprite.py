import pygame
import functions_test as fc_t

# Handles anims for standard sprites and stuff idk yet

class CharSprite(pygame.sprite.Sprite):
    def __init__(self, imgDict):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(imgDict["idle"])
        self.rect = self.image.get_rect()
        self.rect.x = 500
        self.rect.y = 500
        # fix centering issue
        print("Made a sprite")
    
    def update(self, img):
        if isinstance(img, dict):
            self.image = pygame.image.load(img["img"])
            if "flip" in img and img["flip"] == True:
                self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = pygame.image.load(img)