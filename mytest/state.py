from pathlib import Path
from typing import Tuple

import cv2 as cv
import numpy as np
import pygame

from k_domino import Board, TileType
from components import Action


class StateManager:
    def __init__(self, csv_file_name: Path):
        self.current_tile_type = TileType.WHEAT_FIELD
        self.action_history: list[Action] = []
        self.undo_history: list[Action] = []

        self.csv_file_name = csv_file_name

        # Load latest/create dataset
        print("Initializing board from csv")
        board = Board.from_csv(csv_file_name)
        self.board = board  # Assuming you have a Board class
        self._set_img()

    def inc_tile_type(self):
        self.current_tile_type += 1
        if (
            self.board.is_finished()
        ):  # Will have to restart if u need to select older tile type
            self._load_next_board()

    def undo(self):
        if len(self.action_history) > 0:
            action = self.action_history.pop()
            self.undo_history.append(action)
            self.board.set_tile((action.x, action.y), TileType.UNDEFINED)

    def redo(self):
        if len(self.undo_history) > 0:
            action = self.undo_history.pop()
            self.action_history.append(action)
            self.board.set_tile((action.x, action.y), action.tile_type)

    def set_tile(self, idx: Tuple[int, int], tile_type: TileType):
        self.action_history.append(Action(*idx, tile_type))
        self.board.set_tile(idx, tile_type)

    def _set_img(self):
        n_img = self.board.img_idx
        print(f"Reading image {n_img}")
        img = cv.imread(f"../dataset/{n_img+1}.jpg")
        rgb_img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
        rgb_img = cv.resize(rgb_img, None, fx=2, fy=2, interpolation=cv.INTER_LINEAR)
        rgb_img = np.rot90(rgb_img)
        self.img = pygame.surfarray.make_surface(rgb_img)

    def _load_next_board(self):
        print("Current Board finished. Initializing new Board.")
        self.current_tile_type = 0
        self.board.to_csv(self.csv_file_name)
        self.board = Board(self.board.img_idx + 1)
        self._set_img()
