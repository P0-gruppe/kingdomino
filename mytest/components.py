from dataclasses import dataclass
from types import FunctionType
import numpy.typing as npt
import pygame

from k_domino import TileType


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        font: pygame.font.Font,
        color: pygame.color.Color,
        text_color: pygame.color.Color,
        callback: FunctionType,
        border_radius=-1,
    ):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = font.render(text, True, text_color)
        self.color = color
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.border_radius = border_radius
        self.callback = callback

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0, 30)
        surface.blit(self.text, self.text_rect)

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            self.callback()
            return True
        return False


class Grid:
    def __init__(self, x, y, width, height, border_size=5, rows=5, cols=5):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.pos = (x, y)
        self.border_size = border_size
        self.tile_width = width // self.cols
        self.tile_height = height // self.rows
        self.border_color = pygame.Color(128, 128, 128, 255)  # gray
        self.fill_color = pygame.Color(128, 128, 128, 153)  # 0.3 opaque gray

        self.grid_surface = pygame.Surface((1200, 1200), pygame.SRCALPHA)

    def draw(self, surface, tiles: npt.NDArray):
        self.grid_surface.fill((255, 255, 255, 0))

        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.tile_width
                y = row * self.tile_height
                rect = pygame.Rect(x, y, self.tile_width, self.tile_height)
                if tiles[row][col] != TileType.UNDEFINED:
                    pygame.draw.rect(self.grid_surface, self.fill_color, rect)
                pygame.draw.rect(
                    self.grid_surface, self.border_color, rect, self.border_size
                )

        surface.blit(self.grid_surface, self.pos)

    def get_clicked_tile(self, mouse_pos):
        x, y = (
            mouse_pos[0] - self.pos[0],
            mouse_pos[1] - self.pos[1],
        )
        if 0 <= x < self.width and 0 <= y < self.height:
            col = x // self.tile_width
            row = y // self.tile_height
            return row, col
        return None


@dataclass
class Action:
    x: int
    y: int

    tile_type: TileType
