import pygame, json
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

    tiles_per_row = tilemap.get_width() // tileW
    
    colliderList = []

    for mapRow in range(mapH):
        for mapCol in range(mapW):
            tileNum = layers[mapRow * mapW + mapCol]

            # Skip empty tiles
            if tileNum == 0:
                continue
            tileNum -= 1
            
            src_x = (tileNum % tiles_per_row) * tileW
            src_y = (tileNum // tiles_per_row) * tileH
            
            sourceRect = pygame.Rect(src_x, src_y, tileW, tileH)
            tilemapSurface.blit(tilemap, (mapCol * tileW, mapRow * tileH), sourceRect)
            
            if "customColliders" in data and str(tileNum + 1) in data["customColliders"]:
                colliderData = data["customColliders"][str(tileNum + 1)]
                newRect = pygame.Rect(colliderData["x"] + (mapCol * tileW), colliderData["y"] + (mapRow * tileH),
                                      colliderData["w"], colliderData["h"])
                print(newRect)
                colliderList.append(newRect)

    return tilemapSurface, colliderList

# print(json.dumps(data, indent=4))
# print(data["layers"][0]["data"])