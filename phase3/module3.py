from utils.utils import imageType
from phase0.FA_class import DFA
from phase2.module2 import solve_percentage


def get_best_fa(fa_list: list[DFA], image: imageType) -> int:
    max = -1
    j = -1
    for i in range(len(fa_list)):
        fa = fa_list[i]
        res = solve_percentage(fa, image)
        if res > max:
            max = res
            j = i
    return j


def solve(json_fa_list: list[str], images: list[imageType]) -> list[int]:
    fa_list = list[DFA]()
    for json_fa in json_fa_list:
        fa_list.append(DFA.deserialize_json(json_fa))
    res = list[int]()
    for image in images:
        res.append(get_best_fa(fa_list, image))
    return res


if __name__ == "__main__":
    ...
