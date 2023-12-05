from pathlib import Path


def generate_value_for_each_cycle(lines: list[str]) -> None:
    value = 1
    for line in lines:
        if line == "noop":
            yield value
        elif line.startswith("add"):
            new_value = int(line.strip().split(" ")[1])
            yield value
            value += new_value
            yield value
        else:
            raise ValueError(f"Unknown line: {line}")


def calculate_signal_strength(lines: list[str]) -> int:
    relevant_cycles = (v + 20 for v in range(0, 201, 40))
    next_relevant_cycle = next(relevant_cycles)
    for i, value in enumerate(generate_value_for_each_cycle(lines), start=2):
        if i == next_relevant_cycle:
            print(f"Cycle {i}: {value}")
            yield value * next_relevant_cycle
            try:
                next_relevant_cycle = next(relevant_cycles)
            except StopIteration:
                break


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    #     input_text = """addx 15
    # addx -11
    # addx 6
    # addx -3
    # addx 5
    # addx -1
    # addx -8
    # addx 13
    # addx 4
    # noop
    # addx -1
    # addx 5
    # addx -1
    # addx 5
    # addx -1
    # addx 5
    # addx -1
    # addx 5
    # addx -1
    # addx -35
    # addx 1
    # addx 24
    # addx -19
    # addx 1
    # addx 16
    # addx -11
    # noop
    # noop
    # addx 21
    # addx -15
    # noop
    # noop
    # addx -3
    # addx 9
    # addx 1
    # addx -3
    # addx 8
    # addx 1
    # addx 5
    # noop
    # noop
    # noop
    # noop
    # noop
    # addx -36
    # noop
    # addx 1
    # addx 7
    # noop
    # noop
    # noop
    # addx 2
    # addx 6
    # noop
    # noop
    # noop
    # noop
    # noop
    # addx 1
    # noop
    # noop
    # addx 7
    # addx 1
    # noop
    # addx -13
    # addx 13
    # addx 7
    # noop
    # addx 1
    # addx -33
    # noop
    # noop
    # noop
    # addx 2
    # noop
    # noop
    # noop
    # addx 8
    # noop
    # addx -1
    # addx 2
    # addx 1
    # noop
    # addx 17
    # addx -9
    # addx 1
    # addx 1
    # addx -3
    # addx 11
    # noop
    # noop
    # addx 1
    # noop
    # addx 1
    # noop
    # noop
    # addx -13
    # addx -19
    # addx 1
    # addx 3
    # addx 26
    # addx -30
    # addx 12
    # addx -1
    # addx 3
    # addx 1
    # noop
    # noop
    # noop
    # addx -9
    # addx 18
    # addx 1
    # addx 2
    # noop
    # noop
    # addx 9
    # noop
    # noop
    # noop
    # addx -1
    # addx 2
    # addx -37
    # addx 1
    # addx 3
    # noop
    # addx 15
    # addx -21
    # addx 22
    # addx -6
    # addx 1
    # noop
    # addx 2
    # addx 1
    # noop
    # addx -10
    # noop
    # noop
    # addx 20
    # addx 1
    # addx 2
    # addx 2
    # addx -6
    # addx -11
    # noop
    # noop
    # noop"""

    print(sum(calculate_signal_strength(input_text.splitlines())))


if __name__ == "__main__":
    main()
