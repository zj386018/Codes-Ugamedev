import random
from typing import Tuple
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class ScreenEffects:
    def __init__(self):
        self.shake_amount = 0.0
        self.shake_duration = 0.0
        self.shake_offset: Tuple[int, int] = (0, 0)

    def shake(self, amount: float = 5.0, duration: float = 0.3):
        self.shake_amount = amount
        self.shake_duration = duration

    def update(self, dt: float):
        if self.shake_duration > 0:
            self.shake_duration -= dt
            self.shake_offset = (
                random.randint(int(-self.shake_amount), int(self.shake_amount)),
                random.randint(int(-self.shake_amount), int(self.shake_amount))
            )
        else:
            self.shake_offset = (0, 0)

    def apply(self, surface: pygame.Surface):
        if self.shake_offset != (0, 0):
            # Create a copy and shift it
            temp = surface.copy()
            surface.fill((0, 0, 0))
            surface.blit(temp, self.shake_offset)
