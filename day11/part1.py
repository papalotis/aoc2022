from __future__ import annotations

import sys
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import NamedTuple, Self


class MonkeyInspectionResult(NamedTuple):
    new_worry: int
    monkey_to_throw: int


@dataclass
class Operation:
    operand: str
    value_left: int | None
    value_right: int | None

    def __call__(self, worry: int) -> int:
        left = self.value_left if self.value_left is not None else worry
        right = self.value_right if self.value_right is not None else worry
        assert None not in (left, right)

        return int(eval(f"{left} {self.operand} {right}")) // 3

    @classmethod
    def from_string(cls, operation_string: str) -> Self:
        left, operand, right = operation_string.split()

        left = None if "old" in left else int(left)
        right = None if "old" in right else int(right)
        operand = operand.strip()

        return cls(operand, left, right)


@dataclass
class Monkey:
    items: deque[int]
    operation: Operation
    modulo_test_value: int
    monkey_to_throw_if_true: int
    monkey_to_throw_if_false: int
    number_of_inspected_items: int = field(default=0, init=False)

    @classmethod
    def from_string(cls, monkey_string: str) -> Self:
        texts = [x.strip() for x in monkey_string.splitlines()[1:]]

        items = deque(int(x) for x in texts[0].split(":")[1].split(","))
        modulo_test_value = int(texts[2].split("by ")[1])

        operation_string = texts[1].split("new = ")[1]
        operation = Operation.from_string(operation_string)

        monkey_to_throw_if_true = int(texts[3].split(" monkey ")[1])
        monkey_to_throw_if_false = int(texts[4].split(" monkey ")[1])

        return cls(
            items,
            operation,
            modulo_test_value,
            monkey_to_throw_if_true,
            monkey_to_throw_if_false,
        )

    def run_first_items(self) -> MonkeyInspectionResult:
        self.number_of_inspected_items += 1

        worry_first_item = self.items.popleft()

        new_worry = self.operation(worry_first_item)

        monkey_to_throw = (
            self.monkey_to_throw_if_true
            if new_worry % self.modulo_test_value == 0
            else self.monkey_to_throw_if_false
        )

        return MonkeyInspectionResult(new_worry, monkey_to_throw)


@dataclass
class MonkeyGame:
    monkeys: list[Monkey]

    def run_one_round(self) -> None:
        for monkey in self.monkeys:
            while len(monkey.items) > 0:
                result = monkey.run_first_items()
                self.monkeys[result.monkey_to_throw].items.append(result.new_worry)

    def run_rounds(self, rounds: int) -> None:
        for _ in range(rounds):
            self.run_one_round()

    @classmethod
    def from_string(cls, data: str) -> Self:
        monkeys = [Monkey.from_string(x) for x in data.split("\n\n")]
        return MonkeyGame(monkeys)


def main(fname: str) -> None:
    data = Path(fname).read_text()
    game = MonkeyGame.from_string(data)
    game.run_rounds(20)

    n_items_per_monkey = sorted(
        map(lambda x: x.number_of_inspected_items, game.monkeys)
    )
    *_, second_to_last, last = n_items_per_monkey

    print(second_to_last * last)


if __name__ == "__main__":
    fname, *_ = sys.argv[1:]
    main(fname)
