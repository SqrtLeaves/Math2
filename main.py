from src.cmpTree import *
from src.functions import *
from src.formulaGraph import *
test = [
    f_add, f_minus, f_norm, 1, f_norm, 1
]

test2 = [
    f_implies, is_closed
]

for e in fgraph.search(test):
    print(e)

print()

for e in tgraph.search(test2):
    print(e)