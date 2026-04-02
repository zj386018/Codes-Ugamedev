from typing import List, Optional, Tuple
from constants import MAP_WIDTH, MAP_HEIGHT
from world.tile import Tile
from constants import TerrainType


class GameMap:
    def __init__(self, width: int = MAP_WIDTH, height: int = MAP_HEIGHT):
        self.width = width
        self.height = height
        self.tiles: List[List[Tile]] = []
        for y in range(height):
            row = []
            for x in range(width):
                row.append(Tile(x, y, TerrainType.GRASS))
            self.tiles.append(row)

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None

    def set_terrain(self, x: int, y: int, terrain: TerrainType):
        tile = self.get_tile(x, y)
        if tile:
            tile.terrain = terrain

    def get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbors.append((nx, ny))
        return neighbors
