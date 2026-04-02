import json
import os
import random
from enum import Enum, auto
from typing import Dict, List, Tuple, Optional
from constants import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE


class WaveState(Enum):
    PREP = auto()
    ACTIVE = auto()
    COMPLETE = auto()


class WaveManager:
    def __init__(self):
        self.current_wave = 0
        self.state = WaveState.PREP
        self.prep_timer = 120.0
        self.spawn_queue: List[str] = []
        self.spawn_timer = 0.0
        self.zombies_alive = 0
        self.total_zombies_killed = 0

        # Load wave data
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'waves.json')
        with open(data_path, 'r') as f:
            self.data = json.load(f)

        self.wave_definitions = self.data["waves"]
        self.scaling = self.data["scaling"]
        self.spawn_interval = self.data["spawn_interval"]
        self.max_waves = self.data["max_waves"]

    def start_next_wave(self):
        self.current_wave += 1
        self.state = WaveState.ACTIVE

        # Build spawn queue
        wave_def = self._get_wave_definition(self.current_wave)
        self.spawn_queue = []
        for zombie_type, count in wave_def["zombies"].items():
            for _ in range(count):
                self.spawn_queue.append(zombie_type)
        random.shuffle(self.spawn_queue)

        self.spawn_timer = 0.0
        self.zombies_alive = len(self.spawn_queue)

    def _get_wave_definition(self, wave_number: int) -> Dict:
        """Get wave definition, interpolating between defined waves."""
        # Find surrounding defined waves
        lower = None
        upper = None
        for wd in self.wave_definitions:
            if wd["number"] <= wave_number:
                lower = wd
            if wd["number"] >= wave_number and upper is None:
                upper = wd

        if lower is None:
            lower = self.wave_definitions[0]
        if upper is None:
            # Beyond defined waves: scale the last defined wave
            last = self.wave_definitions[-1]
            scale = 1 + (wave_number - last["number"]) * 0.3
            zombies = {}
            for zt, count in last["zombies"].items():
                zombies[zt] = int(count * scale)
            return {"number": wave_number, "prep_time": 40, "zombies": zombies}

        if lower["number"] == wave_number:
            return lower

        # Interpolate
        t = (wave_number - lower["number"]) / max(1, upper["number"] - lower["number"])
        zombies = {}
        all_types = set(list(lower["zombies"].keys()) + list(upper["zombies"].keys()))
        for zt in all_types:
            low_count = lower["zombies"].get(zt, 0)
            high_count = upper["zombies"].get(zt, 0)
            zombies[zt] = int(low_count + (high_count - low_count) * t)

        prep_time = lower["prep_time"] + (upper["prep_time"] - lower["prep_time"]) * t
        return {"number": wave_number, "prep_time": int(prep_time), "zombies": zombies}

    def get_difficulty_multiplier(self) -> Tuple[float, float]:
        """Returns (hp_multiplier, damage_multiplier) for current wave."""
        hp_mult = 1.0 + self.scaling["hp_multiplier_per_wave"] * (self.current_wave - 1)
        dmg_mult = 1.0 + self.scaling["damage_multiplier_per_wave"] * (self.current_wave - 1)
        return hp_mult, dmg_mult

    def get_spawn_point(self) -> Tuple[float, float]:
        """Get a random spawn point on the map edge."""
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top":
            return random.uniform(0, MAP_WIDTH * TILE_SIZE), 0
        elif side == "bottom":
            return random.uniform(0, MAP_WIDTH * TILE_SIZE), (MAP_HEIGHT - 1) * TILE_SIZE
        elif side == "left":
            return 0, random.uniform(0, MAP_HEIGHT * TILE_SIZE)
        else:
            return (MAP_WIDTH - 1) * TILE_SIZE, random.uniform(0, MAP_HEIGHT * TILE_SIZE)

    def update(self, dt: float) -> List[Tuple[str, float, float]]:
        """Update wave state. Returns list of (zombie_type, x, y) for zombies to spawn."""
        spawns = []

        if self.state == WaveState.PREP:
            self.prep_timer -= dt
            if self.prep_timer <= 0:
                self.start_next_wave()

        elif self.state == WaveState.ACTIVE:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0 and self.spawn_queue:
                zombie_type = self.spawn_queue.pop(0)
                x, y = self.get_spawn_point()
                spawns.append((zombie_type, x, y))
                self.spawn_timer = self.spawn_interval

        return spawns

    def on_zombie_killed(self):
        self.zombies_alive -= 1
        self.total_zombies_killed += 1

    def check_wave_complete(self, live_zombie_count: int) -> bool:
        if self.state == WaveState.ACTIVE and len(self.spawn_queue) == 0 and live_zombie_count == 0:
            self.state = WaveState.COMPLETE
            # Set up next prep
            next_wave_def = self._get_wave_definition(self.current_wave + 1)
            self.prep_timer = next_wave_def["prep_time"]
            self.state = WaveState.PREP
            return True
        return False

    def is_victory(self) -> bool:
        return self.current_wave >= self.max_waves and self.state == WaveState.PREP

    def get_prep_time_str(self) -> str:
        if self.state == WaveState.PREP:
            return f"第 {self.current_wave + 1} 波倒计时: {int(self.prep_timer)}秒"
        elif self.state == WaveState.ACTIVE:
            return f"第 {self.current_wave} 波 - 剩余僵尸: {len(self.spawn_queue)}"
        return ""
