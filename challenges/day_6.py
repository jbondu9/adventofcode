from typing import Any, Generator

import re

from utils.handle_file import read_file


def get_races(times: str, distances: str) -> Generator[tuple[int, int], Any, None]:
    pattern = re.compile("(\d+)")

    new_times = [int(t) for t in pattern.findall(times)]
    new_distances = [int(d) for d in pattern.findall(distances)]

    for i in range(len(new_times)):
        yield (new_times[i], new_distances[i])


def get_only_race(time: str, distance: str) -> tuple[int, int]:
    pattern = re.compile("(\d+)")

    total_time = int("".join(pattern.findall(time)))
    total_distance = int("".join(pattern.findall(distance)))

    return (total_time, total_distance)


def get_times_to_win(race: tuple[int, int]) -> int:
    duration = race[0]
    best_record = race[1]

    possible_holding_times: list[int] = []

    for holding_time in range(duration + 1):
        distance_traveled = (duration - holding_time) * holding_time

        if distance_traveled > best_record:
            possible_holding_times.append(distance_traveled)

    return len(possible_holding_times)


if __name__ == "__main__":
    filename = "inputs/day_6.txt"
    data = read_file(filename)

    races = get_races(data[0], data[1])
    result_1 = 1

    for race in races:
        result_1 *= get_times_to_win(race)

    print(result_1)

    only_race = get_only_race(data[0], data[1])
    result_2 = get_times_to_win(only_race)

    print(result_2)
