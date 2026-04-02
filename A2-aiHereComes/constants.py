from enum import Enum, auto

# Font
import pygame
def get_font(size):
    """Get a font that supports Chinese characters."""
    for name in ["simhei", "microsoftyahei", "simsun", "dengxian", "fangsong"]:
        f = pygame.font.SysFont(name, size)
        # Test if font can render Chinese
        if f.render("测试", True, (0, 0, 0)).get_width() > 10:
            return f
    return pygame.font.SysFont(None, size)

# Screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Tile / Map
TILE_SIZE = 32
MAP_WIDTH = 200
MAP_HEIGHT = 200

# Camera
CAMERA_SPEED = 400  # pixels per second
CAMERA_EDGE_SCROLL_ZONE = 20  # pixels from screen edge

# Minimap
MINIMAP_SIZE = 180
MINIMAP_MARGIN = 10

# Colors
class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    DARK_GRAY = (64, 64, 64)

    # Terrain
    GRASS = (76, 153, 0)
    GRASS_DARK = (60, 130, 0)
    DIRT = (160, 130, 80)
    WATER = (40, 100, 180)
    WATER_DEEP = (30, 70, 140)
    FOREST = (40, 100, 20)
    STONE = (140, 140, 140)
    STONE_DARK = (110, 110, 110)

    # Entities
    BUILDING_VALID = (0, 255, 0, 100)
    BUILDING_INVALID = (255, 0, 0, 100)
    HP_GREEN = (0, 200, 0)
    HP_RED = (200, 0, 0)
    HP_YELLOW = (200, 200, 0)

    # UI
    UI_BG = (30, 30, 40)
    UI_BORDER = (80, 80, 100)
    UI_TEXT = (220, 220, 220)
    UI_HIGHLIGHT = (100, 150, 255)
    UI_BUTTON = (60, 60, 80)
    UI_BUTTON_HOVER = (80, 80, 110)


class TerrainType(Enum):
    GRASS = auto()
    GRASS_DARK = auto()
    DIRT = auto()
    WATER = auto()
    FOREST = auto()
    STONE = auto()


TERRAIN_COLORS = {
    TerrainType.GRASS: Color.GRASS,
    TerrainType.GRASS_DARK: Color.GRASS_DARK,
    TerrainType.DIRT: Color.DIRT,
    TerrainType.WATER: Color.WATER,
    TerrainType.FOREST: Color.FOREST,
    TerrainType.STONE: Color.STONE,
}

TERRAIN_WALKABLE = {
    TerrainType.GRASS: True,
    TerrainType.GRASS_DARK: True,
    TerrainType.DIRT: True,
    TerrainType.WATER: False,
    TerrainType.FOREST: True,
    TerrainType.STONE: False,
}

TERRAIN_BUILDABLE = {
    TerrainType.GRASS: True,
    TerrainType.GRASS_DARK: True,
    TerrainType.DIRT: True,
    TerrainType.WATER: False,
    TerrainType.FOREST: False,
    TerrainType.STONE: False,
}

# Resources
RESOURCE_TYPES = ["wood", "stone", "gold", "food"]

# Game States
class GameState(Enum):
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
