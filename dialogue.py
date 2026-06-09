import pygame
import functions as funcs
from pathlib import Path

GAME_DIR = Path(__file__).resolve().parent
FONT_DIR = GAME_DIR / "fonts"

pygame.font.init()
font = pygame.font.Font(FONT_DIR / "LowresPixel-Regular.otf", 10)

def sizeText(text): # TODO: just auto call this for every say() function
    textList = text.split()
    newTextLength = 0
    lengthLimit = 160
    newText = ""
    
    for i in range(len(textList)):
        wordLength = len(textList[i]) * 6
        if newTextLength + wordLength >= lengthLimit:
            newText = str(newText + "\n" + textList[i])
            lengthLimit += 160
        else:
            newText = str(newText + " " + textList[i])
        newTextLength += wordLength
    
    return newText[1:]
        
class Dialoguer(pygame.surface.Surface):
    def __init__(self, size, fc, text="Dialogue box was created", speaker=None):
        super().__init__(size, pygame.SRCALPHA)
        
        self.fill((0, 0, 0, 125))
        self.text = text
        self.startFrame = fc
        self.speaker = None
    
    def say(self, fc, text="No text in dialoguer.say()"):
        self.fill((0, 0, 0, 125))
        self.startFrame = fc
        self.text = text
    
    def update(self, fc):
        
        newText = font.render(self.text[:fc - self.startFrame], False, (255, 255, 255))
        
        self.blit(newText, (0, 0))
        return self