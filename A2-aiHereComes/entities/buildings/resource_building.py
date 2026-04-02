import math
import pygame
from typing import Dict
from entities.building import Building


class ResourceBuilding(Building):
    def __init__(self, tile_x: int, tile_y: int, tile_width: int, tile_height: int,
                 hp: int, build_cost: Dict[str, int], build_time: float,
                 name: str, production: Dict[str, int], color: tuple):
        super().__init__(
            tile_x=tile_x, tile_y=tile_y,
            tile_width=tile_width, tile_height=tile_height,
            hp=hp, build_cost=build_cost, build_time=build_time, name=name
        )
        self.production = production  # e.g. {"food": 5} means 5 per 10s
        self.production_timer = 0.0
        self.building_color = color
        self.base_production = dict(production)  # store base for scaling

    def get_upgrade_cost(self) -> Dict[str, int]:
        """Override in each resource building subclass."""
        return {}

    def upgrade(self):
        # Increase production by 50% of base per level
        for res in self.production:
            self.production[res] = self.base_production[res] + self.base_production[res] * (self.level) // 2
        self.level += 1

    def update(self, dt):
        super().update(dt)
        if self.is_complete:
            self.production_timer += dt
            if self.production_timer >= 10.0:
                self.production_timer -= 10.0
                return dict(self.production)
        return None

    def get_color(self):
        return self.building_color


class Farm(ResourceBuilding):
    UPGRADE_COSTS = {
        1: {"wood": 15, "gold": 10},
        2: {"wood": 25, "gold": 20},
    }

    def __init__(self, tile_x: int, tile_y: int):
        super().__init__(
            tile_x=tile_x, tile_y=tile_y,
            tile_width=2, tile_height=2,
            hp=50,
            build_cost={"wood": 20, "stone": 5},
            build_time=4,
            name="农场",
            production={"food": 5},
            color=(120, 160, 50)
        )

    def get_upgrade_cost(self) -> Dict[str, int]:
        return self.UPGRADE_COSTS.get(self.level, {})

    def _draw_detail(self, surface: pygame.Surface, sx: int, sy: int):
        w, h = self.width, self.height
        # Crop rows
        for row in range(3):
            ry = sy + 12 + row * 14
            for col in range(5):
                cx = sx + 8 + col * 10
                # Wheat stalks
                pygame.draw.line(surface, (200, 190, 60), (cx, ry + 8), (cx, ry), 1)
                pygame.draw.circle(surface, (220, 200, 80), (cx, ry), 2)

        # Fence around edge
        fence_color = (140, 110, 70)
        pygame.draw.rect(surface, fence_color, (sx + 2, sy + 2, w - 4, h - 4), 1)


class LumberMill(ResourceBuilding):
    UPGRADE_COSTS = {
        1: {"wood": 15, "gold": 10},
        2: {"wood": 25, "gold": 20},
    }

    def __init__(self, tile_x: int, tile_y: int):
        super().__init__(
            tile_x=tile_x, tile_y=tile_y,
            tile_width=2, tile_height=2,
            hp=60,
            build_cost={"wood": 15, "stone": 10},
            build_time=4,
            name="伐木场",
            production={"wood": 8},
            color=(100, 70, 40)
        )

    def get_upgrade_cost(self) -> Dict[str, int]:
        return self.UPGRADE_COSTS.get(self.level, {})

    def _draw_detail(self, surface: pygame.Surface, sx: int, sy: int):
        w, h = self.width, self.height  # 64x64

        # === Small shed roof (top-left) ===
        shed_color = (90, 60, 30)
        roof_pts = [(sx + 4, sy + 14), (sx + 30, sy + 6), (sx + 56, sy + 14)]
        pygame.draw.polygon(surface, shed_color, roof_pts)
        pygame.draw.polygon(surface, (70, 45, 20), roof_pts, 2)
        # Roof ridge
        pygame.draw.line(surface, (80, 55, 25), (sx + 30, sy + 6), (sx + 30, sy + 14), 2)

        # === Stacked log pile (left side, 4 layers) ===
        # Bottom layer - 3 logs
        log_dark = (100, 70, 35)
        log_mid = (130, 90, 50)
        log_light = (155, 110, 65)
        log_r = 6  # log radius height
        log_w = 28  # log length

        # Layer 1 (bottom) - 3 horizontal logs
        base_y = sy + h - 12
        for i in range(3):
            lx = sx + 6 + i * (log_w // 3 + 2)
            # Log body
            pygame.draw.ellipse(surface, log_mid, (lx, base_y, log_w // 3 + 4, log_r * 2))
            pygame.draw.ellipse(surface, log_dark, (lx, base_y, log_w // 3 + 4, log_r * 2), 1)
            # Ring on end face
            pygame.draw.ellipse(surface, log_light,
                                (lx + log_w // 6, base_y + 2, log_w // 6, log_r), 1)

        # Layer 2 - 3 logs
        base_y2 = base_y - log_r * 2 + 2
        for i in range(3):
            lx = sx + 8 + i * (log_w // 3 + 2)
            pygame.draw.ellipse(surface, log_mid, (lx, base_y2, log_w // 3 + 4, log_r * 2))
            pygame.draw.ellipse(surface, log_dark, (lx, base_y2, log_w // 3 + 4, log_r * 2), 1)
            pygame.draw.ellipse(surface, log_light,
                                (lx + log_w // 6, base_y2 + 2, log_w // 6, log_r), 1)

        # Layer 3 - 2 logs
        base_y3 = base_y2 - log_r * 2 + 2
        for i in range(2):
            lx = sx + 12 + i * (log_w // 3 + 3)
            pygame.draw.ellipse(surface, log_mid, (lx, base_y3, log_w // 3 + 4, log_r * 2))
            pygame.draw.ellipse(surface, log_dark, (lx, base_y3, log_w // 3 + 4, log_r * 2), 1)
            pygame.draw.ellipse(surface, log_light,
                                (lx + log_w // 6, base_y3 + 2, log_w // 6, log_r), 1)

        # Layer 4 - 1 log on top
        base_y4 = base_y3 - log_r * 2 + 2
        pygame.draw.ellipse(surface, log_mid, (sx + 16, base_y4, log_w // 3 + 4, log_r * 2))
        pygame.draw.ellipse(surface, log_dark, (sx + 16, base_y4, log_w // 3 + 4, log_r * 2), 1)
        pygame.draw.ellipse(surface, log_light,
                            (sx + 16 + log_w // 6, base_y4 + 2, log_w // 6, log_r), 1)

        # === Processed timber planks (right side) ===
        plank_color = (170, 130, 75)
        plank_dark = (140, 100, 55)
        # 3 stacked planks
        for i in range(3):
            py = sy + 20 + i * 8
            pygame.draw.rect(surface, plank_color, (sx + w - 26, py, 20, 6))
            pygame.draw.rect(surface, plank_dark, (sx + w - 26, py, 20, 6), 1)
            # Wood grain lines
            pygame.draw.line(surface, plank_dark, (sx + w - 22, py + 2), (sx + w - 10, py + 2), 1)

        # === Axe (right side) ===
        axe_x = sx + w - 10
        axe_y = sy + 18
        # Handle
        pygame.draw.line(surface, (110, 80, 45), (axe_x, axe_y), (axe_x - 6, axe_y + 18), 2)
        # Blade
        pygame.draw.polygon(surface, (180, 180, 190),
                            [(axe_x + 1, axe_y - 2), (axe_x + 6, axe_y + 2),
                             (axe_x + 1, axe_y + 6)])
        pygame.draw.polygon(surface, (150, 150, 160),
                            [(axe_x + 1, axe_y - 2), (axe_x + 6, axe_y + 2),
                             (axe_x + 1, axe_y + 6)], 1)

        # === Saw blade circle (center) ===
        saw_cx, saw_cy = sx + w - 16, sy + h - 14
        pygame.draw.circle(surface, (170, 170, 180), (saw_cx, saw_cy), 8, 2)
        # Saw teeth
        for angle_idx in range(6):
            a = angle_idx * math.pi / 3
            tx = saw_cx + int(9 * math.cos(a))
            ty = saw_cy + int(9 * math.sin(a))
            pygame.draw.circle(surface, (150, 150, 160), (tx, ty), 1)
        # Center hole
        pygame.draw.circle(surface, (100, 100, 110), (saw_cx, saw_cy), 2)


class Quarry(ResourceBuilding):
    UPGRADE_COSTS = {
        1: {"stone": 15, "gold": 10},
        2: {"stone": 25, "gold": 20},
    }

    def __init__(self, tile_x: int, tile_y: int):
        super().__init__(
            tile_x=tile_x, tile_y=tile_y,
            tile_width=2, tile_height=2,
            hp=80,
            build_cost={"wood": 20, "stone": 5},
            build_time=5,
            name="采石场",
            production={"stone": 6},
            color=(140, 140, 150)
        )

    def get_upgrade_cost(self) -> Dict[str, int]:
        return self.UPGRADE_COSTS.get(self.level, {})

    def _draw_detail(self, surface: pygame.Surface, sx: int, sy: int):
        w, h = self.width, self.height  # 64x64

        # === Rock quarry face (right side - cliff wall) ===
        cliff_color = (130, 130, 140)
        cliff_dark = (100, 100, 110)
        cliff_light = (160, 160, 170)
        # Vertical cliff face
        pygame.draw.rect(surface, cliff_color, (sx + w - 20, sy + 6, 16, h - 16))
        pygame.draw.rect(surface, cliff_dark, (sx + w - 20, sy + 6, 16, h - 16), 1)
        # Horizontal strata lines
        for ly in range(sy + 14, sy + h - 12, 8):
            pygame.draw.line(surface, cliff_dark, (sx + w - 18, ly), (sx + w - 6, ly), 1)
        # Highlight on left edge
        pygame.draw.line(surface, cliff_light, (sx + w - 20, sy + 7), (sx + w - 20, sy + h - 11), 1)

        # === Stacked raw stone blocks (center-left, pyramid) ===
        stone1 = (170, 170, 180)
        stone2 = (155, 155, 165)
        stone3 = (140, 140, 150)
        stone_outline = (110, 110, 120)

        # Bottom row - 4 blocks
        base_y = sy + h - 16
        for i in range(4):
            bx = sx + 6 + i * 11
            pts = [(bx, base_y + 10), (bx + 3, base_y), (bx + 10, base_y - 2),
                   (bx + 13, base_y + 8)]
            pygame.draw.polygon(surface, stone1 if i % 2 == 0 else stone2, pts)
            pygame.draw.polygon(surface, stone_outline, pts, 1)
            # Highlight
            pygame.draw.line(surface, stone1, (bx + 3, base_y + 1), (bx + 9, base_y - 1), 1)

        # Second row - 3 blocks
        base_y2 = base_y - 14
        for i in range(3):
            bx = sx + 10 + i * 11
            pts = [(bx, base_y2 + 10), (bx + 4, base_y2), (bx + 11, base_y2 - 2),
                   (bx + 14, base_y2 + 8)]
            pygame.draw.polygon(surface, stone2 if i % 2 == 0 else stone1, pts)
            pygame.draw.polygon(surface, stone_outline, pts, 1)
            pygame.draw.line(surface, stone1, (bx + 4, base_y2 + 1), (bx + 10, base_y2 - 1), 1)

        # Third row - 2 blocks
        base_y3 = base_y2 - 13
        for i in range(2):
            bx = sx + 14 + i * 12
            pts = [(bx, base_y3 + 10), (bx + 4, base_y3), (bx + 12, base_y3 - 3),
                   (bx + 15, base_y3 + 7)]
            pygame.draw.polygon(surface, stone3, pts)
            pygame.draw.polygon(surface, stone_outline, pts, 1)
            pygame.draw.line(surface, stone2, (bx + 4, base_y3 + 1), (bx + 11, base_y3 - 2), 1)

        # Top cap stone
        top_y = base_y3 - 10
        pts = [(sx + 22, top_y + 8), (sx + 26, top_y), (sx + 34, top_y - 2),
               (sx + 38, top_y + 6)]
        pygame.draw.polygon(surface, stone3, pts)
        pygame.draw.polygon(surface, stone_outline, pts, 1)

        # === Loose rubble/fragments (bottom-left) ===
        rubble_color = (150, 150, 160)
        for rx, ry in [(sx + 4, sy + h - 6), (sx + 10, sy + h - 8),
                        (sx + 18, sy + h - 5), (sx + 26, sy + h - 7)]:
            pygame.draw.polygon(surface, rubble_color,
                                [(rx, ry), (rx + 3, ry - 3), (rx + 6, ry), (rx + 3, ry + 2)])
            pygame.draw.polygon(surface, stone_outline,
                                [(rx, ry), (rx + 3, ry - 3), (rx + 6, ry), (rx + 3, ry + 2)], 1)

        # === Pickaxe (top-left) ===
        px, py = sx + 10, sy + 8
        # Handle
        pygame.draw.line(surface, (130, 90, 50), (px, py), (px + 14, py + 18), 2)
        # Metal head
        pygame.draw.line(surface, (180, 180, 190), (px + 2, py + 2), (px - 4, py - 4), 3)
        pygame.draw.line(surface, (180, 180, 190), (px + 2, py + 2), (px + 8, py - 2), 3)
        # Pick point highlight
        pygame.draw.circle(surface, (200, 200, 210), (px - 4, py - 4), 1)


class GoldMine(ResourceBuilding):
    UPGRADE_COSTS = {
        1: {"stone": 20, "gold": 15},
        2: {"stone": 30, "gold": 30},
    }

    def __init__(self, tile_x: int, tile_y: int):
        super().__init__(
            tile_x=tile_x, tile_y=tile_y,
            tile_width=1, tile_height=1,
            hp=60,
            build_cost={"wood": 30, "stone": 20},
            build_time=6,
            name="金矿",
            production={"gold": 3},
            color=(160, 140, 50)
        )

    def get_upgrade_cost(self) -> Dict[str, int]:
        return self.UPGRADE_COSTS.get(self.level, {})

    def _draw_detail(self, surface: pygame.Surface, sx: int, sy: int):
        # Mine entrance (dark arch)
        pygame.draw.rect(surface, (60, 50, 30), (sx + 8, sy + 10, 16, 14))
        pygame.draw.arc(surface, (40, 30, 20), (sx + 8, sy + 6, 16, 12), 0, 3.14, 2)

        # Gold nugget sparkles
        for gx, gy in [(sx + 12, sy + 16), (sx + 20, sy + 20), (sx + 8, sy + 22)]:
            pygame.draw.circle(surface, (255, 220, 50), (gx, gy), 2)

        # Pickaxe symbol
        pygame.draw.line(surface, (160, 160, 170), (sx + 4, sy + 6), (sx + 12, sy + 14), 1)
