from enum import Enum


class LayerType(Enum):
    TILES = 'tiles'
    TRAFFIC_SIGNS = 'traffic_signs'
    GROUND_APRILTAG = 'ground_apriltag'
    WATCHTOWERS = 'watchtowers'
    REGIONS = 'regions'
    ITEMS = 'items'

    def __str__(self):
        return self.value
