from pathlib import Path

from more_itertools import windowed


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    for position, window in enumerate(windowed(input_text, 4), start=4):
        if len(set(window)) == len(window):
            print(position)
            return


if __name__ == "__main__":
    main()
