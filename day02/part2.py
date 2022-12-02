from enum import Enum
from pathlib import Path


class Move(int, Enum):
    ROCK = A = 1
    PAPER = B = 2
    SCISSORS = C = 3


class Result(Enum):
    LOSE = X = 0
    DRAW = Y = 3
    WIN = Z = 6


MOVE_FOR_RESULT = {
    (Result.LOSE, Move.PAPER): Move.ROCK,
    (Result.LOSE, Move.ROCK): Move.SCISSORS,
    (Result.LOSE, Move.SCISSORS): Move.PAPER,
    (Result.DRAW, Move.PAPER): Move.PAPER,
    (Result.DRAW, Move.ROCK): Move.ROCK,
    (Result.DRAW, Move.SCISSORS): Move.SCISSORS,
    (Result.WIN, Move.PAPER): Move.SCISSORS,
    (Result.WIN, Move.ROCK): Move.PAPER,
    (Result.WIN, Move.SCISSORS): Move.ROCK,
}


def parse_line(line: str) -> tuple[Move, Result]:
    opponent, result = line.split(" ")
    return Move[opponent], Result[result]


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    games = (parse_line(line) for line in input_text.splitlines())

    player_scores = (
        MOVE_FOR_RESULT[result, opponent_move] + result.value
        for opponent_move, result in games
    )

    print(sum(player_scores))


if __name__ == "__main__":
    main()
