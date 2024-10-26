from typing import Type
import numpy as np

from gym_multigrid.core.world import WorldT
from gym_multigrid.utils.rendering import downsample, highlight_img, fill_coords, point_in_rect
from gym_multigrid.core.object import WorldObj, Wall, WorldObjT
from gym_multigrid.core.constants import TILE_PIXELS


class Grid:
    """
    Represent a grid and operations on it
    """

    # Static cache of pre-renderer tiles
    tile_cache = {}

    def __init__(self, width: int, height: int, world: WorldT):
        assert width >= 3
        assert height >= 3

        self.width = width
        self.height = height
        self.world = world

        self.grid: list[WorldObjT | None] = [None] * width * height

    def __contains__(self, key: type[WorldObjT] | tuple) -> bool:
        if isinstance(key, WorldObj):
            for e in self.grid:
                if e is key:
                    return True
        elif isinstance(key, tuple):
            for e in self.grid:
                if e is None:
                    continue
                if (e.color, e.type) == key:
                    return True
                if key[0] is None and key[1] == e.type:
                    return True
        return False

    def __eq__(self, other: "Grid") -> bool:
        grid1 = self.encode()
        grid2 = other.encode()
        return np.array_equal(grid2, grid1)

    def __ne__(self, other: "Grid") -> bool:
        return not self == other

    def copy(self) -> "Grid":
        from copy import deepcopy

        return deepcopy(self)

    def set(self, i: int, j: int, v: WorldObjT | None) -> None:
        assert i >= 0 and i < self.width
        assert j >= 0 and j < self.height
        self.grid[j * self.width + i] = v

    def get(self, i: int, j: int) -> WorldObjT | None:
        assert i >= 0 and i < self.width
        assert j >= 0 and j < self.height
        return self.grid[j * self.width + i]

    def horz_wall(
        self,
        x: int,
        y: int,
        length: int | None = None,
        obj_type: Type[WorldObjT] = Wall,
    ) -> None:
        if length is None:
            length = self.width - x
        assert length is not None
        for i in range(0, length):
            self.set(x + i, y, obj_type(self.world))

    def vert_wall(
        self,
        x: int,
        y: int,
        length: int | None = None,
        obj_type: Type[WorldObjT] = Wall,
    ):
        if length is None:
            length = self.height - y
        for j in range(0, length):
            self.set(x, y + j, obj_type(self.world))

    def wall_rect(self, x: int, y: int, w: int, h: int) -> None:
        self.horz_wall(x, y, w)
        self.horz_wall(x, y + h - 1, w)
        self.vert_wall(x, y, h)
        self.vert_wall(x + w - 1, y, h)

    def rotate_left(self) -> "Grid":
        """
        Rotate the grid to the left (counter-clockwise)
        """

        grid = Grid(self.height, self.width, self.world)

        for i in range(self.width):
            for j in range(self.height):
                v = self.get(i, j)
                grid.set(j, grid.height - 1 - i, v)

        return grid

    def slice(self, topX, topY, width, height):
        """
        Get a subset of the grid
        """

        grid = Grid(width, height, self.world)

        for j in range(0, height):
            for i in range(0, width):
                x = topX + i
                y = topY + j

                if x >= 0 and x < self.width and y >= 0 and y < self.height:
                    v = self.get(x, y)
                else:
                    v = Wall(self.world)

                grid.set(i, j, v)

        return grid

    @classmethod
    def render_tile(
        cls,
        world: WorldT,
        obj: WorldObjT | None,
        highlights: list[bool] = [],
        tile_size: int = TILE_PIXELS,
        subdivs: int = 3,
        cache: bool = True,
    ):
        """
        Render a tile and cache the result
        """

        key = (*highlights, tile_size)
        key = obj.encode() + key if obj else key

        if key in cls.tile_cache:
            return cls.tile_cache[key]

        img = np.zeros(
            shape=(tile_size * subdivs, tile_size * subdivs, 3), dtype=np.uint8
        )

        # Draw the grid lines (top and left edges)

        if obj != None:
            obj.render(img)

        fill_coords(img, point_in_rect(0, 0.031, 0, 1), (100, 100, 100))
        fill_coords(img, point_in_rect(0, 1, 0, 0.031), (100, 100, 100))

        # Highlight the cell  if needed
        if len(highlights) > 0:
            for h in highlights:
                highlight_img(
                    img,
                    color=world.COLORS[world.IDX_TO_COLOR[h % len(world.IDX_TO_COLOR)]],
                )

        # Downsample the image to perform supersampling/anti-aliasing
        img = downsample(img, subdivs)

        # Cache the rendered tile
        if cache:
            cls.tile_cache[key] = img
        else:
            pass

        return img

    def render(
        self, tile_size, highlight_masks=None, uncached_object_types: list[str] = []
    ):
        """
        Render this grid at a given scale
        :param r: target renderer object
        :param tile_size: tile size in pixels
        """

        # Compute the total grid size
        width_px = self.width * tile_size
        height_px = self.height * tile_size

        img = np.zeros(shape=(height_px, width_px, 3), dtype=np.uint8)

        # Render the grid
        for j in range(0, self.height):
            for i in range(0, self.width):
                cell = self.get(i, j)

                cache: bool = True
                if cell is not None and cell.type in uncached_object_types:
                    cache = False
                # agent_here = np.array_equal(agent_pos, (i, j))
                tile_img = Grid.render_tile(
                    self.world,
                    cell,
                    highlights=[] if highlight_masks is None else highlight_masks[i, j],
                    tile_size=tile_size,
                    cache=cache,
                )

                ymin = j * tile_size
                ymax = (j + 1) * tile_size
                xmin = i * tile_size
                xmax = (i + 1) * tile_size
                img[ymin:ymax, xmin:xmax, :] = tile_img

        return img

    def encode(self, vis_mask=None):
        """
        Produce a compact numpy encoding of the grid
        """

        if vis_mask is None:
            vis_mask = np.ones((self.width, self.height), dtype=bool)

        array = np.zeros(
            (self.width, self.height, self.world.encode_dim), dtype="uint8"
        )

        for i in range(self.width):
            for j in range(self.height):
                if vis_mask[i, j]:
                    v = self.get(i, j)

                    if v is None:
                        array[i, j, 0] = self.world.OBJECT_TO_IDX["empty"]
                        array[i, j, 1] = 0
                        array[i, j, 2] = 0
                        if self.world.encode_dim > 3:
                            array[i, j, 3] = 0
                            array[i, j, 4] = 0
                            array[i, j, 5] = 0

                    else:
                        array[i, j, :] = v.encode(self.world)

        return array

    def encode_for_agents(self, agent_pos, vis_mask=None):
        """
        Produce a compact numpy encoding of the grid
        """
        if vis_mask is None:
            vis_mask = np.ones((self.width, self.height), dtype=bool)

        array = np.zeros(
            (self.width, self.height, self.world.encode_dim), dtype="uint8"
        )

        for i in range(self.width):
            for j in range(self.height):
                if vis_mask[i, j]:
                    v = self.get(i, j)

                    if v is None:
                        array[i, j, 0] = self.world.OBJECT_TO_IDX["empty"]
                        array[i, j, 1] = 0
                        array[i, j, 2] = 0
                        if self.world.encode_dim > 3:
                            array[i, j, 3] = 0
                            array[i, j, 4] = 0
                            array[i, j, 5] = 0

                    else:
                        array[i, j, :] = v.encode(
                            current_agent=np.array_equal(agent_pos, (i, j))
                        )

        return array

    def process_vis(grid, agent_pos):
        mask = np.zeros(shape=(grid.width, grid.height), dtype=bool)

        mask[agent_pos[0], agent_pos[1]] = True

        for j in reversed(range(0, grid.height)):
            for i in range(0, grid.width - 1):
                if not mask[i, j]:
                    continue

                cell = grid.get(i, j)
                if cell and not cell.see_behind():
                    continue

                mask[i + 1, j] = True
                if j > 0:
                    mask[i + 1, j - 1] = True
                    mask[i, j - 1] = True

            for i in reversed(range(1, grid.width)):
                if not mask[i, j]:
                    continue

                cell = grid.get(i, j)
                if cell and not cell.see_behind():
                    continue

                mask[i - 1, j] = True
                if j > 0:
                    mask[i - 1, j - 1] = True
                    mask[i, j - 1] = True

        for j in range(0, grid.height):
            for i in range(0, grid.width):
                if not mask[i, j]:
                    grid.set(i, j, None)

        return mask
