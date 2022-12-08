from pathlib import Path

import numpy as np


def middle_is_visible_from_top_mask(array: np.ndarray) -> np.ndarray:
    relevant_array = array[:-1, 1:-1]
    is_visible = np.diff(np.maximum.accumulate(relevant_array, axis=0), axis=0) > 0
    return is_visible


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    array = np.array([list(map(int, line)) for line in input_text.splitlines()])

    top_mask = middle_is_visible_from_top_mask(array)
    bottom_mask = middle_is_visible_from_top_mask(array[::-1])[::-1]
    left_mask = middle_is_visible_from_top_mask(array.T).T
    right_mask = middle_is_visible_from_top_mask(array.T[::-1])[::-1].T

    any_mask = np.logical_or.reduce([top_mask, bottom_mask, left_mask, right_mask])

    inside_n_visible = np.sum(any_mask)
    outside_n_visible = 2 * array.shape[0] + 2 * (array.shape[1] - 2)

    print(inside_n_visible + outside_n_visible)


if __name__ == "__main__":
    main()
