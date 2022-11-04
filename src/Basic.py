from src.func import *
from src.Bipartite import *


class BlockType:
    VAR = 0,
    EXPR = 1


def is_var(e) -> bool:
    return type(e) == str


class Block:
    def __init__(self, src: [dict | str], var: bool = False):
        self.src = src
        if var:
            self.op = f.var
            return
        assert len(self.src) == 1
        self.op = list(self.src.keys())[0]
        self.elements = []
        for e in self.src[self.op]:
            if is_var(e):
                self.elements.append(Block(e, var=True))
            else:
                self.elements.append(Block(e))
    def constructInnerStructure(self):
        pass


def compare_blocks(b1: Block, b2: Block):
    if b1.op != b2.op:
        return False
    if b1.op == f.var:
        return True
    if len(b1.elements) != len(b2.elements):
        return False
    dim = len(b1.elements)
    matrix = newMatrix(dim)
    for i in range(dim):
        e1 = b1.elements[i]
        for j in range(dim):
            e2 = b2.elements[j]
            if compare_blocks(e1, e2):
                matrix[i][j] = 1
    matching = allAllPerfectMatching(matrix)
    if len(matching) == 0 or len(matching[0]) < dim:
        return False
    return True
