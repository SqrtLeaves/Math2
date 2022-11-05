from src.functions import *
from src.cmpTree import *


class fNode:
    def __init__(self, id, name, content , comment=""):
        self.id = id
        self.name = name
        self.content = content
        self.comment = comment
        self.equality = []
        self.greater = []
        self.less = []


class fGraph:
    def __init__(self, vertexs: list[fNode]):
        self.vertexs = vertexs
        self.table = {}
        for v in vertexs:
            assert v.id not in self.table
            self.table[v.id] = v

    def search(self, formula: list):
        result = []
        for v in self.vertexs:
            result.append(tuple([v.id, v.name, cmp_tree(v.content, formula), v.comment]))
        return sorted(result, key=lambda x: x[2], reverse=True)


fgraph = fGraph([
    fNode(
        1,
        "|a+b| <= |a| + |b|",
        [
            f_leq, f_norm, f_add, 2, f_add, f_norm, 1, f_norm, 1
        ],
    ),
    fNode(
        2,
        "｜sum(ab)｜^2 <= sum(|a|^2) * sum(|b|^2)",
        [
            f_leq, f_square, f_norm, f_sum, f_times, 2, f_times, f_sum, f_square, f_norm, 1, f_sum, f_square, f_norm, 1
        ],
        "Baby/Rudin/TM1.35"
    ),
    fNode(
        3,
        "||x| - |y|| <= |x - y|",
        [
            f_leq, f_norm, f_add, f_norm, 1, f_minus, f_norm, 1, f_norm, f_add, 1, f_minus, 1
        ],
        "Bady/Rudin/E13"
    )
])

def theorem_generator(conditon: list, conlusion:list):
    if not conditon[0].startswith("is_"):
        imply = [(f_implies, 2)]
    else:
        imply = [(f_implies, len(conditon) + 1)]
    if not conlusion[0].startswith("is_"):
        answer = [(f_answer, 1)]
    else:
        answer = [(f_answer, len(conlusion))]
    return imply + conditon + answer + conlusion

tgraph = fGraph([
    fNode(
        1,
        "existence of sup/inf",
        [
            (f_implies, 4), is_ordered_set, is_least_upper_bound, is_bounded_below, f_answer, is_inf_exist
        ],
        "Baby/Rudin/TM1.35"
    ),
    fNode(
        2,
        "complement of union = intersection of complement",
        [
            (f_implies, 3), is_complement, is_union, (f_answer, 2), is_intersection, is_complement
        ],
        "Bady/Rudin/E13/TM2.22"
    ),
    fNode(
        3,
        "A set E is open iff its complement is closed",
        [
            (f_implies, 2), is_open, (f_answer, 2), is_complement, is_closed
        ],
        "Bady/Rudin/E13/TM2.23"
    ),
    fNode(
        4,
        "A set E is open iff its complement is closed",
        [
            (f_implies, 2), is_closed, (f_answer, 2), is_complement, is_open
        ],
        "Bady/Rudin/E13/TM2.23"
    ),
    fNode(
        5,
        "Union of any collection of open sets is open",
        [
            (f_implies, 2), is_open, (f_answer, 3), is_union, is_open, is_infinite
        ],
        "Bady/Rudin/E13/TM2.24"
    ),
    fNode(
        6,
        "Intersection of any collection of closed sets is closed",
        [
            (f_implies, 2), is_closed, (f_answer, 3), is_intersection, is_closed, is_infinite
        ],
        "Bady/Rudin/E13/TM2.24"
    ),
    fNode(
        7,
        "Intersection of finite collection of open sets is open",
        [
            (f_implies, 2), is_open, (f_answer, 3), is_intersection, is_open, is_finite
        ],
        "Bady/Rudin/E13/TM2.24"
    ),
    fNode(
        8,
        "Union of any collection of closed sets is closed",
        theorem_generator(
            [is_closed],
            [is_union, is_closed, is_finite]
        ),
        "Bady/Rudin/E13/TM2.24"
    ),
    fNode(
        9,
        "closure is closed",
        theorem_generator(
            [is_closure],
            [is_closed]
        ),
        "Bady/Rudin/E13/TM2.27"
    ),
    fNode(
        10,
        "E = closure(E) iff E is closed",
        theorem_generator(
            [f_equal, is_set, is_closure],
            [is_closed]
        ),
        "Bady/Rudin/E13/TM2.27"
    ),
    fNode(
        11,
        "E = closure(E) iff E is closed",
        theorem_generator(
            [is_set, is_closed],
            [f_equal, is_set, is_closure]
        ),
        "Bady/Rudin/E13/TM2.27"
    ),


])

# tgraph = fGraph([
#     fNode(
#         1,
#         "existence of sup/inf",
#         [
#             (f_implies, 4), is_ordered_set, 1, is_least_upper_bound, 1, is_bounded_below, 1, f_answer, is_inf_exist, 1
#         ]
#     )
# ])
