import sys
from pathlib import Path

import networkx as nx


def letter_diff(letter_a: str, letter_b: str) -> int:
    mapper = {"S": "a", "E": "z"}

    letter_a = mapper.get(letter_a, letter_a)
    letter_b = mapper.get(letter_b, letter_b)

    return ord(letter_a) - ord(letter_b)


NodeType = tuple[int, int]


def parse(data: str) -> tuple[nx.DiGraph, NodeType, NodeType]:
    graph = nx.DiGraph()

    start = None
    end = None

    lines = data.splitlines()

    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            graph.add_node((i, j), char=char)

            neighbors = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
            for ni, nj in neighbors:
                if ni < 0 or ni >= len(lines) or nj < 0 or nj >= len(lines[ni]):
                    continue

                other_char = lines[ni][nj]
                diff = letter_diff(other_char, char)
                if diff < 2:
                    graph.add_edge((i, j), (ni, nj))

            if char == "S":
                start = (i, j)

            if char == "E":
                end = (i, j)

    assert start is not None
    assert end is not None

    return graph, start, end


def main(fname: str) -> None:
    data = Path(fname).read_text()

    graph, _, end = parse(data)

    start_nodes = [
        node for node, data in graph.nodes(data=True) if data["char"] in "aS"
    ]

    shortest_paths_length: dict[int, int] = nx.shortest_path_length(graph, target=end)

    print(
        min(
            shortest_paths_length.get(start_node, float("inf"))
            for start_node in start_nodes
        )
    )


if __name__ == "__main__":
    try:
        fname, *_ = sys.argv[1:]
    except ValueError:
        fname = str(Path(__file__).absolute().parent / "example_data.txt")
    main(fname)
