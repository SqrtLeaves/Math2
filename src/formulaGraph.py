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
        return sorted(result, key=lambda x: [2], reverse=True)


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
    )
])

tgraph = fGraph([
    fNode(
        1,
        "existence of sup/inf",
        [
            (f_implies, 4), is_ordered_set, is_least_upper_bound, is_bounded_below, f_answer, is_inf_exist
        ],
        "Baby/Rudin/TM1.35"
    )
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
