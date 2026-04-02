import json
import os
from typing import Optional, Dict, Tuple
import pygame
from constants import TILE_SIZE, Color
from entities.building import Building
from entities.buildings.wall import Wall
from entities.buildings.tower import Tower
from entities.buildings.town_center import TownCenter
from entities.buildings.housing import House
from entities.buildings.resource_building import Farm, LumberMill, Quarry, GoldMine
from entities.buildings.storage import Storage
from systems.resource_manager import ResourceManager


# Mapping from building type key to class
BUILDING_CLASSES = {
    "wall": Wall,
    "wood_tower": lambda tx, ty: Tower(tx, ty, "wood"),
    "stone_tower": lambda tx, ty: Tower(tx, ty, "stone"),
    "town_center": TownCenter,
    "farm": Farm,
    "house": House,
    "storage": Storage,
    "lumber_mill": LumberMill,
    "quarry": Quarry,
    "gold_mine": GoldMine,
}


class BuildSystem:
    def __init__(self, game_map, resource_manager: ResourceManager):
        self.game_map = game_map
        self.resource_manager = resource_manager
        self.buildings = []
        self.selected_building_type: Optional[str] = None
        self.ghost_pos: Optional[Tuple[int, int]] = None

        # Load building data
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'buildings.json')
        with open(data_path, 'r') as f:
            self.building_data: Dict = json.load(f)

    def select_building(self, building_type: str):
        self.selected_building_type = building_type

    def deselect(self):
        self.selected_building_type = None

    def get_building_size(self, building_type: str) -> Tuple[int, int]:
        data = self.building_data.get(building_type, {})
        size = data.get("tile_size", [1, 1])
        return size[0], size[1]

    def can_place(self, tile_x: int, tile_y: int, building_type: str) -> bool:
        tw, th = self.get_building_size(building_type)

        # Check bounds
        if tile_x < 0 or tile_y < 0:
            return False
        if tile_x + tw > self.game_map.width or tile_y + th > self.game_map.height:
            return False

        # Check each tile
        for dy in range(th):
            for dx in range(tw):
                tile = self.game_map.get_tile(tile_x + dx, tile_y + dy)
                if tile is None or not tile.buildable:
                    return False
                if tile.building is not None:
                    return False

        # Check cost
        cost = self.building_data.get(building_type, {}).get("cost", {})
        if not self.resource_manager.can_afford(cost):
            return False

        return True

    def place_building(self, tile_x: int, tile_y: int, building_type: str) -> Optional[Building]:
        if not self.can_place(tile_x, tile_y, building_type):
            return None

        # Deduct cost
        cost = self.building_data.get(building_type, {}).get("cost", {})
        self.resource_manager.spend(cost)

        # Create building
        builder = BUILDING_CLASSES.get(building_type)
        if builder is None:
            return None

        building = builder(tile_x, tile_y)
        building.place_on_map(self.game_map)
        self.buildings.append(building)

        # Apply bonuses for pre-built buildings
        if building.is_complete:
            self._apply_bonuses(building)

        return building

    def _apply_bonuses(self, building: Building):
        if isinstance(building, (House,)):
            self.resource_manager.add_population_cap(building.population_bonus)
        elif isinstance(building, Storage):
            for res, bonus in building.storage_bonus.items():
                self.resource_manager.increase_cap(res, bonus)
        elif isinstance(building, TownCenter):
            # Town center gives population + storage
            self.resource_manager.add_population_cap(10)
            for res, bonus in {"wood": 200, "stone": 200, "gold": 100, "food": 150}.items():
                self.resource_manager.increase_cap(res, bonus)

    def update_ghost(self, mouse_tile_x: int, mouse_tile_y: int):
        if self.selected_building_type:
            self.ghost_pos = (mouse_tile_x, mouse_tile_y)
        else:
            self.ghost_pos = None

    def draw_ghost(self, surface: pygame.Surface, camera):
        if not self.ghost_pos or not self.selected_building_type:
            return

        tx, ty = self.ghost_pos
        tw, th = self.get_building_size(self.selected_building_type)
        can = self.can_place(tx, ty, self.selected_building_type)

        # Create semi-transparent surface
        ghost_surf = pygame.Surface((tw * TILE_SIZE, th * TILE_SIZE), pygame.SRCALPHA)
        color = (*Color.BUILDING_VALID[:3], 100) if can else (*Color.BUILDING_INVALID[:3], 100)
        ghost_surf.fill(color)

        sx, sy = camera.world_to_screen(tx * TILE_SIZE, ty * TILE_SIZE)
        surface.blit(ghost_surf, (int(sx), int(sy)))

        # Border
        border_color = (0, 200, 0) if can else (200, 0, 0)
        pygame.draw.rect(surface, border_color,
                         (int(sx), int(sy), tw * TILE_SIZE, th * TILE_SIZE), 2)

    def update(self, dt: float):
        for building in self.buildings:
            if not building.alive:
                continue
            was_complete = building.is_complete
            result = building.update(dt)

            # Check if just completed
            if not was_complete and building.is_complete:
                self._apply_bonuses(building)

            # Handle resource production
            if result and isinstance(result, dict):
                for res_type, amount in result.items():
                    self.resource_manager.add_resource(res_type, amount)

    def remove_building(self, building: Building):
        building.remove_from_map(self.game_map)
        if building in self.buildings:
            self.buildings.remove(building)

    def repair_all(self) -> Tuple[int, int]:
        """Repair all damaged buildings. Returns (count_repaired, total_hp_restored)."""
        repaired = 0
        total_restored = 0
        for building in self.buildings:
            if building.alive and building.hp < building.max_hp:
                restored = building.max_hp - building.hp
                building.hp = building.max_hp
                repaired += 1
                total_restored += restored
        return repaired, total_restored
