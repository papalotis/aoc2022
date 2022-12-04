from functools import cache
from itertools import islice, tee
from pathlib import Path
from string import ascii_letters
from typing import Iterable


def split_into_sets_of_n(
    lines: Iterable[str], n: int
) -> Iterable[tuple[set[str], ...]]:
    lines_as_sets = map(set, iter(lines))

    iters = tee(lines_as_sets, n)

    zip_args = (islice(k_iter, k, None, n) for k, k_iter in enumerate(iters))

    return zip(*zip_args)


@cache
def calculate_priority_of_item(item: str) -> int:
    return ascii_letters.index(item) + 1


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    priorities_common_letter_in_groups = (
        calculate_priority_of_item(set.intersection(*chunk).pop())
        for chunk in split_into_sets_of_n(input_text.splitlines(), 3)
    )

    print(sum(priorities_common_letter_in_groups))


if __name__ == "__main__":
    main()
