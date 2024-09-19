from enum import IntEnum
from typing import TextIO, Tuple
from pathlib import Path
import numpy.typing as npt

import csv
import numpy as np


class TileType(IntEnum):
    UNDEFINED = -1
    WHEAT_FIELD = 0
    GRASSLAND = 1
    FOREST = 2
    SWAMP = 3
    LAKE = 4
    MINE = 5
    CASTLE = 6
    TABLE = 7


tile_types_str = [
    "Wheat Field",
    "Grassland",
    "Forest",
    "Swamp",
    "Lake",
    "Mine",
    "Castle",
    "Table",
]


class Board:
    img_idx: int

    def __init__(self, img_idx: int, tiles: npt.NDArray = None):
        self.img_idx = img_idx
        if tiles is not None:
            self.tiles = tiles
        else:
            self.tiles = np.full((5, 5), fill_value=-1, dtype=np.int8)

    @classmethod
    # If want to load all tiles from csv at once
    def from_array(cls, tiles_array: npt.NDArray, n_img: int):
        start_idx = n_img * 25
        end_idx = start_idx + 25

        return cls(tiles_array[start_idx:end_idx], n_img)

    @classmethod
    # If want to load only one board from csv
    def from_csv(cls, file_name: Path, n_img=-1):
        try:
            with open(file_name, "r+") as file:
                tiles_list = list(csv.reader(file))
                n_rows = len(tiles_list)

                if n_img == -1:
                    n_img = n_rows // 25

                start_idx = None
                if n_img == -1:
                    start_idx = 1 + n_rows - n_rows % 25
                else:
                    start_idx = 1 + (n_img * 25)
                end_idx = start_idx + 25
                tiles = np.array([row[3] for row in tiles_list[start_idx:end_idx]])

                if tiles.size != 0:
                    n_img = int(tiles_list[start_idx][0])
                    tiles = tiles.reshape((5, 5))
                    return cls(n_img, tiles)

                # n_img = 0 if this is reached
                return cls(n_img)

        except FileNotFoundError:
            with open(file_name, "w+") as file:
                writer = csv.writer(file)
                writer.writerow(["n_image", "n_row", "n_col", "tile_type"])

            return Board.from_csv(file_name, n_img)

    def to_csv(self, file_name: Path) -> None:
        with open(file_name, "r", newline="") as file:
            tiles_list = list(csv.reader(file))
            if (1 + (self.img_idx * 25)) < len(tiles_list):
                if int(tiles_list[1 + (self.img_idx * 25)][0]) == self.img_idx:
                    return  # avoid writing duplicates

        with open(file_name, "a", newline="") as file:
            writer = csv.writer(file)

            csv_rows = []
            for (n_row, n_col), tile_type in np.ndenumerate(self.tiles):
                csv_rows.append([self.img_idx, n_row, n_col, tile_type])

            writer.writerows(csv_rows)

    def get_all_tiles(self) -> npt.NDArray:
        return self.tiles

    def get_tile(self, idx: Tuple[int, int]) -> TileType:
        i, j = idx
        return self.tiles[i][j]

    def get_tiles_by_type(self, tile_type: TileType) -> list[TileType]:
        tile_list = []
        for row in self.tiles:
            for tile_type in row:
                tile_list.append(tile_type)

        return tile_list

    def set_tile(self, idx: Tuple[int, int], tile_type: TileType) -> None:
        i, j = idx
        self.tiles[i][j] = tile_type
        print(f"Setting tile ({i}, {j}) to {tile_type}")

    def is_finished(self):
        return not bool(len(self.tiles[self.tiles == TileType.UNDEFINED]))
