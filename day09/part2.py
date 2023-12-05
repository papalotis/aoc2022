from enum import Enum
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt

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

    input_text = """R 4
    U 4
    L 3
    D 1
    R 4
    D 1
    L 5
    R 2"""

    input_text = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""
    # input_text = "R 15\nU 15"

    rope_elements = [(0, 0) for _ in range(10)]
    tail_positions = set()

    for direction, distance in parse_input(input_text.splitlines()):
        for _ in range(distance):
            old_rope_element_positions = rope_elements.copy()
            new_rope_elements = [tuple_add(rope_elements[0], direction)]

            for i, (old_element_ahead, element_behind) in enumerate(
                zip(old_rope_element_positions[:-1], rope_elements[1:])
            ):
                element_ahead = new_rope_elements[i]

                element_behind_position = move_tail(
                    element_ahead, old_element_ahead, element_behind
                )
                new_rope_elements.append(element_behind_position)

            rope_elements[:] = new_rope_elements
            tail_positions.add(rope_elements[-1])
            print(rope_elements[-1])

            # plt.plot([0], [0], 'go')

            # for x,y in rope_elements[:-1]:
            #     plt.plot([x], [y], 'ro')
            #     plt.xlim(-20, 20)
            #     plt.ylim(-20, 20)

            # plt.plot([rope_elements[-1][0]], [rope_elements[-1][1]], 'ko')

            # plt.show()

    for tail_pos in tail_positions:
        plt.plot([tail_pos[0]], [tail_pos[1]], "ko")
        plt.xlim(-20, 20)
        plt.ylim(-20, 20)

    plt.show()

    print(len(tail_positions))


if __name__ == "__main__":
    main()
