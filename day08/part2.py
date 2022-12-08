from itertools import product
from pathlib import Path
from typing import Iterable

import numpy as np


def direction_line_n_visible(value: int, line: np.ndarray) -> int:

    mask_is_lower_than_value = line < value
    is_visible_mask = np.logical_and.accumulate(mask_is_lower_than_value)
    out = is_visible_mask.sum() + 1 * (False in is_visible_mask)
    return int(out)


def iterate_scores(array: np.ndarray) -> Iterable[int]:
    for y,x in product(range(array.shape[0]), range(array.shape[1])):
        value = array[y,x]
        top_line = array[:y,x][::-1]
        bottom_line = array[y+1:,x]
        left_line = array[y,:x][::-1]
        right_line = array[y,x+1:]


        up_score = direction_line_n_visible(value, top_line)
        down_score = direction_line_n_visible(value, bottom_line)
        left_score = direction_line_n_visible(value, left_line)
        right_score = direction_line_n_visible(value, right_line)


        n_visible = np.multiply.reduce([up_score, down_score, left_score, right_score])

        yield int(n_visible)



def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    array = np.array([list(map(int, line)) for line in input_text.splitlines()])

    print(max(iterate_scores(array)))

    


    


if __name__ == "__main__":
    main()
