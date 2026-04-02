from typing import List, Tuple
import pygame
from constants import Color, get_font


class Notification:
    def __init__(self, text: str, duration: float = 3.0, color: Tuple[int, int, int] = None):
        self.text = text
        self.duration = duration
        self.max_duration = duration
        self.color = color or Color.UI_TEXT


class NotificationManager:
    def __init__(self):
        self.notifications: List[Notification] = []
        self.font = get_font(28)

    def show(self, text: str, duration: float = 3.0,
             color: Tuple[int, int, int] = None):
        self.notifications.append(Notification(text, duration, color))

    def update(self, dt: float):
        for n in self.notifications:
            n.duration -= dt
        self.notifications = [n for n in self.notifications if n.duration > 0]

    def draw(self, surface: pygame.Surface, screen_width: int):
        y = 50
        for n in self.notifications:
            alpha = min(1.0, n.duration / (n.max_duration * 0.3))
            text_surf = self.font.render(n.text, True, n.color)

            # Background
            bg_rect = text_surf.get_rect(centerx=screen_width // 2, y=y)
            bg_rect.inflate_ip(20, 10)
            bg = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg.fill((*Color.UI_BG, int(200 * alpha)))
            surface.blit(bg, bg_rect)

            # Text
            text_rect = text_surf.get_rect(centerx=screen_width // 2, y=y + 5)
            surface.blit(text_surf, text_rect)

            y += 40
