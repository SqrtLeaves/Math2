from src.bipartite import *
from src.functions import *


class formuNode:
    def __init__(self, fcid_, children: list):
        self.fcid = fcid_
        self.children = children


noneFormuNode = formuNode(f_var, [])


def ft(x):
    if type(x) == tuple:
        f, n = x[0], int(x[1])
    else:
        f = x
        # print(f)
        n = int(x.split("_")[-1])

    return tuple([f, n])


def raw2formal(raw: list):
    result = []
    for f in raw:
        if type(f) == int:
            result += [noneFormuNode] * f
        else:
            e = list(ft(f))
            if e[0] != f_var and e[1] == 0:
                e[1] = 1
                result += [tuple(e), noneFormuNode]
            else:
                result += [tuple(e)]

    return result


def construct_formula_tree(preorder):
    op_stack = []
    num_stack = []
    var_stack = []
    for i in range(len(preorder)):
        if type(preorder[i]) == formuNode:
            op_stack.append(preorder[i])
            var_stack[-1] += 1
            while var_stack[-1] == num_stack[-1]:
                head = -1 * (num_stack[-1] + 1)
                op_stack[head] = formuNode(op_stack[head], op_stack[head + 1:])
                op_stack = op_stack[:head + 1]
                num_stack.pop()
                var_stack.pop()
                if len(var_stack) > 0:
                    var_stack[-1] += 1
                else:
                    break
        else:
            op, num = preorder[i]
            op_stack.append(op)
            num_stack.append(num)
            var_stack.append(0)
    assert len(op_stack) == 1
    return op_stack[0]


def max_continuous_sub_tree(root1: formuNode, root2: formuNode) -> int:
    assert root1.fcid == root2.fcid
    dim1, dim2 = len(root1.children), len(root2.children)
    if max(dim1, dim2) == 0:
        return 1
    if min(dim1, dim2) == 0:
        return 0
    matrix = newMatrix(max(dim1, dim2))
    for i in range(dim1):
        for j in range(dim2):
            if root1.children[i].fcid == root2.children[j].fcid:
                matrix[i][j] = 1
    matchings = allAllPerfectMatching(matrix)
    max_score = 0
    for match in matchings:
        score = 0
        for edge_match in match:
            left = root1.children[edge_match[0]]
            right = root2.children[edge_match[1]]
            # print(edge_match)
            # print(left, right)
            # print(left.fcid, right.fcid)
            score += max_continuous_sub_tree(left, right)
        max_score = max(max_score, score)
    return 1 + max_score


def cmp_tree(f1: list, f2: list):
    f1 = construct_formula_tree(raw2formal(f1))
    f2 = construct_formula_tree(raw2formal(f2))
    return cmp_tree_(f1, f2)


def cmp_tree_(root1: formuNode, root2: formuNode) -> int:
    max_score = 0
    if root1.fcid == root2.fcid:
        max_score = max(max_score, max_continuous_sub_tree(root1, root2))
    for child1 in root1.children + [root1]:
        for child2 in root2.children + [root2]:
            if child1 == root1 and child2 == root2:
                continue
            max_score = max(max_score, cmp_tree_(child1, child2))
    return max_score
