from constants import TerrainType, TERRAIN_WALKABLE, TERRAIN_BUILDABLE


class Tile:
    __slots__ = ('x', 'y', 'terrain', 'building', 'resource_node')

    def __init__(self, x: int, y: int, terrain: TerrainType = TerrainType.GRASS):
        self.x = x
        self.y = y
        self.terrain = terrain
        self.building = None
        self.resource_node = None

    @property
    def walkable(self) -> bool:
        if self.building is not None:
            return False
        return TERRAIN_WALKABLE.get(self.terrain, True)

    @property
    def buildable(self) -> bool:
        if self.building is not None:
            return False
        return TERRAIN_BUILDABLE.get(self.terrain, False)
