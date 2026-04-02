import pygame
from typing import Optional, Callable
from constants import Color, get_font


class Button:
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 callback: Optional[Callable] = None, font_size: int = 18):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.hovered = False
        self.selected = False
        self.font = get_font(font_size)
        self.enabled = True

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.enabled:
            return False

        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        return False

    def draw(self, surface: pygame.Surface):
        if self.selected:
            color = Color.UI_HIGHLIGHT
        elif self.hovered and self.enabled:
            color = Color.UI_BUTTON_HOVER
        elif self.enabled:
            color = Color.UI_BUTTON
        else:
            color = Color.DARK_GRAY

        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, Color.UI_BORDER, self.rect, 1)

        text_color = Color.UI_TEXT if self.enabled else Color.GRAY
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
