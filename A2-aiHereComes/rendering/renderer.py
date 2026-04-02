import pygame
from constants import (SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE, MAP_WIDTH, MAP_HEIGHT,
                       MINIMAP_SIZE, MINIMAP_MARGIN, TERRAIN_COLORS, Color, TerrainType)
from core.camera import Camera
from world.map import GameMap


class Renderer:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.minimap_surface = pygame.Surface((MINIMAP_SIZE, MINIMAP_SIZE))

    def render(self, game_map: GameMap, camera: Camera):
        self.screen.fill(Color.BLACK)
        self._render_terrain(game_map, camera)
        self._render_minimap(game_map, camera)

    def _render_terrain(self, game_map: GameMap, camera: Camera):
        start_col, start_row, end_col, end_row = camera.get_visible_tile_range()

        for row in range(start_row, end_row):
            for col in range(start_col, end_col):
                tile = game_map.get_tile(col, row)
                if tile is None:
                    continue
                color = TERRAIN_COLORS.get(tile.terrain, Color.GRASS)
                sx, sy = camera.world_to_screen(col * TILE_SIZE, row * TILE_SIZE)
                ix, iy = int(sx), int(sy)
                pygame.draw.rect(self.screen, color, (ix, iy, TILE_SIZE, TILE_SIZE))

                # Draw terrain decoration symbols
                if tile.terrain == TerrainType.FOREST:
                    self._draw_tree(self.screen, ix, iy)
                elif tile.terrain == TerrainType.STONE:
                    self._draw_rock(self.screen, ix, iy)

    def _draw_tree(self, surface: pygame.Surface, sx: int, sy: int):
        """Draw a small tree icon on forest tiles."""
        # Tree trunk
        trunk_color = (100, 70, 30)
        pygame.draw.rect(surface, trunk_color, (sx + 13, sy + 18, 6, 10))
        # Tree canopy (triangle)
        leaf_color = (30, 140, 30)
        pygame.draw.polygon(surface, leaf_color,
                            [(sx + 16, sy + 4), (sx + 6, sy + 20), (sx + 26, sy + 20)])
        # Highlight on canopy
        pygame.draw.polygon(surface, (50, 180, 50),
                            [(sx + 16, sy + 4), (sx + 10, sy + 16), (sx + 16, sy + 16)])

    def _draw_rock(self, surface: pygame.Surface, sx: int, sy: int):
        """Draw a rock/mountain icon on stone tiles."""
        # Main rock body
        rock_color = (180, 180, 190)
        pygame.draw.polygon(surface, rock_color,
                            [(sx + 4, sy + 26), (sx + 12, sy + 8),
                             (sx + 22, sy + 12), (sx + 28, sy + 26)])
        # Rock highlight
        pygame.draw.polygon(surface, (210, 210, 220),
                            [(sx + 12, sy + 8), (sx + 22, sy + 12), (sx + 16, sy + 14)])
        # Shadow
        pygame.draw.polygon(surface, (120, 120, 130),
                            [(sx + 4, sy + 26), (sx + 12, sy + 8),
                             (sx + 22, sy + 12), (sx + 28, sy + 26)], 1)
        # Snow cap
        pygame.draw.polygon(surface, (240, 240, 250),
                            [(sx + 14, sy + 10), (sx + 12, sy + 8),
                             (sx + 16, sy + 6), (sx + 20, sy + 10), (sx + 18, sy + 12)])

    def _render_minimap(self, game_map: GameMap, camera: Camera,
                        buildings=None, zombies=None):
        self.minimap_surface.fill(Color.BLACK)

        tile_w = MINIMAP_SIZE / game_map.width
        tile_h = MINIMAP_SIZE / game_map.height

        # Draw terrain (sample every few tiles for performance)
        step = max(1, game_map.width // MINIMAP_SIZE)
        for y in range(0, game_map.height, step):
            for x in range(0, game_map.width, step):
                tile = game_map.get_tile(x, y)
                if tile:
                    color = TERRAIN_COLORS.get(tile.terrain, Color.GRASS)
                    px = int(x * tile_w)
                    py = int(y * tile_h)
                    pw = max(1, int(step * tile_w))
                    ph = max(1, int(step * tile_h))
                    pygame.draw.rect(self.minimap_surface, color, (px, py, pw, ph))

        # Draw buildings on minimap
        if buildings:
            for b in buildings:
                bx = int(b.tile_x * tile_w)
                by = int(b.tile_y * tile_h)
                bw = max(2, int(b.tile_width * tile_w))
                bh = max(2, int(b.tile_height * tile_h))
                color = b.get_color()
                bright = tuple(min(255, c + 40) for c in color)
                pygame.draw.rect(self.minimap_surface, bright, (bx, by, bw, bh))

        # Draw zombies on minimap
        if zombies:
            for z in zombies:
                zx = int((z.x / TILE_SIZE) * tile_w)
                zy = int((z.y / TILE_SIZE) * tile_h)
                pygame.draw.rect(self.minimap_surface, (255, 50, 50),
                                 (zx, zy, max(2, int(tile_w)), max(2, int(tile_h))))

        # Draw camera viewport rectangle
        cam_x = int(camera.x / (game_map.width * TILE_SIZE) * MINIMAP_SIZE)
        cam_y = int(camera.y / (game_map.height * TILE_SIZE) * MINIMAP_SIZE)
        cam_w = int(SCREEN_WIDTH / (game_map.width * TILE_SIZE) * MINIMAP_SIZE)
        cam_h = int(SCREEN_HEIGHT / (game_map.height * TILE_SIZE) * MINIMAP_SIZE)
        pygame.draw.rect(self.minimap_surface, Color.WHITE,
                         (cam_x, cam_y, cam_w, cam_h), 1)

        # Blit minimap to screen
        mx = SCREEN_WIDTH - MINIMAP_SIZE - MINIMAP_MARGIN
        my = SCREEN_HEIGHT - MINIMAP_SIZE - MINIMAP_MARGIN
        pygame.draw.rect(self.screen, Color.UI_BORDER,
                         (mx - 2, my - 2, MINIMAP_SIZE + 4, MINIMAP_SIZE + 4), 2)
        self.screen.blit(self.minimap_surface, (mx, my))
