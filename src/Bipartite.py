from enum import Enum
from typing import Set, Tuple, Any


class VGroup(Enum):
    A = "A"
    B = "B"


class Vertex:
    def __init__(self, id_, group_):
        self.id: int = id_
        self.group: VGroup = group_
        self.outEdge = set()


class Graph:
    def __init__(self, dim):
        self.dim = dim
        self.GA = {}
        self.GB = {}
        for i in range(self.dim):
            self.GA[i] = Vertex(i, VGroup.A)
            self.GB[i] = Vertex(i, VGroup.B)

    def setDirectedEdge(self, matrix: list[list[int]]):
        assert self.dim == len(matrix)
        assert len(matrix) == len(matrix[0])
        for i in range(self.dim):
            vertexA = self.GA[i]
            for j in range(self.dim):
                vertexB = self.GB[j]
                if matrix[i][j] == 1:
                    vertexA.outEdge.add(vertexB)
                if matrix[i][j] == -1:
                    vertexB.outEdge.add(vertexA)

    def dfs(self, root: Vertex, local_marked: set[Vertex], global_marked: set[Vertex]):
        if root in local_marked:
            return [root]
        local_marked.add(root)
        global_marked.add(root)
        if len(root.outEdge) == 0:
            return None
        else:
            for child in root.outEdge:
                result = self.dfs(child, local_marked, global_marked)
                if result:
                    if len(result) > 1 and result[0] == result[-1]:
                        return result
                    else:
                        return [root] + result
                else:
                    return None

    def findCycle(self) -> list[Vertex] | None:
        global_marked = set()
        for v in self.GA.values():
            if v in global_marked:
                continue
            local_marked = set()
            cycle = self.dfs(v, local_marked, global_marked)
            if cycle:
                return cycle
        return None


"""
Input a graph as an adjacency matrix
Output a match as as adjacency matrix
"""


def bipartiteMatching(matrix: list[list[int]]) -> set[tuple[int | Any, ...]]:
    assert len(matrix) == len(matrix[0])
    dim = len(matrix)
    graph = Graph(dim)
    graph.setDirectedEdge(matrix)
    GA = graph.GA
    GB = graph.GB

    s = Vertex(-1, VGroup.B)
    t = Vertex(-1, VGroup.A)

    for i in range(dim):
        s.outEdge.add(GA[i])
        GB[i].outEdge.add(t)

    while 1:

        # for va in GA.values():
        #     va_in_s = (va in s.outEdge)
        #     vb_to_va = False
        #     for vb in GB.values():
        #         if va in vb.outEdge:
        #             vb_to_va = True
        #     assert not (va_in_s and vb_to_va)

        # cycle = graph.findCycle()
        # if cycle:
        #     print([(v.group, v.id) for v in cycle])

        augmentPath = findPath(s, t)
        if len(augmentPath) == 0:
            break
        augmentPath = augmentPath[1:-1]
        s.outEdge.remove(augmentPath[0])
        augmentPath[-1].outEdge.remove(t)

        # path_str = ""
        # for v in augmentPath:
        #     path_str += "{}{} - ".format(v.group, v.id)
        # print(path_str)
        # print("*"*10)

        for i in range(len(augmentPath) - 1):
            head = augmentPath[i]
            tail = augmentPath[i + 1]
            # unmatch -> match
            head.outEdge.remove(tail)
            tail.outEdge.add(head)

    # matching = []
    # for i in range(dim):
    #     matching.append([0] * dim)

    matching = set()

    for vertexB in GB.values():
        for vertexA in vertexB.outEdge:
            if vertexA.id == -1:
                continue
            # print("a{} - b{}".format(vertexA.id, vertexB.id))
            # matching[vertexA.id][vertexB.id] = 1
            matching.add(tuple([vertexA.id, vertexB.id]))
    return matching

def findPath(s: Vertex, t: Vertex) -> list[Vertex]:
    marked = set()
    return findPath_(s, t, marked)

def findPath_(s: Vertex, t: Vertex, marked: set[Vertex]) -> list[Vertex]:
    if s in marked:
        return []
    assert len(t.outEdge) == 0
    # print(s.id,s.group,[v.id for v in s.outEdge], t.id)
    marked.add(s)
    if s == t:
        return [t]
    for child in s.outEdge:
        followingPath = findPath_(child, t, marked)
        if len(followingPath) != 0:
            return [s] + followingPath
    return []



def allAllPerfectMatching_help(matrix: list[list[int]], matching: set[tuple[int | Any, ...]]) -> set[
    tuple[int | Any, ...]] | None:
    assert len(matrix) == len(matrix[0])
    dim = len(matrix)
    graph = Graph(dim)
    GA = graph.GA
    GB = graph.GB
    for i in range(dim):
        for j in range(dim):
            if matrix[i][j] != 1:
                continue
            # match([i,j]) is an undirected edge
            if tuple([i, j]) not in matching:
                GA[i].outEdge.add(GB[j])
            else:
                GB[j].outEdge.add(GA[i])
    cycle = graph.findCycle()
    if not cycle:
        return None
    print([(v.group, v.id) for v in cycle])
    EC = set()
    for i in range(len(cycle) - 1):
        head = cycle[i]
        tail = cycle[i+1]
        if head.group == VGroup.A:
            match = tuple([head.id, tail.id])
        else:
            match = tuple([tail.id, head.id])
        EC.add(match)
    print(len(EC), len(matching))
    return matching.symmetric_difference(EC)

def newMatrix(dim: int):
    matrix = []
    for i in range(dim):
        matrix.append([0] * dim)
    return matrix

def slashGraph(matrix: list[list[int]], edge: tuple[int | Any, ...]):
    assert matrix[edge[0]][edge[1]] == 1
    dim = len(matrix)
    result = newMatrix(dim)
    for i in range(dim):
        for j in range(dim):
            if i == edge[0] or j == edge[1]:
                result[i][j] = 0
            else:
                result[i][j] = matrix[i][j]
    result[edge[0]][edge[1]] = 1
    return result

def backSlashGraph(matrix: list[list[int]], edge: tuple[int | Any, ...]):
    assert matrix[edge[0]][edge[1]] == 1
    dim = len(matrix)
    result = newMatrix(dim)
    for i in range(dim):
        for j in range(dim):
            result[i][j] = matrix[i][j]
    result[edge[0]][edge[1]] = 0
    return result

def allAllPerfectMatching(matrix: list[list[int]]):
    result = []
    M_ = bipartiteMatching(matrix)
    result.append(M_)
    problemQue = [tuple([matrix, M_])]
    while len(problemQue) > 0:
        P1, M1 = problemQue[-1]
        problemQue.pop()
        M2 = allAllPerfectMatching_help(P1, M1)
        if M2 is not None:
            result.append(M2)
            edge = list(M1 - M2)[0]
            problemQue.append(tuple([slashGraph(P1, edge), M1]))
            problemQue.append(tuple([backSlashGraph(P1, edge), M2]))
    return result
