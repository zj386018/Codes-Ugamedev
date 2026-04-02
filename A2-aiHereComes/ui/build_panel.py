from typing import Dict, List, Callable, Optional
import pygame
from constants import Color, SCREEN_WIDTH, TILE_SIZE, get_font
from ui.button import Button


class BuildPanel:
    CATEGORIES = [
        ("城镇", ["house", "storage"]),
        ("资源", ["farm", "lumber_mill", "quarry", "gold_mine"]),
        ("防御", ["wall", "wood_tower", "stone_tower"]),
    ]

    BUILDING_INFO = {
        "wall":        ("城墙",      "10木 5石",    (140, 120, 100), "阻挡僵尸前进"),
        "wood_tower":  ("木箭塔",   "30木 10石",   (160, 100, 50),  "自动射击僵尸"),
        "stone_tower": ("石箭塔",   "10木 40石",   (120, 120, 130), "高伤害远程塔"),
        "farm":        ("农场",      "20木 5石",    (180, 180, 60),  "+5 食物/10秒"),
        "lumber_mill": ("伐木场",   "15木 10石",   (100, 70, 40),   "+8 木材/10秒"),
        "quarry":      ("采石场",   "20木 5石",    (160, 160, 170), "+6 石头/10秒"),
        "gold_mine":   ("金矿",     "30木 20石",   (200, 180, 50),  "+3 金币/10秒"),
        "house":       ("民居",      "30木 10石",   (170, 130, 80),  "+5 人口上限"),
        "storage":     ("仓库",      "20木 20石",   (130, 90, 60),   "+资源容量上限"),
    }

    def __init__(self, on_select: Callable[[Optional[str]], None],
                 on_repair: Optional[Callable[[], None]] = None):
        self.on_select = on_select
        self.on_repair = on_repair
        self.selected: Optional[str] = None
        self.visible = True
        self.panel_height = 65
        self.active_category = 0  # index into CATEGORIES

        # Category tab state
        self.tab_font = get_font(14)
        self.repair_font = get_font(14)

        # Create building buttons (all, show/hide by category)
        self.buttons: Dict[str, Button] = {}
        for key, info in self.BUILDING_INFO.items():
            btn = Button(
                x=0, y=0, width=72, height=22,
                text=info[0],
                callback=lambda k=key: self._on_button_click(k),
                font_size=14
            )
            self.buttons[key] = btn

    def _on_button_click(self, building_type: str):
        if self.selected == building_type:
            self.selected = None
            self.on_select(None)
        else:
            self.selected = building_type
            self.on_select(building_type)
        self._update_button_states()

    def _update_button_states(self):
        for key, btn in self.buttons.items():
            btn.selected = (key == self.selected)

    def deselect(self):
        self.selected = None
        self._update_button_states()

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.visible:
            return False

        # Check category tabs
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            # Tab click detection (computed in draw)
            tab_y = self._panel_y + 3
            tab_x = 10
            for i, (cat_name, _) in enumerate(self.CATEGORIES):
                tab_w = self.tab_font.render(cat_name, True, Color.UI_TEXT).get_width() + 16
                tab_rect = pygame.Rect(tab_x, tab_y, tab_w, 18)
                if tab_rect.collidepoint(mx, my):
                    self.active_category = i
                    return True
                tab_x += tab_w + 4

            # Repair button click
            repair_x = SCREEN_WIDTH - 100
            repair_rect = pygame.Rect(repair_x, tab_y, 88, 18)
            if repair_rect.collidepoint(mx, my) and self.on_repair:
                self.on_repair()
                return True

        # Check building buttons (only active category)
        _, active_keys = self.CATEGORIES[self.active_category]
        for key in active_keys:
            if key in self.buttons and self.buttons[key].handle_event(event):
                return True
        return False

    def draw(self, surface: pygame.Surface, screen_height: int):
        if not self.visible:
            return

        self._panel_y = screen_height - self.panel_height
        panel_y = self._panel_y

        # Panel background
        pygame.draw.rect(surface, Color.UI_BG,
                         (0, panel_y, SCREEN_WIDTH, self.panel_height))
        pygame.draw.line(surface, Color.UI_BORDER,
                         (0, panel_y), (SCREEN_WIDTH, panel_y))

        # === Row 0: Category tabs + Repair button ===
        tab_y = panel_y + 3
        tab_x = 10
        for i, (cat_name, _) in enumerate(self.CATEGORIES):
            tab_text = self.tab_font.render(cat_name, True, Color.UI_TEXT)
            tab_w = tab_text.get_width() + 16
            tab_rect = pygame.Rect(tab_x, tab_y, tab_w, 18)

            if i == self.active_category:
                pygame.draw.rect(surface, Color.UI_HIGHLIGHT, tab_rect)
            else:
                pygame.draw.rect(surface, Color.UI_BUTTON, tab_rect)
            pygame.draw.rect(surface, Color.UI_BORDER, tab_rect, 1)

            surface.blit(tab_text, (tab_x + 8, tab_y + 2))
            tab_x += tab_w + 4

        # Repair button
        repair_x = SCREEN_WIDTH - 100
        repair_rect = pygame.Rect(repair_x, tab_y, 88, 18)
        pygame.draw.rect(surface, (80, 130, 80), repair_rect)
        pygame.draw.rect(surface, (100, 160, 100), repair_rect, 1)
        repair_text = self.repair_font.render("修复全部", True, Color.UI_TEXT)
        surface.blit(repair_text,
                     (repair_x + repair_rect.width // 2 - repair_text.get_width() // 2,
                      tab_y + 2))

        # === Row 1: Building buttons for active category ===
        _, active_keys = self.CATEGORIES[self.active_category]
        btn_width = 72
        btn_height = 22
        btn_y = panel_y + 24
        for j, key in enumerate(active_keys):
            btn = self.buttons[key]
            btn.rect.x = 10 + j * (btn_width + 4)
            btn.rect.y = btn_y
            btn.rect.width = btn_width
            btn.rect.height = btn_height
            btn.draw(surface)

        # === Selected building info (right side) ===
        if self.selected and self.selected in self.BUILDING_INFO:
            info = self.BUILDING_INFO[self.selected]
            font = get_font(18)
            desc_font = get_font(16)

            preview_x = SCREEN_WIDTH - 200
            preview_y = panel_y + 24

            # Color preview + name
            pygame.draw.rect(surface, info[2], (preview_x, preview_y, 16, 16))
            pygame.draw.rect(surface, Color.UI_BORDER, (preview_x, preview_y, 16, 16), 1)

            name_surf = font.render(info[0], True, Color.UI_TEXT)
            surface.blit(name_surf, (preview_x + 22, preview_y))

            # Cost
            cost_surf = font.render(f"费用: {info[1]}", True, (200, 200, 150))
            surface.blit(cost_surf, (preview_x, preview_y + 20))

            # Description
            desc_surf = desc_font.render(info[3], True, Color.GRAY)
            surface.blit(desc_surf, (preview_x, preview_y + 38))
