import pygame, json

testMapFile = "final_project/maps/map_final_test_1.tmj"
testTilemap = "final_project/imgs/tilemap_final_project_1_2.png"

# later implement loading different maps through params and stuff
def load_map():
    with open(testMapFile, "r") as file:
        data = json.load(file)

    layers = data["layers"][0]["data"]
    tileW = data["tilewidth"]
    tileH = data["tileheight"]
    mapW = data["width"]
    mapH = data["height"]

    tilemap = pygame.image.load("final_project/imgs/" + data["tilesets"][0]["name"] + ".png")

    tilemapSurface = pygame.Surface((mapW * tileW, mapH * tileH), pygame.SRCALPHA)

    tiles_per_row = tilemap.get_width() // tileW

    for mapRow in range(mapH):
        for mapCol in range(mapW):
            tileNum = layers[mapRow * mapW + mapCol]

            # Skip empty tiles
            if tileNum == 0:
                continue
            tileNum -= 1
            
            src_x = (tileNum % tiles_per_row) * tileW
            src_y = (tileNum // tiles_per_row) * tileH
            
            source_rect = pygame.Rect(src_x, src_y, tileW, tileH)
            tilemapSurface.blit(tilemap, (mapCol * tileW, mapRow * tileH), source_rect)

    return tilemapSurface

# print(json.dumps(data, indent=4))
# print(data["layers"][0]["data"])