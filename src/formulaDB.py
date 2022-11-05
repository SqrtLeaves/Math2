from src.func import *

class fTag(Enum):
    equal = "equal",
    inequal = "inequal"
    # cos_1 = "cos_1",
    # inequality = "inequality"

db_tag = "tag"
db_content = "content"

class fID(Enum):
    n1 = "cos(a+b)",
    n2 = "cos(a)cos(b) - sin(a)sin(b)",
    n3 = "|a+b|",
    n4 = "|a| + |b|"

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
    {fID.n1, fID.n2},
]

relation_db[fTag.inequal] = [
    {fID.n3, fID.n4},
]

# n4
formula_db[fID.n4] = {
    db_content: {
            f.add: [{f.norm: ["a"]}, {f.norm: ["b"]}]
    }
}

# n3
formula_db[fID.n3] = {
    db_content: {
            f.norm: [{f.add : ["a", "b"]}]
    }
}


# n2
formula_db[fID.n2] = {
    db_content: {
        f.add:[
            {f.times: [{f.cos:"a"},{f.cos:"b"}]},
            {f.minus: [{f.times: [{f.sin:"a"},{f.sin:"b"}]}]}
        ]
    }
}

# n1
formula_db[fID.n1] = {
    db_content: {f.cos:[{f.add:["a", "b"]}]}
}

# check
total_group = set()
for reGroup in relation_db[fTag.equal]:
    assert len(reGroup.intersection(total_group)) == 0
