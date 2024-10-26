from heapq import heapify, heappop, heappush
from typing import NamedTuple, Union

from numpy.typing import NDArray

from gym_multigrid.typing import Position


class AStarNode(NamedTuple):
    f: int
    g: int
    h: int
    parent: Union["AStarNode", None]
    loc: Position


def a_star(start: Position, end: Position, map: NDArray) -> list[Position]:
    """
    Compute the path from start to end using A* algorithm.

    Parameters
    ----------
    start : Position
        Start position
    end : Position
        End position
    map : NDArray
        Map of the environment

    Returns
    -------
    path: list[Position]
        List of positions from start to end
    """

    rows, cols = map.shape
    map_list: list[list[float]] = map.tolist()
    # Add the start and end nodes
    start_node = AStarNode(
        manhattan_distance(start, end), 0, manhattan_distance(start, end), None, start
    )
    # Initialize and heapify the lists
    open_nodes: list[AStarNode] = [start_node]
    closed_nodes: list[AStarNode] = []
    heapify(open_nodes)
    path: list[Position] = []  # return of the func

    while open_nodes:
        # Get the current node popped from the open list
        current_node = heappop(open_nodes)

        # Push the current node to the closed list
        closed_nodes.append(current_node)

        # When the goal is found
        if current_node.loc == end:
            current: AStarNode | None = current_node
            while current is not None:
                path.append(current.loc)
                current = current.parent

            path.reverse()
            break

        else:
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                # Get node location
                current_loc: Position = current_node.loc
                new_loc = (current_loc[0] + direction[0], current_loc[1] + direction[1])

                # Make sure within a range
                if (
                    (new_loc[1] >= 0 and new_loc[1] < cols)
                    and (new_loc[0] >= 0 and new_loc[0] < rows)
                    and (map_list[new_loc[0]][new_loc[1]] != 8)
                ):
                    # Create the f, g, and h values
                    g = current_node.g + 1
                    h = manhattan_distance(new_loc, end)
                    f = g + h

                    # Check if the new node is in the open or closed list
                    open_indices = [
                        i
                        for i, open_node in enumerate(open_nodes)
                        if open_node.loc == new_loc
                    ]
                    closed_indices = [
                        i
                        for i, closed_node in enumerate(closed_nodes)
                        if closed_node.loc == new_loc
                    ]

                    # Compare f values if the new node is already existing in either list
                    if closed_indices:
                        closed_index = closed_indices[0]
                        if f < closed_nodes[closed_index].f:
                            closed_nodes.pop(closed_index)
                            heappush(
                                open_nodes, AStarNode(f, g, h, current_node, new_loc)
                            )
                        else:
                            continue

                    elif open_indices:
                        open_index = open_indices[0]
                        if f < open_nodes[open_index].f:
                            open_nodes.pop(open_index)
                            open_nodes.append(AStarNode(f, g, h, current_node, new_loc))
                            heapify(open_nodes)
                        else:
                            continue

                    else:
                        heappush(open_nodes, AStarNode(f, g, h, current_node, new_loc))

                else:
                    continue

    return path


def manhattan_distance(p1: Position, p2: Position) -> int:
    """
    Compute a Manhattan distance of two points

    Parameters:
    p1 (Position): a location
    p2 (Position): another location

    Returns:
    distance (int): Manhattan distance of the two points
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
