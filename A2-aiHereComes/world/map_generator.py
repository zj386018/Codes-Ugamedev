import random
import math
from typing import Optional, Tuple
from constants import MAP_WIDTH, MAP_HEIGHT, TerrainType
from world.map import GameMap


class MapGenerator:
    """Procedural map generator using simple noise-like clustering."""

    def __init__(self, seed: Optional[int] = None):
        self.rng = random.Random(seed)

    def generate(self, width: int = MAP_WIDTH, height: int = MAP_HEIGHT) -> GameMap:
        game_map = GameMap(width, height)

        # Step 1: Fill with grass
        for y in range(height):
            for x in range(width):
                game_map.set_terrain(x, y, TerrainType.GRASS)

        # Step 2: Scatter terrain patches using random walk clusters
        self._place_clusters(game_map, TerrainType.GRASS_DARK, 25, (15, 40))
        self._place_clusters(game_map, TerrainType.FOREST, 20, (8, 25))
        self._place_clusters(game_map, TerrainType.DIRT, 15, (10, 30))
        self._place_clusters(game_map, TerrainType.STONE, 12, (6, 20))
        self._place_clusters(game_map, TerrainType.WATER, 8, (5, 15))

        # Step 3: Clear starting area (center, 15x15 tiles)
        cx, cy = width // 2, height // 2
        for dy in range(-7, 8):
            for dx in range(-7, 8):
                game_map.set_terrain(cx + dx, cy + dy, TerrainType.GRASS)

        return game_map

    def _place_clusters(self, game_map: GameMap, terrain: TerrainType,
                        num_clusters: int, size_range: Tuple[int, int]):
        for _ in range(num_clusters):
            cx = self.rng.randint(0, game_map.width - 1)
            cy = self.rng.randint(0, game_map.height - 1)
            size = self.rng.randint(*size_range)

            # Random walk from center
            x, y = cx, cy
            for _ in range(size):
                if 0 <= x < game_map.width and 0 <= y < game_map.height:
                    game_map.set_terrain(x, y, terrain)
                x += self.rng.choice([-1, 0, 1])
                y += self.rng.choice([-1, 0, 1])
                x = max(0, min(x, game_map.width - 1))
                y = max(0, min(y, game_map.height - 1))

                # Also fill a small radius around the walk for natural patches
                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < game_map.width and 0 <= ny < game_map.height
                                and self.rng.random() < 0.4):
                            game_map.set_terrain(nx, ny, terrain)
