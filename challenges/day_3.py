from typing import Any, Generator

import re

from utils.handle_file import read_file


def find_expression_positions(
    line: str,
    expression: str,
) -> Generator[tuple[int, int], Any, None]:
    pattern = re.compile(expression)
    last_index = 0

    while pattern.search(line, last_index) is not None:
        positions = pattern.search(line, last_index).span()
        last_index = positions[1]
        yield positions


def get_neighbors(line: str, col_start: int, col_end, n_cols: int) -> str:
    if col_start == 0:
        return "." + line[col_start : col_end + 1]
    elif col_end == n_cols:
        return line[col_start - 1 : col_end] + "."
    return line[col_start - 1 : col_end + 1]


def get_neighborhood(
    row: int,
    col_start: int,
    col_end: int,
    lines: list[str],
    n_lines: int,
    n_cols: int,
) -> str:
    previous_line = ""
    line = get_neighbors(lines[row], col_start, col_end, n_cols)
    next_line = ""

    neighborhood_size = len(line)

    if row == 0:
        previous_line = "." * neighborhood_size
        next_line = lines[row + 1]
    elif row == n_lines - 1:
        previous_line = lines[row - 1]
        next_line = "." * neighborhood_size
    else:
        previous_line = lines[row - 1]
        next_line = lines[row + 1]

    previous_line = get_neighbors(previous_line, col_start, col_end, n_cols)
    next_line = get_neighbors(next_line, col_start, col_end, n_cols)

    return previous_line + line + next_line


def is_part_neighborhood(
    neighborhood: str,
    expression: str,
    neighbor_needed=1,
) -> bool:
    pattern = re.compile(expression)
    last_index = 0
    neighbor_found = 0

    while (
        pattern.search(neighborhood, last_index) is not None
        and neighbor_found < neighbor_needed
    ):
        last_index = pattern.search(neighborhood, last_index).span()[1]
        neighbor_found += 1

    return neighbor_found >= neighbor_needed


def are_neighbors(n_1: tuple[int, int, int], n_2: tuple[int, int, int]):
    if (n_1[0] - 1 <= n_2[0] and n_2[0] <= n_1[0] + 1) and (
        n_1[1] <= n_2[2] and n_2[1] <= n_1[2]
    ):
        return True
    return False


if __name__ == "__main__":
    filename = "inputs/day_3.txt"
    lines = read_file(filename)

    n_lines = len(lines)
    n_cols = len(lines[0])

    result_1 = 0
    result_2 = 0

    potential_gear_numbers = []
    gear_products = []

    for i in range(n_lines):
        number_positions = find_expression_positions(lines[i], "(\d+)")

        for number_position in number_positions:
            col_start, col_end = number_position
            neighborhood = get_neighborhood(
                i,
                col_start,
                col_end,
                lines,
                n_lines,
                n_cols,
            )

            if is_part_neighborhood(neighborhood, "([^0-9.])"):
                result_1 += int(lines[i][col_start:col_end])

                if is_part_neighborhood(neighborhood, "(\*)"):
                    potential_gear_numbers.append((i, col_start, col_end))

    for j in range(n_lines):
        gear_positions = find_expression_positions(lines[j], "(\*)")

        for gear_position in gear_positions:
            col_start, col_end = gear_position
            neighborhood = get_neighborhood(
                j,
                col_start,
                col_end,
                lines,
                n_lines,
                n_cols,
            )

            if is_part_neighborhood(neighborhood, "(\d+)", 2):
                gear_products.append((j, col_start, col_end))

    for gear in gear_products:
        product = 1

        for number in potential_gear_numbers:
            if are_neighbors(gear, number) is True:
                product *= int(lines[number[0]][number[1] : number[2]])

        result_2 += product

    print(result_1)
    print(result_2)
