from src.Basic import *
from src.testExpr import *
# import json
# expr = open("data/func.json")
# js = json.load(expr)


b1 = Block(test1)
b2 = Block(test2)

print(compare_blocks(b1,b2))
