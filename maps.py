import pygame, json, collision
from pathlib import Path

GAME_DIR = Path(__file__).resolve().parent
MAP_DIR = GAME_DIR / "maps"
IMG_DIR = GAME_DIR / "imgs"

imgCollider = pygame.image.load(str(IMG_DIR / "spr_collider.png")).convert_alpha()

def eventUnpack(event):
    newList = []
    for i in range(len(event)):
        newList.append(event[i]["value"])
    return newList

def load_map(mapFile):
    with open(MAP_DIR / mapFile, "r") as file:
        data = json.load(file)
    
    colliderList = []
    interactorList = []
    triggerList = []
    imageList = []
    spawnsDict = {}

    layers = data["layers"]
    # get layers
    for i in range(len(layers)):
        if layers[i]["type"] == "imagelayer":
            imageList.append(layers[i])
        elif layers[i]["name"] == "Base":
            layerBase = layers[i]["data"]
        elif layers[i]["name"] == "Overlay":
            layerOverlay = layers[i]["data"]
        elif layers[i]["name"] == "CollisionMap":
            layerCollision = layers[i]["data"]
        elif layers[i]["name"] == "Colliders":
            layerColliders = layers[i]

            for object in layerColliders["objects"]:
                newCollider = pygame.Rect(object["x"], object["y"], object["width"], object["height"])
                colliderList.append(newCollider)

        elif layers[i]["name"] == "Interactors":
            layerInteractors = layers[i]

            for object in layerInteractors["objects"]:
                for prop in object["properties"]:
                    if prop["name"] == "event":
                        event = eventUnpack(prop["value"])
                newInteractor = collision.Interactor(object["x"], object["y"], object["width"], object["height"], event)
                interactorList.append(newInteractor)

        elif layers[i]["name"] == "Triggers":
            layerTriggers = layers[i]

            for object in layerTriggers["objects"]:
                for prop in object["properties"]:
                    if prop["name"] == "event":
                        event = eventUnpack(prop["value"])
                newTrigger = collision.Trigger(object["x"], object["y"], object["width"], object["height"], event)
                triggerList.append(newTrigger)

        elif layers[i]["name"] == "Spawns":
            layerSpawns = layers[i]

            for i in range(len(layerSpawns["objects"])):
                spawnsDict[layerSpawns["objects"][i]["name"]] = (layerSpawns["objects"][i]["x"], layerSpawns["objects"][i]["y"])

    # other data
    tileW = data["tilewidth"]
    tileH = data["tileheight"]
    mapW = data["width"]
    mapH = data["height"]
    
    if "name" in data["tilesets"][0]: # later account for possible multiple tilesets
        tilemap = pygame.image.load(str(IMG_DIR) + "/" + data["tilesets"][0]["name"] + ".png").convert_alpha()
        tiles_per_row = tilemap.get_width() // tileW

    tilemapSurface = pygame.Surface((mapW * tileW, mapH * tileH), pygame.SRCALPHA)
    overlaySurface = pygame.Surface((mapW * tileW, mapH * tileH), pygame.SRCALPHA)
    colliderSurface = pygame.Surface((mapW * tileW, mapH * tileH), pygame.SRCALPHA)

    # note to self: src is x and y for image surface
    if 'layerBase' in locals():
        for mapRow in range(mapH):
            for mapCol in range(mapW):
                tileNum = layerBase[mapRow * mapW + mapCol]
                # Base layer
                if tileNum != 0:
                    tileNum -= 1
                    srcX = (tileNum % tiles_per_row) * tileW
                    srcY = (tileNum // tiles_per_row) * tileH
                    sourceRect = pygame.Rect(srcX, srcY, tileW, tileH)
                    tilemapSurface.blit(tilemap, (mapCol * tileW, mapRow * tileH), sourceRect)
    
    # Image layers will work like this for now
    for imageLayer in imageList:
        img = pygame.image.load(str(IMG_DIR) + "/" + imageLayer["name"] + ".png").convert_alpha()
        tilemapSurface.blit(img, (imageLayer["offsetx"], imageLayer["offsety"]))

    if 'layerOverlay' in locals():
        for mapRow in range(mapH):
            for mapCol in range(mapW):
                ovtileNum = layerOverlay[mapRow * mapW + mapCol]
                # Overlay layer
                if ovtileNum != 0:
                    ovtileNum -= 1
                    ovSrcX = (ovtileNum % tiles_per_row) * tileW
                    ovSrcY = (ovtileNum // tiles_per_row) * tileH
                    ovSourceRect = pygame.Rect(ovSrcX, ovSrcY, tileW, tileH)
                    overlaySurface.blit(tilemap, (mapCol * tileW, mapRow * tileH), ovSourceRect)
    
    if 'layerCollision' in locals():
        for mapRow in range(mapH):
            for mapCol in range(mapW):
                colTileNum = layerCollision[mapRow * mapW + mapCol]
                # Colliders layer (standard colliders)
                if colTileNum != 0:
                    newCollider = pygame.Rect((mapCol * tileW), (mapRow * tileH), tileW, tileH)
                    colliderSurface.blit(imgCollider, (mapCol * tileW, mapRow * tileH))
                    colliderList.append(newCollider)

    return tilemapSurface, colliderList, colliderSurface, overlaySurface, interactorList, triggerList, spawnsDict

# print(json.dumps(data, indent=4))
# print(data["layers"][0]["data"])