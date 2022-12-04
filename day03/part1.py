from functools import cache
from pathlib import Path
from string import ascii_letters
from typing import Iterable


def split_line_into_sets(lines: Iterable[str]) -> Iterable[tuple[set[str], set[str]]]:
    for line in lines:
        half_length = len(line) // 2
        yield set(line[:half_length]), set(line[half_length:])


@cache
def calculate_priority_of_item(item: str) -> int:
    return ascii_letters.index(item) + 1


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    common_items = (
        left.intersection(right).pop()
        for left, right in split_line_into_sets(input_text.splitlines())
    )

    priority_of_items = map(calculate_priority_of_item, common_items)

    print(sum(priority_of_items))


if __name__ == "__main__":
    main()
