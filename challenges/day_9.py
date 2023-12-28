from typing import Any, Generator

from utils.handle_file import read_file


def get_numbers(line: str) -> list[int]:
    numbers = line.split(" ")
    return [int(n) for n in numbers]


def get_new_line(line: list[int]) -> list[int]:
    return [line[i + 1] - line[i] for i in range(len(line) - 1)]


def is_zero_line(line: list[int]) -> bool:
    zero_line = [0] * len(line)
    return zero_line == line


def get_sequences(line: str) -> Generator[list[int], Any, None]:
    line = get_numbers(line)
    yield line

    while is_zero_line(line) is False:
        line = get_new_line(line)
        yield line


def get_forward_prediction(lines: Generator[list[int], Any, None]) -> int:
    last_numbers = [line[-1] for line in lines]

    prediction = last_numbers[-1]

    for i in range(len(last_numbers) - 1, -1, -1):
        prediction += last_numbers[i]

    return prediction


def get_backward_prediction(lines: Generator[list[int], Any, None]) -> int:
    first_numbers = [line[0] for line in lines]

    prediction = first_numbers[-1]

    for i in range(len(first_numbers) - 1, -1, -1):
        prediction = first_numbers[i] - prediction

    return prediction


if __name__ == "__main__":
    filename = "inputs/day_9.txt"
    data = read_file(filename)

    result_1 = 0
    result_2 = 0

    for line in data:
        sequences = get_sequences(line)
        result_1 += get_forward_prediction(sequences)

    for line in data:
        sequences = get_sequences(line)
        result_2 += get_backward_prediction(sequences)

    print(result_1)
    print(result_2)
