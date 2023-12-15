import re

from utils.handle_file import read_file


def get_next_node(label: str, instruction: str, network: list[str]) -> str:
    pattern = re.compile("([A-Z1-9]{3}, [A-Z1-9]{3})")

    for node in network:
        if node.startswith(label):
            left, right = pattern.search(node).group().split(", ")

            if instruction == "L":
                return left
            else:
                return right

    return ""


if __name__ == "__main__":
    filename = "inputs/day_8.txt"
    data = read_file(filename)

    instruction_sequence = data[0]
    n_instructions = len(instruction_sequence)

    i = 0
    label = "AAA"
    result_1 = 0

    while label != "ZZZ":
        label = get_next_node(label, instruction_sequence[i], data[2:])
        i = (i + 1) % n_instructions
        result_1 += 1

    print(result_1)
