import math
import sys
from functools import cmp_to_key
from itertools import chain, zip_longest
from pathlib import Path
from typing import Iterable, Union

TaskList = list[Union[int, "TaskList"]]


def parse(data: str) -> Iterable[tuple[TaskList, TaskList]]:
    packets = data.split("\n\n")

    for packet in packets:
        packet_top, packet_bottom = packet.splitlines()

        left_part: TaskList = eval(packet_top)
        right_part: TaskList = eval(packet_bottom)

        yield left_part, right_part


def _print_compare_at_level(level: int, left: TaskList, right: TaskList) -> None:
    return
    string = "  " * level + f" - Compare: {left} vs {right}"
    print(string)


def _print_mixed_at_level(level: int, left: TaskList, right: TaskList) -> None:
    return
    left_is_list = isinstance(left, list)
    right_is_list = isinstance(right, list)
    assert left_is_list != right_is_list

    string = f"Mixed types; convert left to {[right if left_is_list else left]} and retry comparison"

    print("  " * level + string)


def _impl_packet_is_valid(left_part: TaskList, right_part: TaskList, level: int) -> int:
    # 1 means valid
    # -1 means invalid
    # 0 cannot determine

    _print_compare_at_level(level, left_part, right_part)

    for left, right in zip_longest(left_part, right_part):
        left_is_number = isinstance(left, int)
        right_is_number = isinstance(right, int)

        left_is_list = isinstance(left, list)
        right_is_list = isinstance(right, list)

        left_does_not_exist = left is None
        right_does_not_exist = right is None

        # _print_compare_at_level(level + 1, left, right)

        if left_is_number and right_is_number:
            _print_compare_at_level(level + 1, left, right)
            if left < right:
                return 1
            elif left > right:
                return -1

        elif left_is_list and right_is_list:
            result = _impl_packet_is_valid(left, right, level + 1)
            if result != 0:
                return result

        elif left_does_not_exist and not right_does_not_exist:
            return 1

        elif not left_does_not_exist and right_does_not_exist:
            return -1

        elif left_is_number and right_is_list:
            _print_mixed_at_level(level + 1, left, right)
            result = _impl_packet_is_valid([left], right, level + 1)
            if result != 0:
                return result

        elif left_is_list and right_is_number:
            _print_mixed_at_level(level + 1, left, right)
            result = _impl_packet_is_valid(left, [right], level + 1)
            if result != 0:
                return result

        else:
            raise ValueError(f"left={left!r}, right={right!r}")

    # cannot determine
    return 0


def is_valid_packet(left_part: TaskList, right_part: TaskList) -> bool:
    result = _impl_packet_is_valid(left_part, right_part, level=0)
    assert result in (-1, 0, 1)
    assert result != 0
    return result


DIVIDER_PACKET = ([[2]], [[6]])


def main(fname: str) -> None:
    data = Path(fname).read_text()

    packets = chain.from_iterable(chain(parse(data), [DIVIDER_PACKET]))

    sorted_packets = sorted(packets, key=cmp_to_key(is_valid_packet), reverse=True)

    print(
        math.prod(
            i
            for i, packet in enumerate(sorted_packets, start=1)
            if packet in DIVIDER_PACKET
        )
    )


if __name__ == "__main__":
    try:
        fname, *_ = sys.argv[1:]
    except ValueError:
        fname = str(Path(__file__).absolute().parent / "example_data.txt")
    main(fname)
