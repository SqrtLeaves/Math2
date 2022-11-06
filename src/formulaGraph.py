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
        score_index = 2
        if formula[0] == f_implies:
            f1 = formula
            f2 = [f_implies] + [(f_add, 1)] + formula[1:]
            r1, r2 = self._search(f1), self._search(f2)
            for v in r1:
                r1[v][score_index] = max(r1[v][score_index], r2[v][score_index])
            result = r1
        else:
            result = self._search(formula)
        return sorted(list(result.values()), key=lambda x: x[score_index], reverse=True)

    def _search(self, formula: list):
        result = {}
        for v in self.vertexs:
            result[v.id] = [v.id, v.comment, cmp_tree(formula, v.content), v.name] # score_index = 2
        return result

    # def _search(self, formula: list):
    #     result = []
    #     for v in self.vertexs:
    #         result.append(tuple([v.id, v.name, cmp_tree(v.content, formula), v.comment]))
    #     return sorted(result, key=lambda x: x[2], reverse=True)


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

def theorem_query(conditon: list[str | tuple], conlusion:list[str | tuple]):
    if len(conditon) == 0:
        conditon = [is_trivial]
    if len(conlusion) == 0:
        conlusion = [is_trivial]
    return theorem_generator(conditon, conlusion)

def theorem_generator(conditon: list[str | tuple: int], conlusion:list[str | tuple | int]):
    assert type(conditon[0]) in (str, int, tuple)
    assert conditon.count(f_and) == 0
    assert conlusion.count(f_and) == 0
    if type(conditon[0]) == int:
        imply = [(f_implies, conditon[0] + 1)]
        conditon = conditon[1:]
    elif type(conditon[0]) == tuple or not conditon[0].startswith("is_"):
        imply = [(f_implies, 2)]
    else:
        imply = [(f_implies, len(conditon) + 1)]

    if type(conlusion[0]) == int:
        answer = [(f_answer, conlusion[0])]
        conlusion = conlusion[1:]
    elif type(conlusion[0]) == tuple or not conlusion[0].startswith("is_"):
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
    fNode(
        12,
        "If F is a closed set, and E is a subset of F, then the closure(E) is a subset of F",
        theorem_generator(
            [is_subset, is_closed],
            [is_subset, is_closure]
        ),
        "Bady/Rudin/E13/TM2.27"
    ),
    fNode(
        13,
        "If y = sup E and if E is closed, then y is in E",
        theorem_generator(
            [(f_and, 2), f_equal, 1, is_sup, is_closed],
            [f_is_in, 1, is_set]
        ),
        "Bady/Rudin/E13/TM2.28"
    ),
    fNode(
        14,
        "Y \subset X; E \subset Y; then E is open relative to Y iff E = Y intersection G for some open open subset G of X",
        theorem_generator(
            [is_subset, is_open_relative_to],
            [f_equal, is_set, (f_and, 2), is_intersection, is_open]
        ),
        "Bady/Rudin/E13/TM2.30"
    ),
    fNode(
        15,
        "E = Y intersection G for some open open subset G of X iff Y \subset X; E \subset Y; then E is open relative to Y ",
        theorem_generator(
            [f_equal, is_set, (f_and, 2), is_intersection, is_open],
            [(f_and, 2), is_subset, is_open_relative_to]
        ),
        "Bady/Rudin/E13/TM2.30"
    ),
    fNode(
        16,
        "Suppose K \subset Y \subset X. Then K is compact relative to X iff K is compact relative to Y",
        theorem_generator(
            [is_subset, is_subset],
            [is_compact_relative_to, is_compact_relative_to]
        ),
        "Bady/Rudin/E13/TM2.33"
    ),
    fNode(
        17,
        "Compact subsets of metric spaces are closed",
        theorem_generator(
            [is_compact, is_metric_space],
            [is_closed]
        ),
        "Bady/Rudin/E13/TM2.34"
    ),
    fNode(
        18,
        "Closed subsets of compact sets are compact",
        theorem_generator(
            [is_closed, is_subset, is_compact],
            [is_compact]
        ),
        "Bady/Rudin/E13/TM2.35"
    ),
    fNode(
        19,
        "If F is closed and K is compact, then F \intersection K is compact",
        theorem_generator(
            [is_closed, is_compact],
            [is_compact, is_intersection]
        ),
        "Bady/Rudin/E13/TM2.35"
    ),
    fNode(
        20,
        "If {K_\alpha} is a collection of compact subsets of a metric space X such that the intersection of every finite subcollection of {K_\alpha} is nonempty, then \intersection K_\alpha is nonempty",
        theorem_generator(
            [is_set, is_compact, is_metric_space,
             is_intersection, is_finite, is_not_empty],
            [is_intersection, is_not_empty]
        ),
        "Bady/Rudin/E13/TM2.36"
    ),
    fNode(
        21,
        "If {K_n} is a sequence of nonempty compact sets such that K_n \supset K_{n+1}, then \cap K_n is not empty",
        theorem_generator(
            [is_sequence, is_not_empty, is_compact, is_subset],
            [is_intersection, is_not_empty]
        ),
        "Bady/Rudin/E13/TM2.36"
    ),
    fNode(
        22,
        "If E is an infinite subset of a compact set K, then E has a limit point in K",
        theorem_generator(
            [is_infinite, is_subset, is_compact],
            [is_limit_point]
        ),
        "Bady/Rudin/E13/TM2.37"
    ),
    fNode(
        23,
        "If {I_n} is a sequence of intervals in R^1, such that I_n \subset I_{n+1}, then \cap I_n is not empty",
        theorem_generator(
            [3, is_sequence, f_interval, 2, is_subset],
            [is_intersection, is_not_empty]
        ),
        "Bady/Rudin/E13/TM2.38"
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
