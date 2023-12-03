from typing import Any, Generator

import re

from utils.handle_file import read_file

MAX_RED_CUBES = 12
MAX_GREEN_CUBES = 13
MAX_BLUE_CUBES = 14


def get_game_id(line: str) -> int:
    p = re.compile("Game \d+")
    return int(p.search(line).group().split(" ")[-1])


def get_cubes(line: str, color: str) -> Generator[int, Any, None]:
    p = re.compile(f"\d+ {color}")
    cubes = p.findall(line)

    for c in cubes:
        try:
            yield int(c.split(" ")[0])
        except ValueError:
            yield 0


def is_valid_game(
    game: str,
    max_red_cubes=MAX_RED_CUBES,
    max_green_cubes=MAX_GREEN_CUBES,
    max_blue_cubes=MAX_BLUE_CUBES,
) -> bool:
    red_cubes = get_cubes(game, "red")
    green_cubes = get_cubes(game, "green")
    blue_cubes = get_cubes(game, "blue")

    for c in red_cubes:
        if c > max_red_cubes:
            return False

    for c in green_cubes:
        if c > max_green_cubes:
            return False

    for c in blue_cubes:
        if c > max_blue_cubes:
            return False

    return True


def get_power_of_game(game: str) -> int:
    red_cubes = get_cubes(game, "red")
    green_cubes = get_cubes(game, "green")
    blue_cubes = get_cubes(game, "blue")

    max_red_cubes = 0
    for c in red_cubes:
        if c > max_red_cubes:
            max_red_cubes = c

    max_green_cubes = 0
    for c in green_cubes:
        if c > max_green_cubes:
            max_green_cubes = c

    max_blue_cubes = 0
    for c in blue_cubes:
        if c > max_blue_cubes:
            max_blue_cubes = c

    return max_red_cubes * max_green_cubes * max_blue_cubes


if __name__ == "__main__":
    filename = "inputs/day_2.txt"
    lines = read_file(filename)

    result_1 = 0
    result_2 = 0

    for line in lines:
        if is_valid_game(line) is True:
            result_1 += get_game_id(line)

        result_2 += get_power_of_game(line)

    print(f"Answer n°1: {result_1}")
    print(f"Answer n°2: {result_2}")
