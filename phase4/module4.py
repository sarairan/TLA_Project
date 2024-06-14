from math import log2
from phase0.FA_class import DFA, State
from phase1.module1 import convert_into_bit_address, split_into_fourths
from phase2.module2 import chack_address
from utils.utils import imageType, imageIndexType


def create_from_bit_address(res: imageType, index: imageIndexType, bit_address: list[str]):
    if index is None or len(index) == 0:
        return
    if len(index) == 1 and len(index[0]) == 1:
        res[index[0][0][0]][index[0][0][1]] = 1 if len(bit_address) > 0 else 0
        return
    part_address = [list[str]() for _ in range(4)]
    for addr in bit_address:
        part_address[int(addr[0])].append(addr[1:])
    parts = split_into_fourths(index)
    for i in range(4):
        create_from_bit_address(res, parts[i], part_address[i])


def solve(json_str: str, resolution: int) -> imageType:
    fa = DFA.deserialize_json(json_str)
    image = [[1 for _ in range(resolution)] for _ in range(resolution)]
    index_image = [[(i, j) for j in range(resolution)] for i in range(resolution)]
    bit_address = convert_into_bit_address(image)
    true_bit_address = list[str]()
    for addr in bit_address:
        if chack_address(addr, fa):
            true_bit_address.append(addr)
    create_from_bit_address(image, index_image, true_bit_address)
    return image


if __name__ == "__main__":
    pic_arr = solve(
        '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
        '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
        '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
        '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
        '"3": "q_4"}}',
        4
    )
    print(pic_arr)
