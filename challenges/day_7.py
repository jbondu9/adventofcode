from enum import IntEnum
from functools import cmp_to_key

from utils.handle_file import read_file


CARD_RANK = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
NEW_CARD_RANK = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


class HandType(IntEnum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


def get_card_frequency(hand: str, new_rule: bool = False) -> list[tuple[str, int]]:
    card_frequency: dict[str, int] = {}

    for card in hand:
        if card in card_frequency:
            card_frequency[card] += 1
        else:
            card_frequency[card] = 1

    count_j = 0

    if new_rule is True and "J" in card_frequency and card_frequency["J"] != 5:
        count_j = card_frequency.pop("J")

    result = sorted(
        card_frequency.items(),
        key=lambda item: item[1],
        reverse=True,
    )

    if count_j != 0:
        max_frequency = list(result[0])
        max_frequency[1] += count_j

        return [tuple(max_frequency)] + result[1:]

    return result


def get_hand_type(hand: str, new_type: bool = False) -> int:
    sorted_card_frequency = get_card_frequency(hand, new_type)

    first_max_frequency = sorted_card_frequency[0][1]

    if first_max_frequency == 5:
        return HandType.FIVE_OF_A_KIND.value
    if first_max_frequency == 4:
        return HandType.FOUR_OF_A_KIND.value

    second_max_frequency = sorted_card_frequency[1][1]

    if first_max_frequency == 3:
        if second_max_frequency == 2:
            return HandType.FULL_HOUSE.value
        return HandType.THREE_OF_KIND.value
    if first_max_frequency == 2:
        if second_max_frequency == 2:
            return HandType.TWO_PAIR.value
        return HandType.ONE_PAIR.value
    return HandType.HIGH_CARD.value


def compare_two_hands(hand_1: tuple[str, int], hand_2: tuple[str, int]) -> int:
    cards_1 = hand_1[0]
    cards_2 = hand_2[0]

    if get_hand_type(cards_1) < get_hand_type(cards_2):
        return -1
    if get_hand_type(cards_1) > get_hand_type(cards_2):
        return 1

    i = 0

    while i < len(cards_1):
        if CARD_RANK.index(cards_1[i]) < CARD_RANK.index(cards_2[i]):
            return -1
        if CARD_RANK.index(cards_1[i]) > CARD_RANK.index(cards_2[i]):
            return 1
        i += 1

    return 0


def new_compare_two_hands(hand_1: tuple[str, int], hand_2: tuple[str, int]) -> int:
    cards_1 = hand_1[0]
    cards_2 = hand_2[0]

    if get_hand_type(cards_1, True) < get_hand_type(cards_2, True):
        return -1
    if get_hand_type(cards_1, True) > get_hand_type(cards_2, True):
        return 1

    i = 0

    while i < len(cards_1):
        if NEW_CARD_RANK.index(cards_1[i]) < NEW_CARD_RANK.index(cards_2[i]):
            return -1
        if NEW_CARD_RANK.index(cards_1[i]) > NEW_CARD_RANK.index(cards_2[i]):
            return 1
        i += 1

    return 0


def get_hands(data: str) -> list[tuple[str, int]]:
    hands: list[tuple[str, int]] = []

    for row in data:
        hand, bid = row.split(" ")
        hands.append((hand, int(bid)))

    return hands


if __name__ == "__main__":
    filename = "inputs/day_7.txt"
    data = read_file(filename)

    hands = get_hands(data)
    sorted_hands = sorted(hands, key=cmp_to_key(compare_two_hands))

    result_1 = 0

    for i in range(len(sorted_hands)):
        hand = sorted_hands[i]
        bid = hand[1]
        result_1 += (i + 1) * bid

    print(result_1)

    new_sorted_hands = sorted(hands, key=cmp_to_key(new_compare_two_hands))

    result_2 = 0

    for i in range(len(new_sorted_hands)):
        hand = new_sorted_hands[i]
        bid = hand[1]
        result_2 += (i + 1) * bid

    print(result_2)
