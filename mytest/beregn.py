import csv
import cv2 as cv
import numpy as np

import os
from sys import argv


if len(argv) < 3:
    print("Provide a computation mode with --mode. (mean/median)")
    exit()

MODE = argv[2]

if MODE != "mean" and MODE != "median":
    print()

INPUT_FILE_PATH = "dataset.csv"
OUTPUT_FILE_PATH = f"{MODE.lower()}_hsv.csv"


def get_tiles(img):
    return img.reshape((5, 100, 5, 100, 3)).transpose(0, 2, 1, 3, 4)


labels = None
n_imgs = 0

with open(INPUT_FILE_PATH, "r") as file:
    tiles_list = list(csv.reader(file))

    n_imgs = len(tiles_list) // 25

    # convert to ints
    csv_data = np.array(tiles_list[1:], dtype=np.int8)

    labels = csv_data[:, 3].reshape(n_imgs, 5, 5)
    labels = np.flip(labels, axis=2)

# n_imgs, counts = np.unique(csv_data[:, 0], return_counts=True)
img_data = np.zeros((n_imgs, 5, 5, 100, 100, 3))
for i in range(0, n_imgs):
    img = cv.imread(f"../dataset/{i+1}.jpg")
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    tiles = get_tiles(hsv)

    img_data[i] = tiles

values = None

if MODE == "median":
    values = np.median(img_data, axis=(3, 4))  # (n_imgs, 5, 5, 3)
else:
    values = np.mean(img_data, axis=(3, 4))

unique_labels = np.unique(labels)
output = np.zeros((n_imgs, 8, 5, 5, 3))

# Iterate over each image and unique label
for i in range(n_imgs):
    print(i)
    for j, label in enumerate(unique_labels):
        # Create a mask for the current label
        mask = labels[i] == label

        # Use the mask to select the corresponding HSV values
        # and store them in the output array
        output[i, j] = np.where(mask[:, :, np.newaxis], values[i], 0)

rows = []
if not os.path.exists(OUTPUT_FILE_PATH):
    # make file
    with open(OUTPUT_FILE_PATH, "w+") as file:
        file.write("n_img,n_row,n_col,tile_type,h,s,v\n")
        file.close()


for i in range(n_imgs):
    for j in range(8):
        for k in range(5):
            for l in range(5):
                if np.all(output[i, j, k, l]):
                    rows.append(
                        [
                            i,
                            k,
                            l,
                            j,
                            output[i, j, k, l, 0],
                            output[i, j, k, l, 1],
                            output[i, j, k, l, 2],
                        ]
                    )

with open(OUTPUT_FILE_PATH, "a") as file:
    writer = csv.writer(file)
    writer.writerows(rows)
