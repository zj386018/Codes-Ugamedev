import json
import os
from typing import Dict, Any, Optional


class SaveManager:
    SAVE_DIR = os.path.join(os.path.dirname(__file__), '..', 'saves')

    @classmethod
    def _ensure_dir(cls):
        os.makedirs(cls.SAVE_DIR, exist_ok=True)

    @classmethod
    def save_game(cls, game_state: Dict[str, Any], filename: str = "save1.json"):
        cls._ensure_dir()
        path = os.path.join(cls.SAVE_DIR, filename)
        with open(path, 'w') as f:
            json.dump(game_state, f, indent=2)

    @classmethod
    def load_game(cls, filename: str = "save1.json") -> Optional[Dict[str, Any]]:
        path = os.path.join(cls.SAVE_DIR, filename)
        if not os.path.exists(path):
            return None
        with open(path, 'r') as f:
            return json.load(f)

    @classmethod
    def get_save_files(cls):
        cls._ensure_dir()
        saves = []
        for f in os.listdir(cls.SAVE_DIR):
            if f.endswith('.json'):
                saves.append(f)
        return sorted(saves)

    @classmethod
    def build_save_state(cls, game) -> Dict[str, Any]:
        """Extract saveable state from a Game object."""
        state = {
            "camera": {"x": game.camera.x, "y": game.camera.y},
            "resources": dict(game.resource_manager.resources),
            "resource_caps": dict(game.resource_manager.resource_caps),
            "population": game.resource_manager.population,
            "max_population": game.resource_manager.max_population,
            "wave": game.wave_manager.current_wave,
            "wave_state": game.wave_manager.state.name,
            "prep_timer": game.wave_manager.prep_timer,
            "zombies_killed": game.wave_manager.total_zombies_killed,
            "buildings": [],
            "zombies": [],
        }

        # Buildings
        for b in game.build_system.buildings:
            bdata = {
                "type": b.name,
                "tile_x": b.tile_x,
                "tile_y": b.tile_y,
                "tile_width": b.tile_width,
                "tile_height": b.tile_height,
                "hp": b.hp,
                "max_hp": b.max_hp,
                "construction_progress": b.construction_progress,
                "is_complete": b.is_complete,
            }
            state["buildings"].append(bdata)

        # Zombies
        for z in game.zombies:
            zdata = {
                "type": z.zombie_type,
                "x": z.x, "y": z.y,
                "hp": z.hp, "max_hp": z.max_hp,
            }
            state["zombies"].append(zdata)

        return state

    @classmethod
    def delete_save(cls, filename: str = "save1.json"):
        path = os.path.join(cls.SAVE_DIR, filename)
        if os.path.exists(path):
            os.remove(path)
