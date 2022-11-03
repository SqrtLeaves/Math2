import re


# test = "+(-(+($a,$b),$c),*($d,$e))"
#
# test = "+(-(+($a,$b),&sin($c)),&int($f,$a))"


# psudo code

def checkGraphRelation(es1, es2):
    pass


def bipartiteMatching(truth):
    pass


def internalStructure():
    pass


def compare(ep1, ep2):
    if not ep1.startOP() != ep2.startOP():
        return False
    es1 = ep1.getBlock()
    es2 = ep2.getBlock()

    if len(es1) != len(es2):
        return False

    if ep1.startOP() in ["+", "*"]:
        truth = {}
        for s1 in es1:
            for s2 in es2:
                truth[s1][s2] = compare(s1, s2)
                truth[s2][s1] = truth[s1][s2]
        lst_es = bipartiteMatching(truth)

        pes1 = internalStructure(es1)
        pes2 = internalStructure(es1)
        for matching in lst_es:
            if checkGraphRelation(pes1, pes2, matching):
                return True
        return False
    else:
        for i in range(len(es1)):
            if compare(es1[i],es2[i]) != True:
                return False
        pes1 = internalStructure(es1)
        pes2 = internalStructure(es2)
        return checkGraphRelation(es1, es2)




#
#
# que = []
# stack = [test]
#
# def block_split(s: str):
#     start = 0
#     result = []
#     slack = 0
#     for i in range(len(s)):
#         c = s[i]
#         if c == '(':
#             slack += 1
#         if c == ')':
#             slack -= 1
#         if slack == 0 and c == ',':
#             tail = i
#             result.append(s[start:tail])
#             start = tail + 1
#     result.append(s[start:])
#     return result
#
# asso = ["&add", "&"]
#
# test = "&int(&*(&m($f,$x),&m($g,$x)),$x)"
#
# def parse(src: str):
#     if src[0] == '&':
#         tail = src.find("(")
#         op = src[:tail]
#         content = block_split(src[tail:][1:-1])


# while len(stack) > 0:
#     cur = stack[-1]
#     stack.pop()
#     if cur[0] == '&':
#         tail = cur.find("(")
#         op = cur[:tail]
#         content = block_split(cur[tail:][1:-1])
#         # print(content)
#         que.append(op)
#         stack.append(content[1])
#         stack.append(content[0])
#     else:
#         que.append(cur)
#     while len(que) >= 3 and que[-1] not in ops and que[-2] not in ops:
#         op = que[-3]
#         left = que[-2]
#         right = que[-1]
#         assert op in ops
#         que[-3] = "$x"
#         que = que[:-2]
#
#         if op == "+":
#             add.add(left)
#             add.add(right)
#         elif op == "-":
#             add.add(left)
#             minus.add(right)
# print(add)
# print(minus)


#
#
#
# for i in range(len(test)):
#     c = test[i]
#     que.append(c)
#
#     while len(que) >= 3 and que[-1] not in ops and que[-2] not in ops:
#         op = que[-3]
#         a = que[-2]
#         b = que[-1]
#         assert op in ops
#         que[-3] = "({}{}{})".format(a,op,b)
#         que = que[:-2]
#
#         if op == "+":
#             add.add(a)
#             add.add(b)
#         if op == "-":
#             add.add(a)
#             minus.add(b)
# print(que)
# print(add)
# print(minus)


