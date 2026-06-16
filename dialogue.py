import pygame, json
import functions as funcs
import keypress
from pathlib import Path

GAME_DIR = Path(__file__).resolve().parent
FONT_DIR = GAME_DIR / "fonts"
IMG_DIR = GAME_DIR / "imgs"
DIAL_DIR = GAME_DIR / "dialogue"

DIALOGUE_WAIT = 0

with open(DIAL_DIR / "dialogue.json", "r") as file:
    dialogue = json.load(file)

pygame.font.init()
font = pygame.font.Font(FONT_DIR / "LowresPixel-Regular.otf", 10)

sprsArrow = pygame.image.load(IMG_DIR / "Dialogue_Arrow" / "sprs_dialogue_arrow_2.png").convert_alpha()

def sizeText(text):
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
    def __init__(self, size, fc):
        super().__init__(size, pygame.SRCALPHA)
        
        self.fill((0, 0, 0, 125))
        self.text = ""
        self.startFrame = fc
        self.speaker = None # feature add later
        self.arrowIndex = 0
        self.queue = []
    
    def say(self, text="No text in dialoguer.say()"):
        self.fill((0, 0, 0, 125))
        
        splitText = text.split("-")
        if len(splitText) > 1:
            self.text = "" # WILL CAUSE PROBLEMS???? WHO KNOWS
            speaker, dialTag = splitText[0], splitText[1]
            if speaker in dialogue and dialTag in dialogue[speaker]:
                for i in range(len(dialogue[speaker][dialTag])):
                    self.queue.append(sizeText(dialogue[speaker][dialTag][i]))
        else:
            if not text in self.queue: # should work
                self.queue.append(sizeText(text))
    
    def update(self, fc, nextDialogue):
        keys = pygame.key.get_pressed()
        
        self.fill((0, 0, 0, 125))
        
        canContinue = fc - self.startFrame > len(self.text) + DIALOGUE_WAIT
        
        if len(self.queue) == 0:
            self.fill((0, 0, 0, 0))
            return self
        
        if nextDialogue:
            if canContinue:
                canContinue = False # so arrow dissapears
                # Press enter & arrow
                self.startFrame = fc
                if self.text in self.queue:
                    self.queue.remove(self.text)
                    if len(self.queue) > 0:
                        self.text = self.queue[0]
            else: # skip dialogue
                self.startFrame -= 500
        elif not self.text in self.queue: # mad jank, might need fixing later
            self.startFrame = fc
            self.text = self.queue[0]
            canContinue = False
        
        newText = font.render(self.text[:fc - self.startFrame], False, (255, 255, 255))
        
        if canContinue:
            self.arrowIndex
            if fc % 10 == 0:
                self.arrowIndex = fc % 40 / 10
            self.blit(sprsArrow, (151, 35), (self.arrowIndex * 7, 0, 7, 9))
        
        self.blit(newText, (0, 0))
        return self