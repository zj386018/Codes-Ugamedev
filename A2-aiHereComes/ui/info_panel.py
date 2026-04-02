from typing import Optional
import pygame
from constants import Color, TILE_SIZE, get_font
from entities.building import Building
from entities.zombie import Zombie
from entities.buildings.tower import Tower

RESOURCE_CN = {
    "wood": "木材", "stone": "石头", "gold": "金币", "food": "食物",
}
ZOMBIE_CN = {
    "basic": "普通", "runner": "跑步者", "tank": "坦克",
    "spitter": "喷射者", "boss": "Boss",
}


class InfoPanel:
    def __init__(self):
        self.visible = False
        self.selected: Optional[object] = None
        self.font = get_font(20)
        self.title_font = get_font(24)
        self.panel_width = 200
        self.panel_x = 10
        self.panel_y = 40

    def select(self, entity):
        self.selected = entity
        self.visible = entity is not None

    def deselect(self):
        self.selected = None
        self.visible = False

    def draw(self, surface: pygame.Surface, camera):
        if not self.visible or self.selected is None:
            return

        entity = self.selected
        x = self.panel_x
        y = self.panel_y
        w = self.panel_width

        # Panel background
        lines = []
        name = entity.name if hasattr(entity, 'name') else "实体"
        lines.append((name, self.title_font, Color.UI_TEXT))

        # HP
        hp_text = f"生命: {entity.hp}/{entity.max_hp}"
        hp_color = Color.HP_GREEN if entity.hp > entity.max_hp * 0.5 else Color.HP_YELLOW if entity.hp > entity.max_hp * 0.25 else Color.HP_RED
        lines.append((hp_text, self.font, hp_color))

        if isinstance(entity, Building):
            if isinstance(entity, Tower):
                lines.append((f"攻击: {entity.attack_damage}", self.font, Color.UI_TEXT))
                lines.append((f"射程: {entity.attack_range} 格", self.font, Color.UI_TEXT))
                lines.append((f"攻速: {entity.attack_speed}/秒", self.font, Color.UI_TEXT))

                # Draw range circle on map
                range_px = entity.attack_range * TILE_SIZE
                cx, cy = entity.center
                sx, sy = camera.world_to_screen(cx, cy)
                range_surf = pygame.Surface((int(range_px * 2), int(range_px * 2)), pygame.SRCALPHA)
                pygame.draw.circle(range_surf, (100, 150, 255, 40),
                                   (int(range_px), int(range_px)), int(range_px))
                pygame.draw.circle(range_surf, (100, 150, 255, 100),
                                   (int(range_px), int(range_px)), int(range_px), 1)
                surface.blit(range_surf, (int(sx - range_px), int(sy - range_px)))

            if hasattr(entity, 'production'):
                for res, amount in entity.production.items():
                    res_cn = RESOURCE_CN.get(res, res)
                    lines.append((f"产出: +{amount} {res_cn}/10秒", self.font, (100, 200, 50)))

            if hasattr(entity, 'population_bonus'):
                lines.append((f"人口: +{entity.population_bonus}", self.font, Color.UI_TEXT))

            if hasattr(entity, 'storage_bonus'):
                for res, bonus in entity.storage_bonus.items():
                    res_cn = RESOURCE_CN.get(res, res)
                    lines.append((f"{res_cn}: +{bonus} 容量", self.font, Color.UI_TEXT))

            if not entity.is_complete:
                pct = int(entity.construction_progress * 100)
                lines.append((f"建造中: {pct}%", self.font, (255, 255, 100)))

        elif isinstance(entity, Zombie):
            zt_cn = ZOMBIE_CN.get(entity.zombie_type, entity.zombie_type)
            lines.append((f"类型: {zt_cn}", self.font, Color.UI_TEXT))
            lines.append((f"速度: {entity.speed}", self.font, Color.UI_TEXT))
            lines.append((f"攻击: {entity.damage}", self.font, Color.UI_TEXT))

        # Calculate panel height
        h = len(lines) * 22 + 15

        # Draw panel
        panel_rect = pygame.Rect(x, y, w, h)
        bg = pygame.Surface((w, h), pygame.SRCALPHA)
        bg.fill((*Color.UI_BG, 220))
        surface.blit(bg, (x, y))
        pygame.draw.rect(surface, Color.UI_BORDER, panel_rect, 1)

        # Draw lines
        for i, (text, font, color) in enumerate(lines):
            text_surf = font.render(text, True, color)
            surface.blit(text_surf, (x + 8, y + 8 + i * 22))
