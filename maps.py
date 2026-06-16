import pygame, json, collision
from pathlib import Path

GAME_DIR = Path(__file__).resolve().parent
MAP_DIR = GAME_DIR / "maps"
IMG_DIR = GAME_DIR / "imgs"

# later implement loading different maps through params and stuff
def load_map(mapFile):
    with open(MAP_DIR / mapFile, "r") as file:
        data = json.load(file)

    layers = data["layers"][0]["data"]
    tileW = data["tilewidth"]
    tileH = data["tileheight"]
    mapW = data["width"]
    mapH = data["height"]

    tilemap = pygame.image.load(str(IMG_DIR) + "/" + data["tilesets"][0]["name"] + ".png").convert_alpha()

    tilemapSurface = pygame.Surface((mapW * tileW, mapH * tileH), pygame.SRCALPHA)
    overlaySurface = pygame.Surface((mapW * tileW, mapH * tileH), pygame.SRCALPHA)

    tiles_per_row = tilemap.get_width() // tileW
    
    colliderList = []
    interactorList = []

    for mapRow in range(mapH):
        for mapCol in range(mapW):
            tileNum = layers[mapRow * mapW + mapCol]

            # Skip empty tiles
            if tileNum == 0:
                continue
            tileNum -= 1
            
            srcX = (tileNum % tiles_per_row) * tileW # src is x and y for image surface
            srcY = (tileNum // tiles_per_row) * tileH
            
            sourceRect = pygame.Rect(srcX, srcY, tileW, tileH)
            
            if "customOverlays" in data and str(tileNum + 1) in data["customOverlays"]:
                # create the stuff for the underneath tile
                unTileNum = int(data["customOverlays"][str(tileNum + 1)])
                unTileNum -= 1
                
                unSrcX = (unTileNum % tiles_per_row) * tileW
                unSrcY = (unTileNum // tiles_per_row) * tileH
                
                unSourceRect = pygame.Rect(unSrcX, unSrcY, tileW, tileH)
                
                tilemapSurface.blit(tilemap, (mapCol * tileW, mapRow * tileH), unSourceRect)
                overlaySurface.blit(tilemap, (mapCol * tileW, mapRow * tileH), sourceRect)
            else:
                tilemapSurface.blit(tilemap, (mapCol * tileW, mapRow * tileH), sourceRect)
            
            if "customColliders" in data and str(tileNum + 1) in data["customColliders"]:
                colliderData = data["customColliders"][str(tileNum + 1)]
                newCollider = pygame.Rect(colliderData["x"] + (mapCol * tileW), colliderData["y"] + (mapRow * tileH),
                                      colliderData["w"], colliderData["h"])
                colliderList.append(newCollider)
            
            if "customInteractors" in data and str(mapRow * mapW + mapCol) in data["customInteractors"]:
                interactorData = data["customInteractors"][str(mapRow * mapW + mapCol)]
                
                if interactorData["useCollider"] == False:
                    newInteractor = collision.Interactor(mapCol * tileW - tileW / 4, mapRow * tileH - tileH / 4,
                                                         tileW * 1.5, tileH * 1.5, interactorData["event"])
                else:
                    newInteractor = collision.Interactor(newCollider.x, newCollider.y,
                                                         newCollider.width, newCollider.height, interactorData["event"])
                
                interactorList.append(newInteractor)

    return tilemapSurface, colliderList, overlaySurface, interactorList

# print(json.dumps(data, indent=4))
# print(data["layers"][0]["data"])