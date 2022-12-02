from pathlib import Path
from typing import Iterable


def calories_per_elf(lines: list[str]) -> Iterable[int]:
    sum_calories = 0

    for line in lines:
        if line == "":
            yield sum_calories
            sum_calories = 0
        else:
            sum_calories += int(line)


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    print(sum(sorted(calories_per_elf(input_text.splitlines()))[-3:]))


if __name__ == "__main__":
    main()
