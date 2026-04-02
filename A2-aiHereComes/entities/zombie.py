import json
import os
import math
import random
from typing import Tuple, Optional
import pygame
from entities.entity import Entity
from constants import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT


class Zombie(Entity):
    def __init__(self, x: float, y: float, zombie_type: str = "basic"):
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'zombies.json')
        with open(data_path, 'r') as f:
            all_data = json.load(f)

        data = all_data.get(zombie_type, all_data["basic"])
        size = 24 if zombie_type != "boss" else 40
        super().__init__(x, y, size, size, data["hp"])

        self.zombie_type = zombie_type
        self.speed = data["speed"]
        self.damage = data["damage"]
        self.attack_rate = data["attack_rate"]
        self.color = tuple(data["color"])
        self.attack_timer = 0.0
        self.target_building = None
        # Town center goal position (set by game)
        self.goal_x = 0.0
        self.goal_y = 0.0

    def update(self, dt: float, pathfinder=None, game_map=None, buildings=None):
        if not self.alive:
            return

        self.attack_timer -= dt

        # Check for nearby buildings to attack
        if buildings:
            best_dist = TILE_SIZE * 1.5
            best_building = None
            for building in buildings:
                if not building.alive:
                    continue
                dist = self._distance_to(building.center)
                if dist < best_dist:
                    best_dist = dist
                    best_building = building

            if best_building and best_dist < TILE_SIZE * 1.2:
                self._attack_building(best_building, dt)
                return

        # Move toward goal using flow field or direct movement
        moved = False

        if pathfinder:
            tx = int(self.center[0] // TILE_SIZE)
            ty = int(self.center[1] // TILE_SIZE)
            direction = pathfinder.get_direction(tx, ty)
            if direction and (direction[0] != 0 or direction[1] != 0):
                dx, dy = direction
                self.x += dx * self.speed * dt
                self.y += dy * self.speed * dt
                moved = True

        # Fallback: move directly toward town center goal
        if not moved:
            gx, gy = self.goal_x, self.goal_y
            cx, cy = self.center
            dx = gx - cx
            dy = gy - cy
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 5:
                self.x += (dx / dist) * self.speed * dt
                self.y += (dy / dist) * self.speed * dt

        # Small random jitter to avoid stacking
        self.x += random.uniform(-3, 3) * dt
        self.y += random.uniform(-3, 3) * dt

    def _distance_to(self, pos: Tuple[float, float]) -> float:
        cx, cy = self.center
        return math.sqrt((cx - pos[0]) ** 2 + (cy - pos[1]) ** 2)

    def _attack_building(self, building, dt: float):
        if self.attack_timer <= 0:
            building.take_damage(self.damage)
            self.attack_timer = 1.0 / self.attack_rate

    def draw(self, surface: pygame.Surface, camera):
        if not self.alive:
            return

        sx, sy = camera.world_to_screen(self.x, self.y)
        ix, iy = int(sx), int(sy)

        # Shadow
        pygame.draw.ellipse(surface, (0, 0, 0, 80),
                            (ix + 2, iy + self.height - 4, self.width - 4, 6))

        # Body
        pygame.draw.rect(surface, self.color,
                         (ix, iy, self.width, self.height))
        # Darker outline
        pygame.draw.rect(surface, tuple(max(0, c - 40) for c in self.color),
                         (ix, iy, self.width, self.height), 1)

        # Eyes
        eye_size = 3 if self.zombie_type != "boss" else 6
        eye_y = iy + self.height // 4
        pygame.draw.rect(surface, (255, 50, 50),
                         (ix + self.width // 4, eye_y, eye_size, eye_size))
        pygame.draw.rect(surface, (255, 50, 50),
                         (ix + self.width // 2 + 2, eye_y, eye_size, eye_size))

        # Arms (simple lines reaching forward)
        arm_color = tuple(min(255, c + 20) for c in self.color)
        pygame.draw.line(surface, arm_color,
                         (ix + 2, iy + self.height // 2),
                         (ix - 4, iy + self.height // 2 + 4), 2)
        pygame.draw.line(surface, arm_color,
                         (ix + self.width - 2, iy + self.height // 2),
                         (ix + self.width + 4, iy + self.height // 2 + 4), 2)

        # HP bar
        if self.hp < self.max_hp:
            bar_w = self.width
            bar_h = 3
            bar_y = iy - 5
            pygame.draw.rect(surface, (60, 0, 0), (ix, bar_y, bar_w, bar_h))
            hp_ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, (200, 0, 0),
                             (ix, bar_y, int(bar_w * hp_ratio), bar_h))
