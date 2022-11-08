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
            (f_implies, 4), is_ordered_set, is_least_upper_bound, is_bounded, f_answer, is_inf_exist
        ],
        "Baby/Rudin/TM1.35"
    ),
    fNode(
        2,
        "complement of union = intersection of complement",
        [
            (f_implies, 3), is_complement, is_union, (f_answer, 2), is_intersection, is_complement
        ],
        "Bady/Rudin/TM2.22"
    ),
    fNode(
        3,
        "A set E is open iff its complement is closed",
        [
            (f_implies, 2), is_open, (f_answer, 2), is_complement, is_closed
        ],
        "Bady/Rudin/TM2.23"
    ),
    fNode(
        4,
        "A set E is open iff its complement is closed",
        [
            (f_implies, 2), is_closed, (f_answer, 2), is_complement, is_open
        ],
        "Bady/Rudin/TM2.23"
    ),
    fNode(
        5,
        "Union of any collection of open sets is open",
        [
            (f_implies, 2), is_open, (f_answer, 3), is_union, is_open, is_infinite
        ],
        "Bady/Rudin/TM2.24"
    ),
    fNode(
        6,
        "Intersection of any collection of closed sets is closed",
        [
            (f_implies, 2), is_closed, (f_answer, 3), is_intersection, is_closed, is_infinite
        ],
        "Bady/Rudin/TM2.24"
    ),
    fNode(
        7,
        "Intersection of finite collection of open sets is open",
        [
            (f_implies, 2), is_open, (f_answer, 3), is_intersection, is_open, is_finite
        ],
        "Bady/Rudin/TM2.24"
    ),
    fNode(
        8,
        "Union of any collection of closed sets is closed",
        theorem_generator(
            [is_closed],
            [is_union, is_closed, is_finite]
        ),
        "Bady/Rudin/TM2.24"
    ),
    fNode(
        9,
        "closure is closed",
        theorem_generator(
            [is_closure],
            [is_closed]
        ),
        "Bady/Rudin/TM2.27"
    ),
    fNode(
        10,
        "E = closure(E) iff E is closed",
        theorem_generator(
            [f_equal, is_set, is_closure],
            [is_closed]
        ),
        "Bady/Rudin/TM2.27"
    ),
    fNode(
        11,
        "E = closure(E) iff E is closed",
        theorem_generator(
            [is_set, is_closed],
            [f_equal, is_set, is_closure]
        ),
        "Bady/Rudin/TM2.27"
    ),
    fNode(
        12,
        "If F is a closed set, and E is a subset of F, then the closure(E) is a subset of F",
        theorem_generator(
            [is_subset, is_closed],
            [is_subset, is_closure]
        ),
        "Bady/Rudin/TM2.27"
    ),
    fNode(
        13,
        "If y = sup E and if E is closed, then y is in E",
        theorem_generator(
            [(f_and, 2), f_equal, 1, is_sup, is_closed],
            [f_is_in, 1, is_set]
        ),
        "Bady/Rudin/TM2.28"
    ),
    fNode(
        14,
        "Y \subset X; E \subset Y; then E is open relative to Y iff E = Y intersection G for some open open subset G of X",
        theorem_generator(
            [is_subset, is_open_relative_to],
            [f_equal, is_set, (f_and, 2), is_intersection, is_open]
        ),
        "Bady/Rudin/TM2.30"
    ),
    fNode(
        15,
        "E = Y intersection G for some open open subset G of X iff Y \subset X; E \subset Y; then E is open relative to Y ",
        theorem_generator(
            [f_equal, is_set, (f_and, 2), is_intersection, is_open],
            [(f_and, 2), is_subset, is_open_relative_to]
        ),
        "Bady/Rudin/TM2.30"
    ),
    fNode(
        16,
        "Suppose K \subset Y \subset X. Then K is compact relative to X iff K is compact relative to Y",
        theorem_generator(
            [is_subset, is_subset],
            [is_compact_relative_to, is_compact_relative_to]
        ),
        "Bady/Rudin/TM2.33"
    ),
    fNode(
        17,
        "Compact subsets of metric spaces are closed",
        theorem_generator(
            [is_compact, is_metric_space],
            [is_closed]
        ),
        "Bady/Rudin/TM2.34"
    ),
    fNode(
        18,
        "Closed subsets of compact sets are compact",
        theorem_generator(
            [is_closed, is_subset, is_compact],
            [is_compact]
        ),
        "Bady/Rudin/TM2.35"
    ),
    fNode(
        19,
        "If F is closed and K is compact, then F \intersection K is compact",
        theorem_generator(
            [is_closed, is_compact],
            [is_compact, is_intersection]
        ),
        "Bady/Rudin/TM2.35"
    ),
    fNode(
        20,
        "If {K_\alpha} is a collection of compact subsets of a metric space X such that the intersection of every finite subcollection of {K_\alpha} is nonempty, then \intersection K_\alpha is nonempty",
        theorem_generator(
            [6, is_set, is_compact, is_metric_space,
             is_intersection, is_finite, f_not, is_empty],
            [2, is_intersection, f_not, is_empty]
        ),
        "Bady/Rudin/TM2.36"
    ),
    fNode(
        21,
        "If {K_n} is a sequence of nonempty compact sets such that K_n \supset K_{n+1}, then \cap K_n is not empty",
        theorem_generator(
            [4, is_sequence, f_not, is_empty, is_compact, is_subset],
            [2, is_intersection, f_not, is_empty]
        ),
        "Bady/Rudin/TM2.36"
    ),
    fNode(
        22,
        "If E is an infinite subset of a compact set K, then E has a limit point in K",
        theorem_generator(
            [is_infinite, is_subset, is_compact],
            [is_limit_point]
        ),
        "Bady/Rudin/TM2.37"
    ),
    fNode(
        23,
        "If {I_n} is a sequence of intervals in R^1, such that I_n \subset I_{n+1}, then \cap I_n is not empty",
        theorem_generator(
            [3, is_sequence, f_interval, 2, is_subset],
            [2, is_intersection, f_not, is_empty]
        ),
        "Bady/Rudin/TM2.38"
    ),
    fNode(
        24,
        "Let k be a positive integer. If {I_n} is a sequence of k-cells such that I_n \supset I_{n+1}, then \cap I_n is not empty",
        theorem_generator(
            [is_sequence, is_k_cells, is_subset],
            [2, is_intersection, f_not, is_empty]
        ),
        "Bady/Rudin/TM2.39"
    ),
    fNode(
        25,
        "Every k-cell is compact",
        theorem_generator(
            [is_k_cells],
            [is_compact]
        ),
        "Bady/Rudin/TM2.40"
    ),
    fNode(
        26,
        "If E is closed, and bounded then, E is compact and every infinite subsets of E has a limit point in E",
        theorem_generator(
            [is_closed, is_bounded],
            [
                 is_compact,
                 is_infinite, is_limit_point
            ]
        ),
        "Bady/Rudin/TM2.41"
    ),
    fNode(
        27,
        "If E is compact, then E is closed, and every infinite subsets of E has a limit point in E",
        theorem_generator(
            [is_compact],
            [
                 is_closed, is_bounded,
                 is_infinite, is_limit_point
            ]
        ),
        "Bady/Rudin/TM2.41"
    ),
    fNode(
        28,
        "If every infinite subsets of E has a limit point in E; then E is closed,and bounded; and E is compact",
        theorem_generator(
            [is_infinite, is_limit_point],
            [
                is_compact,
                is_closed, is_bounded
            ]
        ),
        "Bady/Rudin/TM2.41"
    ),
    fNode(
        29,
        "Every bounded infinite subset of R^k has a limit point in R^k",
        theorem_generator(
            [is_bounded, is_finite, is_subset, is_R_k],
            [is_limit_point]
        ),
        "Bady/Rudin/TM2.42"
    ),
    fNode(
        30,
        "Let P be a non-empty perfect set in R_k. Then P is uncountable",
        theorem_generator(
            [3, f_not, is_empty, is_perfect_set, is_R_k],
            [1, f_not, is_countable]
        ),
        "Bady/Rudin/TM2.43"
    ),
    fNode(
        31,
        "Every interval [a,b] is uncountable. In particular, the set of all real numbers is uncountable.",
        theorem_generator(
            [2, f_interval, 2, is_R],
            [1, f_not, is_countable]
        ),
        "Bady/Rudin/TM2.43"
    ),
    fNode(
        32,
        "A subset E of the real line R^1 is connected iff it has the following property: if x,y \in E, and x < z < y, then z \in E",
        theorem_generator(
            [is_R, is_connected],
            theorem_generator(
                [4, f_is_in, 2, f_is_in, 2, f_leq, 2, f_leq, 2],
                [1, f_is_in, 2]
            )
        ),
        "Bady/Rudin/TM2.47"
    ),
    fNode(
        33,
        "A subset E of the real line R^1 is connected iff it has the following property: if x,y \in E, and x < z < y, then z \in E",
        theorem_generator(
            theorem_generator(
                [4, f_is_in, 2, f_is_in, 2, f_leq, 2, f_leq, 2],
                [1, f_is_in, 2]
            ),
            [is_R, is_connected]
        ),
        "Bady/Rudin/TM2.47"
    ),
    fNode(
        34,
        "Cantor set is a perfect set which contain no segment",
        theorem_generator(
            [2, is_perfect_set, f_not, is_segment],
            [is_Cantor_set]
        ),
        "Bady/Rudin/TM2.47"
    ),
    fNode(
        35,
        "E and closure(E) have the same limit points",
        theorem_generator(
            [is_set, is_closure],
            [is_limit_point]
        ),
        "Bady/Rudin/EX6"
    ),
    fNode(
        36,
        "Def. of interior point",
        theorem_generator(
            [is_interior_point],
            [is_trivial]
        ),
        "Bady/Rudin/E9"
    ),
    fNode(
        37,
        "If A,B are disjoint closed sets in some metric space X, they are separated",
        theorem_generator(
            [is_disjoint, is_metric_space],
            [1, f_not, is_connected]
        ),
        "Bady/Rudin/E19"
    ),
    fNode(
        38,
        "Every connected metric space with least two points is uncountable",
        theorem_generator(
            [is_connected],
            [1, f_not, is_countable]
        ),
        "Bady/Rudin/E19(d)"
    ),
    fNode(
        39,
        "Let X be a metric space in which every infinite subset has a limit point. Then X is separable",
        theorem_generator(
            [is_metric_space, is_infinite, is_limit_point],
            [is_seperable]
        ),
        "Bady/Rudin/E24"
    ),
    fNode(
        40,
        "Every compact metric space K has a countable base, and K is thus separable",
        theorem_generator(
            [is_compact, is_metric_space, is_countable, is_base],
            [is_seperable]
        ),
        "Bady/Rudin/E25"
    ),
    fNode(
        41,
        "Let X be a metric space in which every infinite subset has a limit point. Then X is compact",
        theorem_generator(
            [is_metric_space, is_infinite, is_limit_point],
            [is_compact]
        ),
        "Bady/Rudin/E26"
    ),
    fNode(
        42,
        "Def. condensation point",
        theorem_generator(
            [2, is_neighborhood, f_not, is_countable],
            [is_condensation_point]
        ),
        "Bady/Rudin/E27"
    ),
    fNode(
        43,
        "Every closed set in a separable metric space is the union of a perfect set and a set which is at most countable",
        theorem_generator(
            [is_closed, is_seperable],
            [is_union, is_perfect_set, is_countable]
        ),
        "Bady/Rudin/E28"
    ),
    fNode(
        44,
        "Every open set in R^1 is the union of an at moust countable collection of disjoint segment",
        theorem_generator(
            [is_R, is_open],
            [is_union, is_countable, is_disjoint, is_segment]
        ),
        "Bady/Rudin/E29"
    ),
    fNode(
        45,
        "If R^k = \cup F_n, where each F_n is a closed subset of R^k, then at least one F_n has a nonempty interior",
        theorem_generator(
            [is_R_k, is_closed],
            [is_interior_point]
        ),
        "Bady/Rudin/E30"
    ),
    fNode(
        46,
        "If G_n is a dense open subset of R^k, then \cap G_n is not empty",
        theorem_generator(
            [is_dense, is_open, is_R_k],
            [2, is_intersection, f_not, is_empty]
        ),
        "Bady/Rudin/E30"
    ),
    # Baby/Rudin/Chap3
    fNode(
        47,
        "If {p_n} is a sequence in a compact metric space3 X, then some subsequence of {p_n} converges to a point of X",
        theorem_generator(
            [is_sequence, is_compact, is_metric_space],
            [is_sequence, is_subsequence, is_converge]
        ),
        "Baby/Rudin/TM3.6(a)"
    ),
    fNode(
        48,
        "Every bounded sequence in R^k contains a convergent subsequence",
        theorem_generator(
            [is_bounded, is_sequence, is_R_k],
            [is_converge, is_sequence]
        ),
        "Baby/Rudin/TM3.6(b)"
    ),
    fNode(
        49,
        "The subsequential limits of a sequence {p_n} in a metric space X form a closed subset of X",
        theorem_generator(
            [is_subsequence, is_limit, is_sequence, is_metric_space],
            [is_closed]
        ),
        "Baby/Rudin/TM3.7"
    ),
    fNode(
        50,
        "If closure(E) is the closure of a set E in a metric space X, then diam closure(E) = diam E",
        theorem_generator(
            [is_closure, is_metric_space],
            [is_diameter, is_closure]
        ),
        "Baby/Rudin/TM3.10(a)"
    ),
    fNode(
        51,
        "If K_n is a sequence of compact sets in X such that K_n \supset K_{n+1}, and if \lim_{n -> \infty} diam K_n = 0, then \intersection_1^\infty K_n consists of exactly one point",
        theorem_generator(
            [is_sequence, is_compact, is_subset, is_limit, is_diameter],
            [is_intersection, is_point]
        ),
        "Baby/Rudin/TM3.10(b)"
    ),
    fNode(
        52,
        "In any metric space X, every convergent sequence is a Cauchy sequence.",
        theorem_generator(
            [is_metric_space, is_converge, is_sequence],
            [is_cauchy_sequence]
        ),
        "Baby/Rudin/TM3.11(a)"
    ),
    fNode(
        53,
        "If X is a compact metric space and if {p_n} is a cauchy sequence in X, then {p_n} converges to some point of X",
        theorem_generator(
            [is_compact, is_metric_space, is_cauchy_sequence],
            [is_converge]
        ),
        "Baby/Rudin/3.11(b)"
    ),
    fNode(
        54,
        "In R^k, every Cauchy sequence converges",
        theorem_generator(
            [is_R_k, is_cauchy_sequence],
            [is_converge]
        ),
        "Baby/Rudin/3.11(c)"
    ),
    fNode(
        55,
        "Suppose {s_n} is monotonic. Then {s_n} converges iff it is bounded",
        theorem_generator(
            [is_sequence, is_monotonical,is_converge],
            [is_bounded]
        ),
        "Baby/Rudin/3.14"
    ),
    fNode(
        56,
        "Suppose {s_n} is monotonic. Then {s_n} converges iff it is bounded",
        theorem_generator(
            [is_sequence, is_monotonical, is_bounded],
            [is_converge]
        ),
        "Baby/Rudin/3.14"
    ),
    fNode(
        57,
        "Let {s_n} be a sequence of real numbers. Let E and s* have the same meaning as in Def 3.16. Then s* has the following two properties. Then s* has the following two properties:",
        theorem_generator(
            [is_sequence, is_R, is_upper_limit],
            [is_subset, is_bounded]
        ),
        "Baby/Rudin/"
    ),
    fNode(
        58,
        "\lim_{n} 1/(n^p) = 0",
        theorem_generator(
            [1, f_geq, 1, c_zero],
            [1, f_equal, (is_limit, 1), f_reverse, f_pow_down, 1, c_zero]
        ),
        "Baby/Rudin/TM3.20(a)"
    ),
    fNode(
        59,
        "If p > 0, then \lim_{n} \sqrtn = 1",
        theorem_generator(
            [1, f_geq, 1, c_zero],
            [1, f_equal, (is_limit, 1), f_sqrtn, 1, c_one]
        ),
        "Baby/Rudin/TM3.20(b)"
    ),
    fNode(
        60,
        "lim_n sqrt[n]n = 1",
        theorem_generator(
            [is_trivial],
            [1, f_equal, (is_limit, 1), f_sqrtn, 1, c_one]
        ),
        "Baby/Rudin/TM3.20(c)"
    ),
    fNode(
        61,
        "lim_n n^a/(1+p)^n",
        theorem_generator(
            [1, f_geq, 1, c_zero],
            [1, f_equal, c_zero, (is_limit, 1), f_times, f_pow_down, 1, f_reverse, f_pow_up, f_add, c_one, 1]
        ),
        "Baby/Rudin/3.20(c)"
    ),
    fNode(
        62,
        "If |x| < 1, then \lim_n x^n = 0",
        theorem_generator(
            [f_leq, f_norm, 1, c_one],
            [f_equal, (is_limit, 1), f_pow_up, 1, c_zero]
        ),
        "Baby/Rudin/3.20(e)"
    ),
    fNode(
        63,
        "A series is converge iff ...",
        theorem_generator(
            [1, (is_converge, 1), f_sum, is_sequence],
            [1, f_leq, f_norm, f_sum, is_sequence, c_epsilon]
        ),
        "Baby/Rudin/3.22"
    ),
    fNode(
        64,
        "If \sum(a_n) converges, then \lim_n a_n = 0",
        theorem_generator(
            [1, (is_converge, 1), f_sum, is_sequence],
            [1, f_equal, (is_limit, 1), is_sequence, c_zero]
        ),
        "Baby/Rudin/3.23"
    ),
    fNode(
        65,
        "A series of nonnegative terms converges iff its partial sums form a bounded sequence",
        theorem_generator(
            [1, (is_converge, 1), f_sum, (is_sequence, 1), f_not, is_positive],
            [is_bounded, is_sequence]
        ),
        "Baby/Rudin/3.24"
    ),
    fNode(
        66,
        "if converge - converge",
        theorem_generator(
            [is_sequence, is_converge],
            [is_sequence, is_converge]
        ),
        "Baby/Rudin/TM3.25(a)"
    ),
    fNode(
        67,
        "If diverge - diver",
        theorem_generator(
            [1, (is_sequence, 1), f_not, is_converge],
            [1, (is_sequence, 1), f_not, is_converge]
        ),
        "Baby/Rudin/TM3.25(b)"
    ),
    fNode(
        68,
        "sum(x^n) = 1/(1-x)",
        theorem_generator(
            [is_trivial],
            [1, f_equal, f_sum, f_pow_down, 1, f_reverse, f_add, c_one, f_minus, 1]
        ),
        "Baby/Rudin/TM3.26"
    ),
    fNode(
        69,
        "convergence test",
        theorem_generator(
            [1] + isc_series,
            [1] + isc_series
        ),
        "Baby/Rudin/3.27"
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
