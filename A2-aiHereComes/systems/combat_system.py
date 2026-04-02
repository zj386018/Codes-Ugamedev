import math
from typing import List, Tuple
from entities.buildings.tower import Tower
from entities.zombie import Zombie
from entities.projectile import Projectile
from entities.building import Building
from constants import TILE_SIZE


class CombatSystem:
    def __init__(self):
        self.projectiles: List[Projectile] = []

    def update(self, dt: float, buildings: List[Building], zombies: List[Zombie]):
        # Tower targeting and shooting
        for building in buildings:
            if not building.alive or not building.is_complete:
                continue
            if not isinstance(building, Tower):
                continue

            building.attack_timer -= dt
            if building.attack_timer <= 0:
                target = self._find_target(building, zombies)
                if target:
                    self._fire_projectile(building, target)
                    building.attack_timer = 1.0 / building.attack_speed

        # Update projectiles
        for proj in self.projectiles:
            proj.update(dt)
            if not proj.alive:
                continue

            # Check collision with zombies
            for zombie in zombies:
                if not zombie.alive:
                    continue
                dx = proj.center[0] - zombie.center[0]
                dy = proj.center[1] - zombie.center[1]
                if dx * dx + dy * dy < 200:  # Collision radius ~14px
                    zombie.take_damage(proj.damage)
                    proj.alive = False
                    break

        # Clean up dead projectiles
        self.projectiles = [p for p in self.projectiles if p.alive]

    def _find_target(self, tower: Tower, zombies: List[Zombie]) -> Zombie:
        """Find the nearest zombie within tower's attack range."""
        best = None
        best_dist = float('inf')
        range_px = tower.attack_range * TILE_SIZE

        tx, ty = tower.center
        for zombie in zombies:
            if not zombie.alive:
                continue
            zx, zy = zombie.center
            dist = math.sqrt((tx - zx) ** 2 + (ty - zy) ** 2)
            if dist < range_px and dist < best_dist:
                best = zombie
                best_dist = dist

        return best

    def _fire_projectile(self, tower: Tower, target: Zombie):
        sx, sy = tower.center
        tx, ty = target.center
        proj = Projectile(sx, sy, tx, ty, speed=300, damage=tower.attack_damage)
        self.projectiles.append(proj)

    def draw(self, surface, camera):
        for proj in self.projectiles:
            proj.draw(surface, camera)
