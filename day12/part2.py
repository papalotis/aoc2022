import sys
from pathlib import Path

import networkx as nx
import numpy as np
from numpy.typing import NDArray


def map_to_int(letter: str) -> int:
    if letter == "S":
        return 0
    if letter == "E":
        return 26

    return ord(letter) - ord("a")


def parse(data: str) -> tuple[NDArray[np.int64], NDArray[np.int64], NDArray[np.int64]]:
    rows = []
    start = None
    end = None

    for i, line in enumerate(data.splitlines()):
        values = list(map(map_to_int, line))
        rows.append(values)

        j = line.find("S")
        if j >= 0:
            start = (i, j)

        j = line.find("E")
        if j >= 0:
            end = (i, j)

    assert start is not None
    assert end is not None

    return np.array(rows), np.array(start), np.array(end)


def create_graph_from_maze(maze: NDArray[np.int64]) -> NDArray[np.int64]:
    indices = np.argwhere(maze >= 0)
    values = maze[indices[:, 0], indices[:, 1]]

    mask_2d_distance = (
        np.linalg.norm(indices[:, None, :] - indices[None, :, :], axis=-1) == 1
    )

    diffs = values[None, :] - values[:, None]

    mask_value = diffs < 2

    mask = mask_2d_distance & mask_value

    return nx.from_numpy_array(mask, create_using=nx.DiGraph)


def main(fname: str) -> None:
    data = Path(fname).read_text()

    maze, start, end = parse(data)

    graph = create_graph_from_maze(maze)

    # convert start and end to index
    start_nodes = np.nonzero(maze.ravel() == 0)[0]
    
    end_node = end[0] * maze.shape[1] + end[1]
    shortest_paths_length: dict[int, int] = nx.shortest_path_length(graph, target=end_node)

    print(min(shortest_paths_length.get(start_node, np.inf) for start_node in start_nodes))

if __name__ == "__main__":
    try:
        fname, *_ = sys.argv[1:]
    except ValueError:
        fname = str(Path(__file__).absolute().parent / "example_data.txt")
    main(fname)
