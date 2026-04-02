import pygame
from typing import Dict
from entities.building import Building


class Wall(Building):
    UPGRADE_COSTS = {
        1: {"stone": 15, "gold": 10},
        2: {"stone": 25, "gold": 20},
    }

    def __init__(self, tile_x: int, tile_y: int):
        super().__init__(
            tile_x=tile_x, tile_y=tile_y,
            tile_width=1, tile_height=1,
            hp=200,
            build_cost={"wood": 10, "stone": 5},
            build_time=2,
            name="城墙"
        )

    def get_upgrade_cost(self) -> Dict[str, int]:
        return self.UPGRADE_COSTS.get(self.level, {})

    def upgrade(self):
        self.max_hp += 100
        self.hp = self.max_hp
        self.level += 1

    def get_color(self):
        return (140, 120, 100)

    def _draw_detail(self, surface: pygame.Surface, sx: int, sy: int):
        # Stone block pattern
        pygame.draw.line(surface, (100, 80, 60), (sx + 4, sy + 8), (sx + 12, sy + 8), 1)
        pygame.draw.line(surface, (100, 80, 60), (sx + 8, sy + 4), (sx + 8, sy + 12), 1)
        pygame.draw.line(surface, (100, 80, 60), (sx + 18, sy + 16), (sx + 28, sy + 16), 1)
        pygame.draw.line(surface, (100, 80, 60), (sx + 22, sy + 12), (sx + 22, sy + 22), 1)
        # Highlight
        pygame.draw.line(surface, (170, 150, 120), (sx + 3, sy + 3), (sx + 28, sy + 3), 1)
