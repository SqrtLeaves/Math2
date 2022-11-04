from src.bipartite import *
from src.func import *


def compare_var_path(src1: dict, src2: dict) -> bool:
    varMap1 = _get_all_op_path(src1)
    varMap2 = _get_all_op_path(src2)
    if len(varMap1) != len(varMap2):
        return False
    varPathList1 = list(varMap1.values())
    varPathList2 = list(varMap2.values())

    dim = len(varPathList1)

    matrix = newMatrix(dim)

    for i in range(dim):
        for j in range(dim):
            matrix[i][j] = _compare_2_path(varPathList1[i], varPathList2[j])

    match = bipartiteMatching(matrix)

    return len(match) == dim

# helper_function
def _is_var(e) -> bool:
    return type(e) == str


def _get_all_op_path(src: dict) -> dict[str]:
    assert len(list(src.keys())) == 1
    result = {}
    op = list(src.keys())[0]
    for e in src[op]:
        if _is_var(e):
            if e not in result:
                result[e] = []
            result[e] += [[op]]
        else:
            assert type(e) == dict
            sub_result = _get_all_op_path(e)
            for k in sub_result.keys():
                if k not in result:
                    result[k] = []
                for sub_path in sub_result[k]:
                    new = [op] + sub_path
                    result[k] += [new]
    return result


def _compare_2_path(path1: list[f], path2: list[f]):
    if len(path1) != len(path2):
        return False
    dim = len(path1)
    for i in range(dim):
        if path1[i] != path2[i]:
            return False
    return True