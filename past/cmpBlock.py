from src.bipartite import *


class BlockType:
    VAR = 0,
    EXPR = 1


def is_var(e) -> bool:
    return type(e) == str


# 通过结构比较两个expression

class Block:
    def __init__(self, src: [dict | str], var: bool = False):
        self.src = src
        if var:
            self.op = fc.var
            return
        assert len(self.src) == 1
        self.op = list(self.src.keys())[0]
        self.elements = []
        for e in self.src[self.op]:
            if is_var(e):
                self.elements.append(Block(e, var=True))
            else:
                self.elements.append(Block(e))


def compare_blocks(src1: dict, src2: dict, depth: float = float('inf')):
    b1 = Block(src1)
    b2 = Block(src2)
    return _compare_blocks(b1, b2, depth)


def _compare_blocks(b1: Block, b2: Block, depth: float = float('inf')):
    if b1.op != b2.op:
        return False
    if depth == 0:
        return True
    if b1.op == fc.var:
        return True
    if len(b1.elements) != len(b2.elements):
        return False
    dim = len(b1.elements)
    matrix = newMatrix(dim)
    for i in range(dim):
        e1 = b1.elements[i]
        for j in range(dim):
            e2 = b2.elements[j]
            if _compare_blocks(e1, e2, depth - 1):
                matrix[i][j] = 1
    matching = allAllPerfectMatching(matrix)
    if len(matching) == 0 or len(matching[0]) < dim:
        return False
    return True
