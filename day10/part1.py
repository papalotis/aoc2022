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
            raise ValueError(f"Unknown line: {line:r}")


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

    print(sum(calculate_signal_strength(input_text.splitlines())))


if __name__ == "__main__":
    main()
