import pygame

edgeDict = { # not used
    "left": -1,
    "right": 1,
    "up": -1,
    "down": 1
}

class Interactor(pygame.Rect):
    def __init__(self, x, y, w ,h, event):
        super().__init__(x, y, w, h)
        
        self.event = event

class Trigger(pygame.Rect):
    def __init__(self, x, y, w, h, event, oneUse=True):
        super().__init__(x, y, w, h)
        
        self.event = event
        self.oneUse = oneUse

def plrColStatic(plrRect, static):
    overlap_left = plrRect.right - static.left
    overlap_right = static.right - plrRect.left
    overlap_top = plrRect.bottom - static.top
    overlap_bottom = static.bottom - plrRect.top

    min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

    if min_overlap == overlap_left:
        plrRect.right = static.left
    elif min_overlap == overlap_right:
        plrRect.left = static.right
    elif min_overlap == overlap_top:
        plrRect.bottom = static.top
    else:
        plrRect.top = static.bottom