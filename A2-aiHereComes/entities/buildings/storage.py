import pygame
from typing import Dict
from entities.building import Building


class Storage(Building):
    def __init__(self, tile_x: int, tile_y: int):
        super().__init__(
            tile_x=tile_x, tile_y=tile_y,
            tile_width=2, tile_height=2,
            hp=100,
            build_cost={"wood": 20, "stone": 20},
            build_time=6,
            name="仓库"
        )
        self.storage_bonus: Dict[str, int] = {
            "wood": 200, "stone": 200, "gold": 100, "food": 150
        }

    def on_complete(self):
        pass  # Handled by BuildSystem

    def get_color(self):
        return (130, 90, 60)

    def _draw_detail(self, surface: pygame.Surface, sx: int, sy: int):
        w, h = self.width, self.height

        # Barn roof
        roof_color = (100, 60, 30)
        points = [(sx + w // 2, sy + 6), (sx + 6, sy + 22), (sx + w - 6, sy + 22)]
        pygame.draw.polygon(surface, roof_color, points)
        pygame.draw.polygon(surface, (80, 45, 20), points, 1)

        # Double doors
        door_color = (80, 50, 25)
        pygame.draw.rect(surface, door_color, (sx + w // 2 - 8, sy + h - 16, 7, 12))
        pygame.draw.rect(surface, door_color, (sx + w // 2 + 1, sy + h - 16, 7, 12))
        pygame.draw.rect(surface, (60, 35, 15), (sx + w // 2 - 8, sy + h - 16, 16, 12), 1)

        # Crate/barrel icons on sides
        barrel_color = (150, 110, 60)
        pygame.draw.circle(surface, barrel_color, (sx + 14, sy + 30), 5)
        pygame.draw.circle(surface, (120, 85, 45), (sx + 14, sy + 30), 5, 1)
        pygame.draw.circle(surface, barrel_color, (sx + w - 14, sy + 30), 5)
        pygame.draw.circle(surface, (120, 85, 45), (sx + w - 14, sy + 30), 5, 1)
