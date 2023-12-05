from utils.handle_file import read_file


def get_numbers(
    line: str,
    start_symbol: str,
    end_symbol: str = "",
) -> list[int]:
    i = line.index(start_symbol)

    if end_symbol != "":
        line = line[i : line.index(end_symbol)]
    else:
        line = line[i:]

    result: list[int] = []

    for number in line.split(" "):
        try:
            result.append(int(number))
        except ValueError:
            continue

    return result


def get_matching_numbers(line: str) -> int:
    winning_numbers = get_numbers(line, ":", "|")
    numbers_we_have = get_numbers(line, "|")

    return len(list(set(winning_numbers).intersection(numbers_we_have)))


def generate_scratchcard_map(n_scratchcards: int) -> dict:
    scratchcard_map = {}

    for i in range(n_scratchcards):
        scratchcard_map[str(i)] = 1

    return scratchcard_map


if __name__ == "__main__":
    filename = "inputs/day_4.txt"
    lines = read_file(filename)
    n_lines = len(lines)

    result_1 = 0
    result_2 = 0

    scratchcard_map = generate_scratchcard_map(n_lines)

    for i, line in enumerate(lines):
        matching_numbers = get_matching_numbers(line)

        if matching_numbers != 0:
            result_1 += 2 ** (matching_numbers - 1)

            start = min(i + 1, n_lines - 1)
            end = min(i + matching_numbers + 1, n_lines)

            for j in range(start, end):
                scratchcard_map[str(j)] += scratchcard_map[str(i)]

    for k in scratchcard_map.keys():
        result_2 += scratchcard_map[k]

    print(result_1)
    print(result_2)
