import pygame

def getKeyUp(key, keys, oldKeys):
    if keys[key] == False and oldKeys[key] == True:
        return True
    else:
        return False
    
def getKeyDown(key, keys, oldKeys):
    if keys[key] == True and oldKeys[key] == False:
        return True
    else:
        return False