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
        direct_directory_size.keys(),
        key=lambda key: (str(key).count("/"), len(str(key))),
        reverse=True,
    )
    for directory in dirs:
        subdirectories_total_size = sum(
            size
            for existing_dir, size in final_sizes.items()
            if existing_dir.parent == directory
        )

        final_size = subdirectories_total_size + direct_directory_size[directory]

        final_sizes[directory] = final_size

    used_space = max(final_sizes.values())
    total_space = 70_000_000
    unused_space = total_space - used_space
    needed_space = 30_000_000

    space_to_delete = needed_space - unused_space

    return min(filter(lambda size: size >= space_to_delete, final_sizes.values()))


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    #     input_text = """$ cd /
    # $ ls
    # dir a
    # 14848514 b.txt
    # 8504156 c.dat
    # dir d
    # $ cd a
    # $ ls
    # dir e
    # 29116 f
    # 2557 g
    # 62596 h.lst
    # $ cd e
    # $ ls
    # 584 i
    # $ cd ..
    # $ cd ..
    # $ cd d
    # $ ls
    # 4060174 j
    # 8033020 d.log
    # 5626152 d.ext
    # 7214296 k
    # """

    print(solve(input_text.splitlines()))


if __name__ == "__main__":
    main()
