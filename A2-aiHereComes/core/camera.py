from typing import Tuple
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, MAP_WIDTH, MAP_HEIGHT


class Camera:
    def __init__(self):
        self.x = 0.0  # top-left corner in world pixels
        self.y = 0.0

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy
        self._clamp()

    def _clamp(self):
        max_x = MAP_WIDTH * TILE_SIZE - SCREEN_WIDTH
        max_y = MAP_HEIGHT * TILE_SIZE - SCREEN_HEIGHT
        self.x = max(0, min(self.x, max_x))
        self.y = max(0, min(self.y, max_y))

    def world_to_screen(self, wx: float, wy: float) -> Tuple[float, float]:
        return wx - self.x, wy - self.y

    def screen_to_world(self, sx: float, sy: float) -> Tuple[float, float]:
        return sx + self.x, sy + self.y

    def screen_to_tile(self, sx: float, sy: float) -> Tuple[int, int]:
        wx, wy = self.screen_to_world(sx, sy)
        return int(wx // TILE_SIZE), int(wy // TILE_SIZE)

    def get_visible_tile_range(self) -> Tuple[int, int, int, int]:
        start_col = max(0, int(self.x // TILE_SIZE))
        start_row = max(0, int(self.y // TILE_SIZE))
        end_col = min(MAP_WIDTH, int((self.x + SCREEN_WIDTH) // TILE_SIZE) + 2)
        end_row = min(MAP_HEIGHT, int((self.y + SCREEN_HEIGHT) // TILE_SIZE) + 2)
        return start_col, start_row, end_col, end_row

    def center_on(self, wx: float, wy: float):
        self.x = wx - SCREEN_WIDTH / 2
        self.y = wy - SCREEN_HEIGHT / 2
        self._clamp()
