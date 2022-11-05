from src.formulaDB import *
# from src.cmpVarPath import *
# from src.cmpBlock import *
from src.cmpCombo import *
from IPython.display import Latex
from src.query import *
# import json
# expr = open("data/func.json")
# js = json.load(expr)

#
# b1 = Block(test1)
# b2 = Block(test2)

# print(compare_blocks(test1,test2,2))

# for i in range(100):
#     print(i)

ye = {
    f.cos: [{f.add: ["a", "b"]}]
}

for e in search_formula(ye):
    print(e)

Latex(r"$\sqrt{x^2+y^2}$")

for e in find_relation(fID.n1, fTag.equal):
    print(e)

# print(compare_combo(formula_db["test1"], formula_db["test2"]))


# print(get_all_op_path(test2))

# print(compare_var_path(test1, test2))



