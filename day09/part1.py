from enum import Enum
from pathlib import Path
from typing import Iterable

Vector2D = tuple[int, int]


class Direction(Vector2D, Enum):
    UP = U = (0, 1)
    DOWN = D = (0, -1)
    LEFT = L = (-1, 0)
    RIGHT = R = (1, 0)


Move = tuple[Direction, int]


def parse_input(input_lines: Iterable[str]) -> Iterable[Move]:
    for line in input_lines:
        direction, distance = line.split()

        yield Direction[direction], int(distance)


def tuple_add(a: Vector2D, b: Vector2D) -> Vector2D:
    return a[0] + b[0], a[1] + b[1]


def head_and_tail_on_same_line(head: Vector2D, tail: Vector2D) -> bool:
    return any(h_value == tail_value for h_value, tail_value in zip(head, tail))


def head_too_far_away_from_tail(head: Vector2D, tail: Vector2D) -> bool:
    return any(abs(h_value - tail_value) > 1 for h_value, tail_value in zip(head, tail))


def head_tail_manhattan_distance(head: Vector2D, tail: Vector2D) -> int:
    return sum(abs(h_value - tail_value) for h_value, tail_value in zip(head, tail))


def tail_should_move_because_on_same_line_and_too_far_away(
    new_head: Vector2D, tail: Vector2D
) -> bool:
    return head_and_tail_on_same_line(new_head, tail) and head_too_far_away_from_tail(
        new_head, tail
    )


def tail_should_move_because_not_on_same_line_and_too_far_away(
    new_head: Vector2D, tail: Vector2D
) -> bool:
    return (
        not head_and_tail_on_same_line(new_head, tail)
        and head_tail_manhattan_distance(new_head, tail) > 2
    )


def move_tail(new_head: Vector2D, old_head: Vector2D, tail: Vector2D) -> Vector2D:
    if tail_should_move_because_on_same_line_and_too_far_away(
        new_head, tail
    ) or tail_should_move_because_not_on_same_line_and_too_far_away(new_head, tail):
        return old_head

    return tail


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    #     input_text = """R 4
    # U 4
    # L 3
    # D 1
    # R 4
    # D 1
    # L 5
    # R 2"""

    head = (0, 0)
    tail = (0, 0)

    tail_positions = {tail}

    for direction, distance in parse_input(input_text.splitlines()):
        for _ in range(distance):
            old_head, head = head, tuple_add(head, direction)
            tail = move_tail(head, old_head, tail)

            tail_positions.add(tail)

    print(len(tail_positions))


if __name__ == "__main__":
    main()
