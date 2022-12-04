from pathlib import Path


def parse_line(line: str) -> tuple[tuple[int, int], tuple[int, int]]:

    pair_1, pair_2 = line.split(",")

    pair_1_start, pair_1_end = pair_1.split("-")
    pair_2_start, pair_2_end = pair_2.split("-")
    return tuple(
        ((int(pair_1_start), int(pair_1_end)), (int(pair_2_start), int(pair_2_end)),)
    )


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    parsed_pairs = map(parse_line, input_text.splitlines())

    print(
        sum(
            pair_2_end in range(pair_1_start, pair_1_end + 1)
            or part_2_start in range(pair_1_start, pair_1_end + 1)
            or pair_1_end in range(part_2_start, pair_2_end + 1)
            or pair_1_start in range(part_2_start, pair_2_end + 1)
            for (pair_1_start, pair_1_end), (part_2_start, pair_2_end) in parsed_pairs
        )
    )


if __name__ == "__main__":
    main()
