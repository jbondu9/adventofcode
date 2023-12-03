import re

from utils.handle_file import read_file

DIGIT_WORDS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def build_pattern(with_word=False, reverse=False) -> str:
    p = "\d"

    if with_word is True:
        for w in DIGIT_WORDS.keys():
            if reverse is True:
                w = w[::-1]
            p += "|" + w

    return f"({p})"


def word_to_number(word: str, reverse=False) -> int:
    try:
        return int(word)
    except ValueError:
        if reverse is True:
            word = word[::-1]
        return int(DIGIT_WORDS[word])


def find_first_digit(line: str, with_word=False, reverse=False) -> int:
    p = re.compile(build_pattern(with_word, reverse))

    if reverse is True:
        line = line[::-1]

    return word_to_number(p.search(line).group(), reverse)


if __name__ == "__main__":
    filename = "inputs/day_1.txt"
    lines = read_file(filename)

    result_1 = 0
    result_2 = 0

    for line in lines:
        tens_digit = find_first_digit(line) * 10
        units_digit = find_first_digit(line, reverse=True)
        result_1 += tens_digit + units_digit

        tens_digit = find_first_digit(line, with_word=True) * 10
        units_digit = find_first_digit(line, with_word=True, reverse=True)
        result_2 += tens_digit + units_digit

    print(f"Answer n°1: {result_1}")
    print(f"Answer n°2: {result_2}")
