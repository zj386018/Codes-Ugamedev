from typing import List, Dict, Tuple, Optional
import pygame
from entities.entity import Entity
from constants import TILE_SIZE


class Building(Entity):
    def __init__(self, tile_x: int, tile_y: int, tile_width: int, tile_height: int,
                 hp: int, build_cost: Dict[str, int], build_time: float = 0.0,
                 name: str = "Building"):
        x = tile_x * TILE_SIZE
        y = tile_y * TILE_SIZE
        width = tile_width * TILE_SIZE
        height = tile_height * TILE_SIZE
        super().__init__(x, y, width, height, hp)

        self.tile_x = tile_x
        self.tile_y = tile_y
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.build_cost = build_cost
        self.build_time = build_time
        self.name = name

        self.construction_progress = 0.0 if build_time > 0 else 1.0
        self.is_complete = build_time == 0

        # Upgrade system
        self.level = 1
        self.max_level = 3

    def get_occupied_tiles(self) -> List[Tuple[int, int]]:
        tiles = []
        for dy in range(self.tile_height):
            for dx in range(self.tile_width):
                tiles.append((self.tile_x + dx, self.tile_y + dy))
        return tiles

    def place_on_map(self, game_map):
        for tx, ty in self.get_occupied_tiles():
            tile = game_map.get_tile(tx, ty)
            if tile:
                tile.building = self

    def remove_from_map(self, game_map):
        for tx, ty in self.get_occupied_tiles():
            tile = game_map.get_tile(tx, ty)
            if tile and tile.building is self:
                tile.building = None

    def update(self, dt: float):
        if not self.is_complete:
            self.construction_progress += dt / self.build_time
            if self.construction_progress >= 1.0:
                self.construction_progress = 1.0
                self.is_complete = True
                self.on_complete()
        return None

    def on_complete(self):
        pass

    def get_color(self) -> Tuple[int, int, int]:
        return (150, 150, 150)

    def draw(self, surface: pygame.Surface, camera):
        sx, sy = camera.world_to_screen(self.x, self.y)

        # Building body
        color = self.get_color()
        if not self.is_complete:
            color = tuple(c // 2 for c in color)

        # Draw main body
        pygame.draw.rect(surface, color,
                         (int(sx), int(sy), self.width, self.height))
        pygame.draw.rect(surface, (0, 0, 0),
                         (int(sx), int(sy), self.width, self.height), 2)

        # Draw inner detail border
        inner_color = tuple(min(255, c + 30) for c in color)
        pygame.draw.rect(surface, inner_color,
                         (int(sx) + 3, int(sy) + 3, self.width - 6, self.height - 6), 1)

        # Draw building-specific detail/icon
        if self.is_complete:
            self._draw_detail(surface, int(sx), int(sy))
            # Draw level indicator (stars in top-right)
            if self.level > 1:
                star_font = pygame.font.SysFont(None, 16)
                star_text = "★" * (self.level - 1)
                star_surf = star_font.render(star_text, True, (255, 220, 50))
                surface.blit(star_surf, (int(sx) + self.width - star_surf.get_width() - 2,
                                         int(sy) + 2))

        # Construction progress bar
        if not self.is_complete:
            bar_w = self.width
            bar_h = 4
            bar_y = int(sy) + self.height // 2 - bar_h // 2
            pygame.draw.rect(surface, (60, 60, 60), (int(sx), bar_y, bar_w, bar_h))
            fill_w = int(bar_w * self.construction_progress)
            pygame.draw.rect(surface, (255, 255, 0), (int(sx), bar_y, fill_w, bar_h))

        # HP bar (only if damaged)
        if self.hp < self.max_hp:
            bar_w = self.width
            bar_h = 3
            bar_y = int(sy) - 5
            pygame.draw.rect(surface, (60, 0, 0), (int(sx), bar_y, bar_w, bar_h))
            hp_ratio = self.hp / self.max_hp
            hp_color = (0, 200, 0) if hp_ratio > 0.5 else (200, 200, 0) if hp_ratio > 0.25 else (200, 0, 0)
            pygame.draw.rect(surface, hp_color, (int(sx), bar_y, int(bar_w * hp_ratio), bar_h))

    def _draw_detail(self, surface: pygame.Surface, sx: int, sy: int):
        """Override in subclasses to draw building-specific details."""
        pass

    def can_upgrade(self) -> bool:
        return self.level < self.max_level and self.is_complete

    def get_upgrade_cost(self) -> Dict[str, int]:
        """Override in subclasses. Returns cost dict for next upgrade."""
        return {}

    def upgrade(self):
        """Override in subclasses to apply upgrade effects."""
        pass
