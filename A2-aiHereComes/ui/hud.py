import pygame
from constants import Color, SCREEN_WIDTH, get_font
from systems.resource_manager import ResourceManager


class HUD:
    def __init__(self, resource_manager: ResourceManager):
        self.resource_manager = resource_manager
        self.font = get_font(18)
        self.label_font = get_font(14)
        self.height = 30  # top bar height
        self.panel_width = 140  # left panel width
        self.panel_x = 0
        self.panel_y = 30  # starts below top bar
        self.line_height = 22
        self.zombie_count = 0

    def draw(self, surface: pygame.Surface):
        # Top bar (wave info area)
        pygame.draw.rect(surface, Color.UI_BG, (0, 0, SCREEN_WIDTH, self.height))
        pygame.draw.line(surface, Color.UI_BORDER, (0, self.height), (SCREEN_WIDTH, self.height))

        # Left vertical resource panel
        resources = [
            ("木材", "wood", (139, 90, 43)),
            ("石头", "stone", (150, 150, 150)),
            ("金币", "gold", (255, 215, 0)),
            ("食物", "food", (100, 200, 50)),
        ]

        panel_h = len(resources) * self.line_height + 10 + self.line_height + 8

        # Semi-transparent background
        bg = pygame.Surface((self.panel_width, panel_h), pygame.SRCALPHA)
        bg.fill((*Color.UI_BG, 200))
        surface.blit(bg, (self.panel_x, self.panel_y))
        pygame.draw.rect(surface, Color.UI_BORDER,
                         (self.panel_x, self.panel_y, self.panel_width, panel_h), 1)

        y = self.panel_y + 5
        x = self.panel_x + 8

        for label, res_type, color in resources:
            amount = self.resource_manager.resources.get(res_type, 0)
            cap = self.resource_manager.resource_caps.get(res_type, 0)

            # Color dot indicator
            pygame.draw.circle(surface, color, (x + 5, y + 9), 4)
            pygame.draw.circle(surface, (0, 0, 0), (x + 5, y + 9), 4, 1)

            # Label
            label_surf = self.label_font.render(label, True, color)
            surface.blit(label_surf, (x + 12, y))

            # Value
            value_text = f"{amount}/{cap}"
            value_surf = self.label_font.render(value_text, True, Color.UI_TEXT)
            surface.blit(value_surf, (x + 12 + label_surf.get_width() + 4, y))

            y += self.line_height

        # Population
        pygame.draw.circle(surface, Color.UI_TEXT, (x + 5, y + 9), 4)
        pygame.draw.circle(surface, (0, 0, 0), (x + 5, y + 9), 4, 1)
        pop_text = f"人口: {self.resource_manager.population}/{self.resource_manager.max_population}"
        pop_surf = self.label_font.render(pop_text, True, Color.UI_TEXT)
        surface.blit(pop_surf, (x + 12, y))
