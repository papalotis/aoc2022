import re
from pathlib import Path


def parse_line(line: str) -> tuple[tuple[int, int], tuple[int, int]]:
    match = re.match(r"(\d+)-(\d+),(\d+)-(\d+)", line)
    start_1, end_1, start_2, end_2 = map(int, match.groups())
    return ((start_1, end_1), (start_2, end_2))


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    parsed_pairs = map(parse_line, input_text.splitlines())

    print(
        sum(
            (
                pair_2_end in range(pair_1_start, pair_1_end + 1)
                and part_2_start in range(pair_1_start, pair_1_end + 1)
            )
            or (
                pair_1_end in range(part_2_start, pair_2_end + 1)
                and pair_1_start in range(part_2_start, pair_2_end + 1)
            )
            for (pair_1_start, pair_1_end), (part_2_start, pair_2_end) in parsed_pairs
        )
    )


if __name__ == "__main__":
    main()
