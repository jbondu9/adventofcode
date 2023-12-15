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


def get_all_nodes(ends_with: str, network: str) -> list[str]:
    pattern = re.compile("([A-Z1-9]{2}" + f"{ends_with}" + "{1} =)")
    nodes = pattern.findall(network)
    return [n[:3] for n in nodes]


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

    i = 0
    starting_nodes = get_all_nodes("A", "\n".join(data[2:]))
    ending_nodes = get_all_nodes("Z", "\n".join(data[2:]))
    result_2 = 0

    while set(starting_nodes).issubset(ending_nodes) is not True:
        starting_nodes = [
            get_next_node(n, instruction_sequence[i], data[2:]) for n in starting_nodes
        ]
        i = (i + 1) % n_instructions
        result_2 += 1

    print(result_2)
