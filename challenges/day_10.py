from math import floor

from utils.handle_file import read_file


def find_starting_point(lines: list[str]) -> tuple[int, int]:
    row = 0
    col = 0

    while True:
        if "S" in lines[row]:
            col = lines[row].index("S")
            break
        row += 1

    return (row, col)


def get_next_tile(
    lines: list[str],
    row: int,
    col: int,
    direction: str,
) -> tuple[int, int, str]:
    current_tile = lines[row][col]

    if current_tile == "|":
        if (
            direction == "NS"
            and row < len(lines) - 1
            and lines[row + 1][col] in ["L", "J", "|", "S"]
        ):
            if lines[row + 1][col] == "S":
                direction = ""
            return (row + 1, col, direction)
        elif (
            direction == "SN"
            and 0 < row
            and lines[row - 1][col] in ["F", "7", "|", "S"]
        ):
            if lines[row - 1][col] == "S":
                direction = ""
            return (row - 1, col, direction)

    elif current_tile == "-":
        if (
            direction == "WE"
            and col < len(lines[row]) - 1
            and lines[row][col + 1] in ["J", "7", "-", "S"]
        ):
            if lines[row][col + 1] == "S":
                direction = ""
            return (row, col + 1, direction)
        elif (
            direction == "EW"
            and 0 < col
            and lines[row][col - 1] in ["L", "F", "-", "S"]
        ):
            if lines[row][col - 1] == "S":
                direction = ""
            return (row, col - 1, direction)

    elif current_tile == "L":
        if (
            direction == "NS"
            and col < len(lines[row]) - 1
            and lines[row][col + 1] in ["7", "J", "-", "S"]
        ):
            direction = "WE"
            if lines[row][col + 1] == "S":
                direction = ""
            return (row, col + 1, direction)
        elif (
            direction == "EW"
            and 0 < row
            and lines[row - 1][col] in ["7", "F", "|", "S"]
        ):
            direction = "SN"
            if lines[row - 1][col] == "S":
                direction = ""
            return (row - 1, col, direction)

    elif current_tile == "J":
        if (
            direction == "NS"
            and 0 < col
            and lines[row][col - 1] in ["F", "L", "-", "S"]
        ):
            direction = "EW"
            if lines[row][col - 1] == "S":
                direction = ""
            return (row, col - 1, direction)
        elif (
            direction == "WE"
            and 0 < row
            and lines[row - 1][col] in ["|", "F", "7", "S"]
        ):
            direction = "SN"
            if lines[row - 1][col] == "S":
                direction = ""
            return (row - 1, col, direction)

    elif current_tile == "7":
        if (
            direction == "WE"
            and row < len(lines) - 1
            and lines[row + 1][col] in ["|", "L", "J", "S"]
        ):
            direction = "NS"
            if lines[row + 1][col] == "S":
                direction = ""
            return (row + 1, col, direction)
        elif (
            direction == "SN"
            and 0 < col
            and lines[row][col - 1] in ["-", "L", "F", "S"]
        ):
            direction = "EW"
            if lines[row][col - 1] == "S":
                direction = ""
            return (row, col - 1, direction)

    elif current_tile == "F":
        if (
            direction == "SN"
            and col < len(lines[row]) - 1
            and lines[row][col + 1] in ["J", "7", "-", "S"]
        ):
            direction = "WE"
            if lines[row][col + 1] == "S":
                direction = ""
            return (row, col + 1, direction)
        elif (
            direction == "EW"
            and row < len(lines) - 1
            and lines[row + 1][col] in ["|", "J", "L", "S"]
        ):
            direction = "NS"
            if lines[row + 1][col] == "S":
                direction = ""
            return (row + 1, col, direction)

    elif current_tile == "S":
        if (
            direction == "NS"
            and row < len(lines) - 1
            and lines[row + 1][col] in ["|", "L", "J"]
        ):
            return (row + 1, col, "NS")
        elif direction == "SN" and 1 < row and lines[row - 1][col] in ["7", "F", "|"]:
            return (row - 1, col, "SN")
        elif (
            direction == "WE"
            and col < len(lines[row]) - 1
            and lines[row][col + 1] in ["-", "7", "J"]
        ):
            return (row, col + 1, "WE")
        elif direction == "EW" and 1 < col and lines[row][col - 1] in ["F", "L", "-"]:
            return (row, col - 1, "EW")

    return (row, col, "")


def get_farthest_point(lines: list[str], direction: str) -> int:
    row, col = find_starting_point(lines)
    distance = 0

    while direction != "":
        row, col, direction = get_next_tile(lines, row, col, direction)
        distance += 1

    if lines[row][col] == "S":
        return floor(distance / 2)
    return distance


if __name__ == "__main__":
    filename = "inputs/day_10.txt"
    data = read_file(filename)

    directions = ["NS", "SN", "WE", "EW"]

    results_1 = [get_farthest_point(data, direction) for direction in directions]

    print(max(results_1))
