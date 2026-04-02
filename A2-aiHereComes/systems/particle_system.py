import math
import random
from typing import List, Tuple
import pygame


class Particle:
    __slots__ = ('x', 'y', 'vx', 'vy', 'lifetime', 'max_lifetime', 'color', 'size')

    def __init__(self, x: float, y: float, vx: float, vy: float,
                 lifetime: float, color: Tuple[int, int, int], size: float = 2.0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.color = color
        self.size = size


class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []

    def emit(self, x: float, y: float, count: int = 5,
             color: Tuple[int, int, int] = (200, 0, 0),
             speed_range: Tuple[float, float] = (20, 60),
             lifetime_range: Tuple[float, float] = (0.2, 0.5),
             size: float = 2.0):
        for _ in range(count):
            angle = random.uniform(0, 6.283)
            speed = random.uniform(*speed_range)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifetime = random.uniform(*lifetime_range)
            self.particles.append(Particle(x, y, vx, vy, lifetime, color, size))

    def update(self, dt: float):
        alive = []
        for p in self.particles:
            p.lifetime -= dt
            if p.lifetime > 0:
                p.x += p.vx * dt
                p.y += p.vy * dt
                alive.append(p)
        self.particles = alive

    def draw(self, surface: pygame.Surface, camera):
        for p in self.particles:
            alpha = p.lifetime / p.max_lifetime
            sx, sy = camera.world_to_screen(p.x, p.y)
            size = max(1, int(p.size * alpha))
            color = tuple(int(c * alpha) for c in p.color)
            pygame.draw.circle(surface, color, (int(sx), int(sy)), size)
