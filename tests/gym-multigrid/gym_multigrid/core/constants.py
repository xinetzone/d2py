import numpy as np
from numpy.typing import NDArray

# Size in pixels of a tile in the full-scale human view
TILE_PIXELS = 32

# Map of color names to RGB values
COLORS = {
    "red": np.array([228, 3, 3]),
    "orange": np.array([255, 140, 0]),
    "yellow": np.array([255, 237, 0]),
    "green": np.array([0, 128, 38]),
    "blue": np.array([0, 77, 255]),
    "purple": np.array([117, 7, 135]),
    "brown": np.array([120, 79, 23]),
    "grey": np.array([100, 100, 100]),
    "light_red": np.array([234, 153, 153]),
    "light_blue": np.array([90, 170, 223]),
}

CTF_COLORS: dict[str, NDArray[np.uint]] = {
    "red": np.array([228, 3, 3]),
    "orange": np.array([255, 140, 0]),
    "yellow": np.array([255, 237, 0]),
    "green": np.array([0, 128, 38]),
    "blue": np.array([0, 77, 255]),
    "purple": np.array([117, 7, 135]),
    "brown": np.array([120, 79, 23]),
    "grey": np.array([100, 100, 100]),
    "light_red": np.array([255, 228, 225]),
    "light_blue": np.array([240, 248, 255]),
    "white": np.array([255, 250, 250]),
    "red_grey": np.array([170, 152, 169]),
    "blue_grey": np.array([140, 146, 172]),
}

MAZE_COLORS: dict[str, NDArray[np.uint]] = {
    "red": np.array([228, 3, 3]),
    "orange": np.array([255, 140, 0]),
    "yellow": np.array([255, 237, 0]),
    "green": np.array([0, 128, 38]),
    "blue": np.array([0, 77, 255]),
    "purple": np.array([117, 7, 135]),
    "brown": np.array([120, 79, 23]),
    "grey": np.array([100, 100, 100]),
    "light_red": np.array([255, 228, 225]),
    "light_blue": np.array([240, 248, 255]),
    "white": np.array([255, 250, 250]),
}

COLOR_NAMES = sorted(list(COLORS.keys()))

# Used to map colors to integers
COLOR_TO_IDX: "dict[str, int]" = {key: i for i, key in enumerate(COLORS.keys())}
IDX_TO_COLOR = dict(zip(COLOR_TO_IDX.values(), COLOR_TO_IDX.keys()))

# Map of state names to integers
STATE_TO_IDX = {
    "open": 0,
    "closed": 1,
    "locked": 2,
}

# Map of agent direction indices to vectors
DIR_TO_VEC = [
    # Pointing right (positive X)
    np.array((1, 0)),
    # Down (positive Y)
    np.array((0, 1)),
    # Pointing left (negative X)
    np.array((-1, 0)),
    # Up (negative Y)
    np.array((0, -1)),
]

# Map of object types to short string
OBJECT_TO_STR = {
    "wall": "x",
    "floor": "F",
    "door": "D",
    "key": "K",
    "ball": "o",
    "box": "B",
    "goal": "G",
    "lava": "V",
    "agent": "a",
}

# Short string for opened door
OPENED_DOOR_IDS = "_"

# Map agent's direction to short string
AGENT_DIR_TO_STR = {0: ">", 1: "V", 2: "<", 3: "^"}
