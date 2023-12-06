from typing import Any

import re

from utils.handle_file import read_file


def get_categories(lines: str, expression: str) -> list[str]:
    pattern = re.compile(expression)
    categories: list[str] = []

    for line in lines:
        if "map" not in line:
            pass
        else:
            category = pattern.search(line).group(1)
            categories.append(category)

    return categories


def get_seeds(line: str) -> list[int]:
    pattern = re.compile("(\d+)")
    seeds = pattern.findall(line)
    return [int(s) for s in seeds]


def get_new_seeds(line: str) -> list[tuple[int, int]]:
    pattern = re.compile("(\d+)")
    all_numbers = pattern.findall(line)
    seeds: list[tuple[int, int]] = []

    for i in range(0, len(all_numbers), 2):
        seeds.append((int(all_numbers[i]), int(all_numbers[i + 1])))

    return sorted(seeds)


def is_valid_seed(seed: int, seeds: list[tuple[int, int]]) -> bool:
    for s in seeds:
        source_range = s[0]
        length_range = s[1]

        if source_range <= seed and seed < source_range + length_range:
            return True

    return False


def get_map(
    lines: list[str],
    source: str,
    destination: str,
) -> list[tuple[int, int, int]]:
    section_start = lines.index(f"{source}-to-{destination} map:")
    source_to_destination: list[tuple[int, int, int]] = []
    index = 1

    while section_start + index < len(lines) and lines[section_start + index] != "":
        current_line = lines[section_start + index]
        col_1, col_2, col_3 = current_line.split(" ")
        index += 1

        source_to_destination.append((int(col_2), int(col_1), int(col_3)))

    return sorted(source_to_destination)


def generate_almanac(lines: str) -> list[dict[str, Any]]:
    sources = get_categories(lines, "(\w+)-to")
    destinations = get_categories(lines, "to-(\w+)")

    almanac: list[dict[str, Any]] = []

    for i in range(len(sources)):
        source = sources[i]
        destination = destinations[i]
        source_to_destination_map = get_map(lines, source, destination)

        almanac.append(
            {
                "source": source,
                "destination": destination,
                "map": source_to_destination_map,
            }
        )

    return almanac


def get_map_result(
    permutations: list[tuple[int, int, int]],
    x: int,
    reverse: bool = False,
) -> bool:
    for p in permutations:
        source_range = None
        destination_range = None
        length_range = p[2]

        if reverse is True:
            source_range = p[1]
            destination_range = p[0]
        else:
            source_range = p[0]
            destination_range = p[1]

        if source_range <= x and x < source_range + length_range:
            return destination_range + (x - source_range)

    return x


def go_through_almanac(
    seed: int,
    almanac: list[dict[str, Any]],
    reverse: bool = False,
) -> int:
    result = seed

    if reverse is True:
        almanac = almanac[::-1]

    for step in almanac:
        result = get_map_result(step["map"], result, reverse)

    return result


if __name__ == "__main__":
    filename = "inputs/day_5.txt"
    lines = read_file(filename)

    seeds = get_seeds(lines[0])
    almanac = generate_almanac(lines)

    results_1: list[int] = []

    for seed in seeds:
        results_1.append(go_through_almanac(seed, almanac))

    result_1 = min(results_1)

    print(result_1)

    new_seeds = get_new_seeds(lines[0])

    result_2 = 0
    seed = go_through_almanac(result_2, almanac, True)

    while is_valid_seed(seed, new_seeds) is False:
        result_2 += 1
        seed = go_through_almanac(result_2, almanac, True)

    print(result_2)
