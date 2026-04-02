from typing import Tuple
import pygame
from constants import TILE_SIZE


class Entity:
    def __init__(self, x: float, y: float, width: int, height: int, hp: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hp = hp
        self.max_hp = hp
        self.alive = True

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    @property
    def center(self) -> Tuple[float, float]:
        return self.x + self.width / 2, self.y + self.height / 2

    @property
    def tile_pos(self) -> Tuple[int, int]:
        return int(self.x // TILE_SIZE), int(self.y // TILE_SIZE)

    def take_damage(self, amount: int):
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def update(self, dt: float):
        pass

    def draw(self, surface: pygame.Surface, camera):
        pass
