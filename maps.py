import pygame, json, collision, sys
from pathlib import Path

if getattr(sys, "frozen", False):
    GAME_DIR = Path(sys.executable).resolve().parent
else:
    GAME_DIR = Path(__file__).resolve().parent
MAP_DIR = GAME_DIR / "maps"
IMG_DIR = GAME_DIR / "imgs"

imgCollider = pygame.image.load(str(IMG_DIR / "spr_collider.png")).convert_alpha()

def eventUnpack(event):
    newList = []
    for i in range(len(event)):
        newList.append(event[i]["value"])
    return newList

def eventListUnpack(eventList):
    newEventList = []
    for i in range(len(eventList)):
        newEventList.append(eventUnpack(eventList[i]["value"]))
    return newEventList

class Map(object):
    def __init__(self, mapFile=None):
        super().__init__()

        self.colliderList = []
        self.interactorList = []
        self.triggerList = []
        self.imageList = []
        self.spawnsDict = {}

        self.tilemapSurface = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.overlaySurface = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.colliderSurface = pygame.Surface((0, 0), pygame.SRCALPHA)

        self.onLoadEventList = None
        self.onLeaveEventList = None

        if mapFile != None:
            self.loadMap(mapFile)

    def loadMap(self, mapFile):
        with open(MAP_DIR / mapFile, "r") as file:
            data = json.load(file)
        
        self.colliderList = []
        self.interactorList = []
        self.triggerList = []
        self.imageList = []
        self.spawnsDict = {}

        layers = data["layers"]
        # get layers
        for i in range(len(layers)):
            if layers[i]["type"] == "imagelayer":
                self.imageList.append(layers[i])
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
                    self.colliderList.append(newCollider)

            elif layers[i]["name"] == "Interactors":
                layerInteractors = layers[i]

                for object in layerInteractors["objects"]:
                    for prop in object["properties"]:
                        if prop["name"] == "event":
                            event = eventUnpack(prop["value"])
                    newInteractor = collision.Interactor(object["x"], object["y"], object["width"], object["height"], event)
                    self.interactorList.append(newInteractor)

            elif layers[i]["name"] == "Triggers":
                layerTriggers = layers[i]

                for object in layerTriggers["objects"]:
                    for prop in object["properties"]:
                        if prop["name"] == "event":
                            event = eventUnpack(prop["value"])
                    newTrigger = collision.Trigger(object["x"], object["y"], object["width"], object["height"], event)
                    self.triggerList.append(newTrigger)

            elif layers[i]["name"] == "Spawns":
                layerSpawns = layers[i]

                for i in range(len(layerSpawns["objects"])):
                    self.spawnsDict[layerSpawns["objects"][i]["name"]] = (layerSpawns["objects"][i]["x"], layerSpawns["objects"][i]["y"])

        # other data
        tileW = data["tilewidth"]
        tileH = data["tileheight"]
        mapW = data["width"]
        mapH = data["height"]
        
        if "name" in data["tilesets"][0]: # later account for possible multiple tilesets
            tilemap = pygame.image.load(str(IMG_DIR) + "/" + data["tilesets"][0]["name"] + ".png").convert_alpha()
            tiles_per_row = tilemap.get_width() // tileW

        self.tilemapSurface = pygame.Surface((mapW * tileW, mapH * tileH), pygame.SRCALPHA)
        self.overlaySurface = pygame.Surface((mapW * tileW, mapH * tileH), pygame.SRCALPHA)
        self.colliderSurface = pygame.Surface((mapW * tileW, mapH * tileH), pygame.SRCALPHA)

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
                        self.tilemapSurface.blit(tilemap, (mapCol * tileW, mapRow * tileH), sourceRect)
        
        # Image layers will work like this for now
        for imageLayer in self.imageList:
            img = pygame.image.load(str(IMG_DIR) + "/" + imageLayer["name"] + ".png").convert_alpha()
            self.tilemapSurface.blit(img, (imageLayer["offsetx"], imageLayer["offsety"]))

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
                        self.overlaySurface.blit(tilemap, (mapCol * tileW, mapRow * tileH), ovSourceRect)
        
        if 'layerCollision' in locals():
            for mapRow in range(mapH):
                for mapCol in range(mapW):
                    colTileNum = layerCollision[mapRow * mapW + mapCol]
                    # Colliders layer (standard colliders)
                    if colTileNum != 0:
                        newCollider = pygame.Rect((mapCol * tileW), (mapRow * tileH), tileW, tileH)
                        self.colliderSurface.blit(imgCollider, (mapCol * tileW, mapRow * tileH))
                        self.colliderList.append(newCollider)

        self.onLoadEventList = None
        self.onLeaveEventList = None

        if "properties" in data:
            for prop in data["properties"]:
                if prop["name"] == "onLoad":
                    self.onLoadEventList = eventListUnpack(prop["value"])
                elif prop["name"] == "onLeave":
                    self.onLeaveEventList = eventListUnpack(prop["value"])

    # deprecate return with new class structure

# print(json.dumps(data, indent=4))
# print(data["layers"][0]["data"])