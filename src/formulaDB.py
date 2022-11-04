from src.func import *

class fTag(Enum):
    cos_1 = 0

db_tag = "tag"
db_content = "content"

formula_db = {}


formula_db["cos(a+b)"] = {
    db_tag: [fTag.cos_1],
    db_content: {f.cos:[{f.add:["a", "b"]}]}
}

formula_db["cos(a)cos(b) - sin(a)sin(b)"] = {
    db_tag: [fTag.cos_1],
    db_content: {
        f.add:[
            {f.times: [{f.cos:"a"},{f.cos:"b"}]},
            {f.minus: [{f.times: [{f.sin:"a"},{f.sin:"b"}]}]}
        ]
    }
}







#
# formula_db["test1"] \
# = {
#     f.add:[
#         "b",
#         {
#             f.times:[
#                 "b", {
#                     f.add: ["a","b"]
#                 }
#             ]
#         },
#         {
#             f.times:[
#                 "b","c"
#             ]
#         }
#     ]
# }
#
# formula_db["test2"] \
# = {
#     f.add:[
#         {
#             f.times: [
#                 "b", {
#                     f.add: ["a",
#                             {f.times:[
#                         "a","b"
#                     ]}]
#                 }
#             ]
#         },
#         {
#             f.times:[
#                 "b","c"
#             ]
#         },
#         "a"
#     ]
# }