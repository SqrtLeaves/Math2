from src.formulaDB import *
# from src.cmpVarPath import *
# from src.cmpBlock import *
from src.cmpCombo import *
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
    f.cos: ["x"]
}

for e in search_formula(ye):
    print(e)


# print(compare_combo(formula_db["test1"], formula_db["test2"]))


# print(get_all_op_path(test2))

# print(compare_var_path(test1, test2))



