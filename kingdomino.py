import cv2 as cv
import numpy as np
import os

points = {
    "Field": 0,
    "Forest": 0,
    "Lake": 0,
    "Grassland": 0,
    "Swamp": 0,
    "Mine": 0,
    "Home": 0,
    "Table": 0,
}


# Main function containing the backbone of the program
def main():
    print("+-------------------------------+")
    print("| King Domino points calculator |")
    print("+-------------------------------+")
    image_path = "./dataset/pictures/1.jpg"
    if not os.path.isfile(image_path):
        print("Image not found")
        return
    image = cv.imread(image_path)
    tiles = get_tiles(image)
    print(len(tiles))
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            print(f"Tile ({x}, {y}):")
            tile_type = get_terrain(tile)
            points[tile_type] += 1
            print("=====")
    print(points)


# Break a board into tiles
def get_tiles(image):
    tiles = []
    for y in range(5):
        tiles.append([])
        for x in range(5):
            tiles[-1].append(image[y * 100 : (y + 1) * 100, x * 100 : (x + 1) * 100])
    return tiles


# Determine the type of terrain in a tile
def get_terrain(tile):
    hsv_tile = cv.cvtColor(tile, cv.COLOR_BGR2HSV)
    hue, saturation, value = np.median(hsv_tile, axis=(0, 1))

    print(f"H: {hue}, S: {saturation}, V: {value}")

    if 22 < hue < 30 and 225 < saturation < 256 and 104 < value < 210:
        return "Field"
    if 28 < hue < 61 and 73 < saturation < 224 and 32 < value < 70:
        return "Forest"
    if 100 < hue < 110 and 210 < saturation < 256 and 107 < value < 195:
        return "Lake"
    if 33 < hue < 49 and 160 < saturation < 256 and 72 < value < 170:
        return "Grassland"
    if 17 < hue < 30 and 34 < saturation < 210 and 72 < value < 148:
        return "Swamp"
    if 19 < hue < 28 and 38 < saturation < 140 and 23 < value < 70:
        return "Mine"
    if 16 < hue < 39 and 40 < saturation < 150 and 52 < value < 150:
        return "Home"
    return "Table"


if __name__ == "__main__":
    main()
