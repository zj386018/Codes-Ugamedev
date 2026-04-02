import pygame
from typing import Dict
from entities.building import Building


class Tower(Building):
    # Upgrade costs: level -> cost dict
    WOOD_UPGRADE_COSTS = {
        1: {"wood": 20, "gold": 15},
        2: {"wood": 30, "gold": 25},
    }
    STONE_UPGRADE_COSTS = {
        1: {"stone": 20, "gold": 20},
        2: {"stone": 35, "gold": 35},
    }

    def __init__(self, tile_x: int, tile_y: int, tower_type: str = "wood"):
        if tower_type == "stone":
            super().__init__(
                tile_x=tile_x, tile_y=tile_y,
                tile_width=1, tile_height=1,
                hp=200,
                build_cost={"wood": 10, "stone": 40},
                build_time=8,
                name="石箭塔"
            )
            self.attack_range = 7
            self.attack_damage = 15
            self.attack_speed = 0.8
            self.tower_color = (120, 120, 130)
            self.tower_type = "stone"
        else:
            super().__init__(
                tile_x=tile_x, tile_y=tile_y,
                tile_width=1, tile_height=1,
                hp=100,
                build_cost={"wood": 30, "stone": 10},
                build_time=5,
                name="木箭塔"
            )
            self.attack_range = 5
            self.attack_damage = 10
            self.attack_speed = 1.0
            self.tower_color = (160, 100, 50)
            self.tower_type = "wood"

        self.attack_timer = 0.0
        self.target = None

    def get_upgrade_cost(self) -> Dict[str, int]:
        costs = self.STONE_UPGRADE_COSTS if self.tower_type == "stone" else self.WOOD_UPGRADE_COSTS
        return costs.get(self.level, {})

    def upgrade(self):
        if self.tower_type == "stone":
            self.max_hp += 80
            self.hp = self.max_hp
            self.attack_damage += 8
            self.attack_range += 1
        else:
            self.max_hp += 50
            self.hp = self.max_hp
            self.attack_damage += 5
            self.attack_range += 1
        self.level += 1

    def get_color(self):
        return self.tower_color

    def get_symbol(self):
        return "T"

    def _draw_detail(self, surface: pygame.Surface, sx: int, sy: int):
        # Tower base (darker rectangle in center)
        base_color = tuple(max(0, c - 40) for c in self.tower_color)
        pygame.draw.rect(surface, base_color,
                         (sx + 8, sy + 8, 16, 16))

        # Crenellations (battlements) on top
        crenel_color = tuple(min(255, c + 20) for c in self.tower_color)
        for cx in [sx + 6, sx + 14, sx + 22]:
            pygame.draw.rect(surface, crenel_color, (cx, sy + 4, 4, 6))

        # Arrow slit (center)
        pygame.draw.rect(surface, (40, 40, 40), (sx + 14, sy + 12, 4, 8))
        pygame.draw.rect(surface, (40, 40, 40), (sx + 12, sy + 14, 8, 4))
