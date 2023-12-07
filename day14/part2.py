import sys
from itertools import count
from pathlib import Path


def draw_rocks(rocks: set[tuple[int, int]], sand_particles: set[tuple[int, int]]):
    min_x = min(rocks, key=lambda x: x[0])[0]
    max_x = max(rocks, key=lambda x: x[0])[0]
    min_y = min(rocks, key=lambda x: x[1])[1]
    max_y = max(rocks, key=lambda x: x[1])[1]

    min_y = min(min_y, 0)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            point = (x, y)
            string = "#" if point in rocks else "o" if point in sand_particles else "."
            print(string, end="")
        print()


def parse(data: str) -> set[tuple[int, int]]:
    lines = data.splitlines()

    rocks: set[int, int] = set()

    for line in lines:
        pairs = line.split(" -> ")
        path_points = [tuple(map(int, pair.split(","))) for pair in pairs]

        for start, stop in zip(path_points[:-1], path_points[1:]):
            # exactly one of the coordinates must be the same
            assert (start[0] == stop[0]) + (start[1] == stop[1]) == 1
            dim_to_iterate_over = 0 if start[1] == stop[1] else 1

            low, high = sorted([start[dim_to_iterate_over], stop[dim_to_iterate_over]])
            for i in range(low, high + 1):
                if dim_to_iterate_over == 0:
                    rocks.add((i, start[1]))
                else:
                    rocks.add((start[0], i))

    return rocks


def simulate_round(
    rocks: set[tuple[int, int]], sand_particles: set[tuple[int, int]]
) -> tuple[tuple[int, int], bool]:
    # Start a particle from (500, 0) and run until it rests

    all_obstacles = rocks | sand_particles

    max_y = max(rocks, key=lambda x: x[1])[1]

    start_position = (500, 0)

    particle = start_position
    prev_particle: tuple[int, int] | None = None
    while True:
        # move down
        particle_down = (particle[0], particle[1] + 1)
        # move down left
        particle_down_left = (particle[0] - 1, particle[1] + 1)
        # move down right
        particle_down_right = (particle[0] + 1, particle[1] + 1)
        if particle[1] >= max_y + 1:
            is_final_particle = False
            break
        elif particle_down not in all_obstacles:
            particle = particle_down
        elif particle_down_left not in all_obstacles:
            particle = particle_down_left
        elif particle_down_right not in all_obstacles:
            particle = particle_down_right

        if particle == prev_particle:
            is_final_particle = particle == start_position
            break

        prev_particle = particle

    return particle, is_final_particle


def main(fname: str) -> None:
    data = Path(fname).read_text()

    rocks = parse(data)
    sand_particles: set[tuple[int, int]] = set()

    for i in count(start=1):
        new_particle, is_final_particle = simulate_round(rocks, sand_particles)
        if not is_final_particle:
            sand_particles.add(new_particle)
        else:
            break

    print(i)


if __name__ == "__main__":
    try:
        fname, *_ = sys.argv[1:]
    except ValueError:
        fname = str(Path(__file__).absolute().parent / "example_data.txt")
    main(fname)
