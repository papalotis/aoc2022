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
            neighbors = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
            for ni, nj in neighbors:
                try:
                    other_char = lines[ni][nj]
                except IndexError:
                    pass
                else:
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

    print(nx.shortest_path_length(*parse(data)))


if __name__ == "__main__":
    try:
        fname, *_ = sys.argv[1:]
    except ValueError:
        fname = str(Path(__file__).absolute().parent / "example_data.txt")
    main(fname)
