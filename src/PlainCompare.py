from src.Bipartite import *
from src.func import *


def is_var(e) -> bool:
    return type(e) == str


# class Block2:
#     def __init__(self, src: dict, var: bool = False):
#         self.src = src
#         if var:
#             self.op = f.var
#             return
#         assert len(self.src) == 1
#         self.op = list(self.src.keys())[0]
#         self.elements = []
#         for e in self.src[self.op]:
#             if is_var(e):
#                 self.elements.append(Block2(e, var=True))
#             else:
#                 self.elements.append(Block2(e))

# def add_2_result()

def get_all_op_path(src: dict) -> dict[str]:
    assert len(src) == 1
    result = {}
    op = list(src.keys())[0]
    for e in src[op]:
        if is_var(e):
            if e not in result:
                result[e] = []
            result[e] += [[op]]
        else:
            sub_result = get_all_op_path(e)
            for k in sub_result.keys():
                if k not in result:
                    result[k] = []
                for sub_path in sub_result[k]:
                    new = [op] + sub_path
                    result[k] += [new]
    return result


def compare_2_path(path1: list[f], path2: list[f]):
    if len(path1) != len(path2):
        return False
    dim = len(path1)
    for i in range(dim):
        if path1[i] != path2[i]:
            return False
    return True


def compare_2_expr(src1: dict, src2: dict) -> bool:
    varMap1 = get_all_op_path(src1)
    varMap2 = get_all_op_path(src2)
    if len(varMap1) != len(varMap2):
        return False
    varPathList1 = list(varMap1.values())
    varPathList2 = list(varMap2.values())

    dim = len(varPathList1)

    matrix = newMatrix(dim)

    for i in range(dim):
        for j in range(dim):
            matrix[i][j] = compare_2_path(varPathList1[i], varPathList2[j])

    match = bipartiteMatching(matrix)

    return len(match) == dim
