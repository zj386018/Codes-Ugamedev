from typing import Dict, List, Tuple, Optional
from collections import deque
from constants import MAP_WIDTH, MAP_HEIGHT


class Pathfinder:
    """Flow field pathfinding. Computes BFS from a goal tile.
    Each tile stores the direction toward the goal.
    Zombies read the direction from their current tile to move."""

    def __init__(self, game_map):
        self.game_map = game_map
        self.flow_field: Dict[Tuple[int, int], Tuple[float, float]] = {}
        self.flow_field_dirty = True
        self.goal: Optional[Tuple[int, int]] = None

    def set_goal(self, tile_x: int, tile_y: int):
        self.goal = (tile_x, tile_y)
        self.flow_field_dirty = True

    def invalidate(self):
        self.flow_field_dirty = True

    def get_direction(self, tile_x: int, tile_y: int) -> Optional[Tuple[float, float]]:
        if self.flow_field_dirty:
            self._compute_flow_field()
        return self.flow_field.get((tile_x, tile_y))

    def _compute_flow_field(self):
        if self.goal is None:
            return

        self.flow_field.clear()

        # BFS from goal outward
        visited = set()
        queue = deque()

        gx, gy = self.goal
        if not (0 <= gx < self.game_map.width and 0 <= gy < self.game_map.height):
            return

        visited.add((gx, gy))
        self.flow_field[(gx, gy)] = (0.0, 0.0)  # At goal, no movement needed
        queue.append((gx, gy))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                      (-1, -1), (-1, 1), (1, -1), (1, 1)]  # 8-directional

        while queue:
            cx, cy = queue.popleft()

            for dx, dy in directions:
                nx, ny = cx + dx, cy + dy

                if (nx, ny) in visited:
                    continue

                tile = self.game_map.get_tile(nx, ny)
                if tile is None:
                    continue
                if not tile.walkable:
                    continue

                # For diagonal movement, check that both adjacent tiles are walkable
                if dx != 0 and dy != 0:
                    t1 = self.game_map.get_tile(cx + dx, cy)
                    t2 = self.game_map.get_tile(cx, cy + dy)
                    if t1 is None or not t1.walkable or t2 is None or not t2.walkable:
                        continue

                visited.add((nx, ny))
                # Direction from this tile toward the current tile (closer to goal)
                length = (dx * dx + dy * dy) ** 0.5
                self.flow_field[(nx, ny)] = (-dx / length, -dy / length)
                queue.append((nx, ny))

        self.flow_field_dirty = False
