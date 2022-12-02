from enum import Enum
from pathlib import Path


class Move(int, Enum):
    ROCK = A = X = 1
    PAPER = B = Y = 2
    SCISSORS = C = Z = 3


MOVE_BEATS_MOVE = {
    Move.PAPER: Move.ROCK,
    Move.ROCK: Move.SCISSORS,
    Move.SCISSORS: Move.PAPER,
}


def parse_line(line: str) -> tuple[Move, Move]:
    opponent, result = line.split(" ")
    return Move[opponent], Move[result]


def main() -> None:
    input_text = (Path(__file__).parent / "input.txt").read_text()

    games = (parse_line(line) for line in input_text.splitlines())

    player_scores = (
        player_move
        + 3 * (opponent_move == player_move)
        + 6 * (MOVE_BEATS_MOVE[player_move] == opponent_move)
        for opponent_move, player_move in games
    )

    print(sum(player_scores))


if __name__ == "__main__":
    main()
