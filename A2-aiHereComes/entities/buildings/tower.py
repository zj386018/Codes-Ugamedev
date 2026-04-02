import pygame
from entities.building import Building


class Tower(Building):
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
