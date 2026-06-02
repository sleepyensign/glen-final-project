import pygame

# takes tuple (0.5, 0.25) + screen w & h, returns pixel value
def sc_to_px(scaleTup):
    screenInfo = pygame.display.Info()
    return (scaleTup[0] * screenInfo.current_w, scaleTup[1] * screenInfo.current_h)

# takes tuple (800, 6000)
def px_to_sc(pixelTup):
    screenInfo = pygame.display.Info()
    return (round(pixelTup[0] / screenInfo.current_w, 3), round(pixelTup[1] / screenInfo.current_h, 3))