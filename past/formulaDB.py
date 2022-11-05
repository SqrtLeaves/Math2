from past.func import *


class fTag(Enum):
    equal = "equal",
    inequal = "inequal"


db_tag = "tag"
db_content = "content"


class fid(Enum):
    n1 = "cos(a+b)",
    n2 = "cos(a)cos(b) - sin(a)sin(b)",
    n3 = "|a+b|",
    n4 = "|a| + |b|"
    n5 = "|x-y| + |y-z|"
    n6 = "|x - y|"
    n7 = "｜sum(ab)｜^2"


def add2Dict(table: dict[fTag], k: fTag | list[fTag], v: tuple):
    if type(k) == list:
        for k_ in k:
            add2Dict(table, k_, v)
        return
    if k not in table:
        table[k] = []
    table[k].append(v)


formula_db = {}

relation_db = {}

relation_db[fTag.equal] = [
    {fid.n1, fid.n2},
]

relation_db[fTag.inequal] = [
    {fid.n3, fid.n4}, # Baby_Rudin_TM1.37
    {fid.n5, fid.n6} # Baby_Rudin_TM1.37
]

# n7
# formula_db[fid.n7] = {
#     db_content: {
#         bd1(fc.)
#     }
# }

# n6
# formula_db[fid.n6] = {
#     db_content: {
#         fc.norm: [
#             "x", {fc.minus: ["y"]}
#         ]
#     }
# }
#
# # n5
# formula_db[fid.n5] = {
#     db_content: {
#         fc.add:[formula_db[fid.n6][db_content], formula_db[fid.n6][db_content]]
#     }
# }
# # formula_db[fid.n5] = {
# #     db_content: {
# #         fc.add:[{fc.norm: [
# #             {fc.add: ["x", {fc.minus: ["y"]}]}
# #         ]},
# #        {fc.norm: [{
# #            fc.add: ["y", {fc.minus: ["z"]}]
# #        }]}]
# #     }
# # }
#
# # n4
# formula_db[fid.n4] = {
#     db_content: {
#         fc.add: [{fc.norm: ["a"]}, {fc.norm: ["b"]}]
#     }
# }
#
# # n3
# formula_db[fid.n3] = {
#     db_content: {
#         fc.norm: [{fc.add: ["a", "b"]}]
#     }
# }
#
# # n2
# formula_db[fid.n2] = {
#     db_content: {
#         fc.add: [
#             {fc.times: [{fc.cos: "a"}, {fc.cos: "b"}]},
#             {fc.minus: [{fc.times: [{fc.sin: "a"}, {fc.sin: "b"}]}]}
#         ]
#     }
# }
#
# # n1
# formula_db[fid.n1] = {
#     db_content: {fc.cos: [{fc.add: ["a", "b"]}]}
# }

# check
total_group = set()
for reGroup in relation_db[fTag.equal]:
    assert len(reGroup.intersection(total_group)) == 0
