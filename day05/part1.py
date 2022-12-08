import re
from collections import deque
from pathlib import Path

from more_itertools import chunked


def parse_input(
    lines: list[str],
) -> tuple[list[deque[str]], list[tuple[int, int, int]]]:
    first_line = lines[0]
    n_stacks = len(first_line) // 4 + 1
    stacks: list[deque[int]] = [deque() for _ in range(n_stacks)]

    # create one iterator
    line_iter = iter(lines)

    # parse stacks
    for line in line_iter:

        if line == "":
            # stop parsing stacks
            break

        for stack, chunk in zip(stacks, chunked(line, 4)):
            if chunk[0] == "[":
                stack.appendleft(chunk[1])

    # parse moves
    moves: list[tuple[int, int, int]] = []
    for line in line_iter:
        amount, source, dest = map(
            int, re.match(r"move (\d+) from (\d+) to (\d+)", line).groups()
        )
        source, dest = source - 1, dest - 1  # subtract 1 to create indices
        moves.append((amount, source, dest))

    return stacks, moves


def inplace_move_stack_elements(
    stacks: list[deque[int]], amount: int, source_index: int, destination_index: int
) -> None:
    source_stack = stacks[source_index]
    destination_stack = stacks[destination_index]

    any(destination_stack.append(source_stack.pop()) for _ in range(amount))


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    stacks, moves = parse_input(input_text.splitlines())
    any(inplace_move_stack_elements(stacks, *move) for move in moves)

    out = "".join(stack[-1] for stack in stacks)
    print(out)


if __name__ == "__main__":
    main()
