from src.cmpBlock import *
from src.cmpVarPath import *


def compare_combo (src1: dict, src2: dict) -> tuple[int | float, ...]:
    block_score = 0
    var_score = 0
    if compare_var_path(src1, src2):
        var_score = 1
    if compare_blocks(src1,src2):
        block_score = float('inf')
    else:
        while compare_blocks(src1,src2,block_score):
            block_score += 1
    return tuple([var_score, block_score])