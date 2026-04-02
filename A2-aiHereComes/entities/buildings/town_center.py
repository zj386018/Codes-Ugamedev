import pygame
from entities.building import Building


class TownCenter(Building):
    def __init__(self, tile_x: int, tile_y: int):
        super().__init__(
            tile_x=tile_x, tile_y=tile_y,
            tile_width=3, tile_height=3,
            hp=500,
            build_cost={},
            build_time=0,
            name="城镇中心"
        )

    def get_color(self):
        return (180, 160, 110)

    def _draw_detail(self, surface: pygame.Surface, sx: int, sy: int):
        w, h = self.width, self.height  # 96x96
        cx = sx + w // 2  # center x

        # === Base / foundation ===
        pygame.draw.rect(surface, (120, 100, 70), (sx + 4, sy + h - 8, w - 8, 8))
        pygame.draw.rect(surface, (100, 80, 55), (sx + 4, sy + h - 8, w - 8, 8), 1)

        # === Two side towers ===
        for tx in [sx + 6, sx + w - 22]:
            # Tower body
            pygame.draw.rect(surface, (160, 140, 100), (tx, sy + 18, 16, h - 26))
            pygame.draw.rect(surface, (130, 110, 75), (tx, sy + 18, 16, h - 26), 1)
            # Tower window (arch)
            pygame.draw.rect(surface, (80, 130, 200), (tx + 4, sy + 34, 8, 10))
            pygame.draw.arc(surface, (80, 130, 200), (tx + 3, sy + 30, 10, 10), 0, 3.14, 2)
            pygame.draw.rect(surface, (100, 80, 55), (tx + 4, sy + 34, 8, 10), 1)
            # Tower crenellations
            for i in range(4):
                pygame.draw.rect(surface, (160, 140, 100), (tx + i * 4, sy + 12, 3, 6))
                pygame.draw.rect(surface, (130, 110, 75), (tx + i * 4, sy + 12, 3, 6), 1)
            # Tower cone roof
            points = [(tx + 8, sy + 2), (tx, sy + 14), (tx + 16, sy + 14)]
            pygame.draw.polygon(surface, (170, 60, 40), points)
            pygame.draw.polygon(surface, (140, 45, 30), points, 1)

        # === Central keep / main building ===
        keep_x, keep_y = sx + 20, sy + 28
        keep_w, keep_h = w - 40, h - 36
        pygame.draw.rect(surface, (190, 170, 120), (keep_x, keep_y, keep_w, keep_h))
        pygame.draw.rect(surface, (150, 130, 90), (keep_x, keep_y, keep_w, keep_h), 2)

        # Stone texture lines
        for ly in range(keep_y + 10, keep_y + keep_h, 12):
            pygame.draw.line(surface, (170, 150, 105), (keep_x + 2, ly), (keep_x + keep_w - 2, ly), 1)

        # === Central main roof ===
        roof_points = [
            (cx, sy + 18),
            (keep_x + 2, keep_y + 2),
            (keep_x + keep_w - 2, keep_y + 2)
        ]
        pygame.draw.polygon(surface, (180, 55, 35), roof_points)
        pygame.draw.polygon(surface, (150, 40, 25), roof_points, 2)
        # Roof ridge line
        pygame.draw.line(surface, (200, 70, 40), (cx, sy + 18), (cx, keep_y + 2), 2)

        # === Arched grand door ===
        door_x = cx - 10
        door_y = sy + h - 28
        door_w, door_h = 20, 22
        pygame.draw.rect(surface, (70, 45, 25), (door_x, door_y, door_w, door_h))
        pygame.draw.arc(surface, (70, 45, 25), (door_x - 1, door_y - 8, door_w + 2, 18), 0, 3.14, 3)
        pygame.draw.rect(surface, (50, 30, 15), (door_x, door_y, door_w, door_h), 1)
        # Door handles
        pygame.draw.circle(surface, (200, 180, 60), (cx - 3, door_y + door_h // 2), 2)
        pygame.draw.circle(surface, (200, 180, 60), (cx + 3, door_y + door_h // 2), 2)

        # === Keep windows ===
        for wx_off in [-16, 16]:
            wx = cx + wx_off - 4
            wy = keep_y + 14
            pygame.draw.rect(surface, (80, 140, 210), (wx, wy, 8, 10))
            pygame.draw.arc(surface, (80, 140, 210), (wx - 1, wy - 5, 10, 12), 0, 3.14, 2)
            pygame.draw.rect(surface, (100, 80, 55), (wx, wy, 8, 10), 1)
            # Cross bar
            pygame.draw.line(surface, (100, 80, 55), (wx, wy + 5), (wx + 8, wy + 5), 1)
            pygame.draw.line(surface, (100, 80, 55), (wx + 4, wy), (wx + 4, wy + 10), 1)

        # === Shield emblem above door ===
        shield_x, shield_y = cx, keep_y + keep_h - 18
        pygame.draw.ellipse(surface, (200, 180, 50), (shield_x - 6, shield_y, 12, 14))
        pygame.draw.ellipse(surface, (160, 140, 30), (shield_x - 6, shield_y, 12, 14), 1)
        # Sword on shield
        pygame.draw.line(surface, (100, 80, 50), (shield_x, shield_y + 2), (shield_x, shield_y + 12), 2)
        pygame.draw.line(surface, (100, 80, 50), (shield_x - 3, shield_y + 5), (shield_x + 3, shield_y + 5), 2)

        # === Central flag pole with banner ===
        flag_x = cx
        flag_top = sy + 1
        # Pole
        pygame.draw.line(surface, (100, 80, 60), (flag_x, flag_top), (flag_x, sy + 24), 2)
        # Pole ball
        pygame.draw.circle(surface, (220, 200, 60), (flag_x, flag_top), 3)
        # Banner (waving)
        banner_pts = [
            (flag_x + 2, flag_top + 3),
            (flag_x + 18, flag_top + 1),
            (flag_x + 16, flag_top + 6),
            (flag_x + 18, flag_top + 11),
            (flag_x + 2, flag_top + 9),
        ]
        pygame.draw.polygon(surface, (220, 40, 40), banner_pts)
        pygame.draw.polygon(surface, (180, 30, 30), banner_pts, 1)
        # Banner cross
        pygame.draw.line(surface, (240, 220, 180), (flag_x + 5, flag_top + 5), (flag_x + 14, flag_top + 7), 1)
        pygame.draw.line(surface, (240, 220, 180), (flag_x + 9, flag_top + 3), (flag_x + 9, flag_top + 10), 1)

        # === Wall crenellations along top edge ===
        for i in range(8):
            bx = sx + 8 + i * 10
            pygame.draw.rect(surface, (180, 160, 110), (bx, sy + 5, 6, 8))
            pygame.draw.rect(surface, (140, 120, 80), (bx, sy + 5, 6, 8), 1)

        # === Torches on each side tower ===
        for tx in [sx + 14, sx + w - 14]:
            # Torch bracket
            pygame.draw.rect(surface, (100, 80, 50), (tx - 2, sy + 50, 4, 8))
            # Flame
            pygame.draw.ellipse(surface, (255, 180, 30), (tx - 3, sy + 45, 6, 7))
            pygame.draw.ellipse(surface, (255, 240, 100), (tx - 2, sy + 47, 4, 4))
