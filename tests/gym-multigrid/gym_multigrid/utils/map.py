import numpy as np
from numpy.typing import NDArray

from gym_multigrid.typing import Position


def distance_points(p1: Position, p2: Position, is_defeated: bool = False) -> float:
    """Calculate the squared distance of two points"""
    return (
        float(np.linalg.norm(np.array(p1) - np.array(p2)))
        if not is_defeated
        else float("inf")
    )


def distance_area_point(point: Position, area: list[Position]) -> float:
    """Calculate the squared distance of an area and a point"""
    distances = [np.linalg.norm(np.array(point) - np.array(node)) for node in area]
    return float(np.min(distances))


def load_text_map(map_path: str) -> NDArray:
    """
    Load a map from a text file

    Parameters
    ----------
    map_path : str
        Path to the map file (relative to the current directory to execute the script using this function).

    Returns
    -------
    field_map : numpy.typing.NDArray
        Field map of the environment.

    """
    field_map: NDArray = np.loadtxt(map_path).T

    return field_map


def position_in_positions(position: Position, positions: list[Position]) -> bool:
    """Check if a position is in a list of positions"""
    in_positions: bool = False

    for pos in positions:
        if position[0] == pos[0] and position[1] == pos[1]:
            in_positions = True
            break
        else:
            pass

    return in_positions


def closest_area_pos(pos: Position, area: list[Position]) -> Position:
    """Calculate the squared distance of an area and a point"""
    pos_np: NDArray[np.int_] = np.array(pos)

    distances = [np.linalg.norm(pos_np - np.array(node)) for node in area]
    return area[np.argmin(distances)]
