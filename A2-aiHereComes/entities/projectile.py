import math
from typing import Tuple
import pygame
from entities.entity import Entity


class Projectile(Entity):
    def __init__(self, x: float, y: float, target_x: float, target_y: float,
                 speed: float = 300.0, damage: int = 10, splash_radius: float = 0):
        super().__init__(x, y, 6, 6, 1)  # Small size, irrelevant HP
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.damage = damage
        self.splash_radius = splash_radius
        self.alive = True

        # Calculate velocity
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
        else:
            self.vx = 0
            self.vy = 0
            self.alive = False

    def update(self, dt: float):
        if not self.alive:
            return

        self.x += self.vx * dt
        self.y += self.vy * dt

        # Check if reached target
        dx = self.target_x - self.center[0]
        dy = self.target_y - self.center[1]
        if dx * dx + dy * dy < 100:  # Within 10 pixels
            self.alive = False

    def draw(self, surface: pygame.Surface, camera):
        if not self.alive:
            return
        sx, sy = camera.world_to_screen(self.center[0] - 3, self.center[1] - 3)
        pygame.draw.circle(surface, (255, 255, 100), (int(sx + 3), int(sy + 3)), 3)
