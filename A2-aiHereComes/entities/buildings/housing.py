import pygame
from entities.building import Building


class House(Building):
    def __init__(self, tile_x: int, tile_y: int):
        super().__init__(
            tile_x=tile_x, tile_y=tile_y,
            tile_width=2, tile_height=2,
            hp=80,
            build_cost={"wood": 30, "stone": 10},
            build_time=5,
            name="民居"
        )
        self.population_bonus = 5

    def on_complete(self):
        pass  # Handled by BuildSystem

    def get_color(self):
        return (170, 130, 80)

    def _draw_detail(self, surface: pygame.Surface, sx: int, sy: int):
        w, h = self.width, self.height

        # Roof
        roof_color = (150, 60, 40)
        points = [(sx + w // 2, sy + 6), (sx + 6, sy + 22), (sx + w - 6, sy + 22)]
        pygame.draw.polygon(surface, roof_color, points)
        pygame.draw.polygon(surface, (120, 40, 30), points, 1)

        # Door
        pygame.draw.rect(surface, (90, 55, 25), (sx + w // 2 - 5, sy + h - 14, 10, 12))

        # Windows
        for wx in [sx + 12, sx + w - 20]:
            pygame.draw.rect(surface, (150, 200, 255), (wx, sy + 28, 7, 7))
            pygame.draw.line(surface, (80, 80, 80), (wx + 3, sy + 28), (wx + 3, sy + 35), 1)
            pygame.draw.line(surface, (80, 80, 80), (wx, sy + 31), (wx + 7, sy + 31), 1)
