from collections import defaultdict
from pathlib import Path


def extract_direct_file_size_for_directories(lines: list[str]) -> dict[Path, int]:

    active_directory: Path | None = None

    direct_directory_size: defaultdict[Path, int] = defaultdict(int)

    for line in lines:
        if line.startswith("$ ls"):
            pass

        elif line.startswith("$ cd"):
            new_directory = line.split()[-1]
            if new_directory == "..":
                assert active_directory is not None
                active_directory = active_directory.parent
            elif active_directory is None or new_directory == "/":
                active_directory = Path(new_directory)
            else:
                active_directory = active_directory / new_directory
        else:
            try:
                file_size = int(line.split()[0])
            except ValueError:
                file_size = 0
            direct_directory_size[active_directory] += file_size

    return direct_directory_size


def solve(lines: list[str]) -> None:

    direct_directory_size = extract_direct_file_size_for_directories(lines)

    final_sizes: dict[Path, int] = {}
    # sort directories from deepest to shallowest
    dirs = sorted(
        direct_directory_size.keys(), key=lambda key: str(key).count("/"), reverse=True
    )
    for directory in dirs:
        final_size = (
            sum(
                size
                for existing_dir, size in final_sizes.items()
                if str(existing_dir).startswith(str(directory))
            )
            + direct_directory_size[directory]
        )

        final_sizes[directory] = final_size

    return sum(size for size in final_sizes.values() if size <= 100000)


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    print(solve(input_text.splitlines()))


if __name__ == "__main__":
    main()
