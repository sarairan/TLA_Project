from phase0.FA_class import DFA
from utils.utils import imageType


def split_into_fourths(image: imageType) -> list[imageType] | None:
    height = len(image)
    width = len(image[0])

    part_height = height // 2
    part_width = width // 2

    part1: imageType = []
    part2: imageType = []
    part3: imageType = []
    part4: imageType = []

    if part_height <= 0 and part_width <= 0:
        return None

    for i in range(height):
        part11 = list[int]()
        part21 = list[int]()
        part31 = list[int]()
        part41 = list[int]()
        for j in range(width):
            if i < part_height and j < part_width:
                part11.append(image[i][j])
            elif i < part_height and j >= part_width:
                part21.append(image[i][j])
            elif i >= part_height and j < part_width:
                part31.append(image[i][j])
            else:
                part41.append(image[i][j])
        if len(part11) >= 1:
            part1.append(part11)
        if len(part21) >= 1:
            part2.append(part21)
        if len(part31) >= 1:
            part3.append(part31)
        if len(part41) >= 1:
            part4.append(part41)

    return [part1, part2, part3, part4]


def convert_into_bit_address(image: imageType, prefix: str = ""):
    res = list[str]()
    if image == None or len(image) == 0:
        return res
    if len(image) == 1 and len(image[0]) == 1:
        return [prefix] if image[0][0] == 1 else res
    parts = split_into_fourths(image)
    for i in range(4):
        res += convert_into_bit_address(parts[i], prefix + str(i))
    return res


def solve(image: imageType) -> 'DFA':
    diction = {}
    dfa = DFA()
    initState = dfa.add_state(0)
    dfa.assign_initial_state(initState)
    dfa.alphabet = ['0', '1', '2', '3']
    i = 0
    j = 0
    diction[initState] = image
    while True:
        k = 0
        parts = split_into_fourths(diction[dfa.get_state_by_id(i)])
        if parts is None:
            if diction[dfa.get_state_by_id(i)][0] == [1]:
                dfa.add_final_state(dfa.get_state_by_id(i))
            for ik in range(4):
                dfa.add_transition(dfa.get_state_by_id(i), dfa.get_state_by_id(i), dfa.alphabet[ik])
        else:
            for part in parts:
                if part in diction.values():
                    keyToState = next((k for k, v in diction.items() if v == part), None)
                    dfa.add_transition(dfa.get_state_by_id(i), keyToState, dfa.alphabet[k])
                else:
                    j += 1
                    newState = dfa.add_state(j)
                    diction[newState] = part
                    dfa.add_transition(dfa.get_state_by_id(i), newState, dfa.alphabet[k])
                k += 1
        if i == j:
            break
        else:
            i += 1
    return dfa


if __name__ == "__main__":
    import utils

    image = [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]

    utils.save_image(image)
    fa = solve(image)
    print(fa.serialize_json())
