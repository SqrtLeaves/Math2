from src.cmpTree import *
from src.functions import *
from src.formulaGraph import *
# test = [
#     f_add, f_minus, f_norm, 1, f_norm, 1
# ]
#
#
# for e in fgraph.search(test):
#     print(e)

print()


test2 = theorem_query(
    [is_R_k],
    []
)


for e in tgraph.search(test2):
    print(e)