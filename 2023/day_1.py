import re

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


def read_file(filename: str) -> str:
    try:
        with open(filename) as file:
            return file.read()
    except OSError:
        return ""


def word_to_number(word: str, reverse=False) -> int:
    try:
        return int(word)
    except ValueError:
        if reverse is True:
            word = word[::-1]
        return int(DIGIT_WORDS[word])


def build_pattern(with_word=False, reverse=False) -> str:
    p = "\d"

    if with_word is True:
        for w in DIGIT_WORDS.keys():
            if reverse is True:
                w = w[::-1]
            p += "|" + w

    return f"({p})"


def find_first_digit(line: str, with_word=False, reverse=False) -> int:
    p = re.compile(build_pattern(with_word, reverse))
    return word_to_number(p.search(line).group(), reverse)


if __name__ == "__main__":
    filename = "../inputs/day_1.txt"
    data = read_file(filename)
    result = 0

    for line in data.split("\n")[:-1]:
        tens_digit = find_first_digit(line, False) * 10
        units_digit = find_first_digit(line[::-1], False, False)
        result += tens_digit + units_digit

    print(result)
