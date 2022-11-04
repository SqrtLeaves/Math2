from src.cmpBlock import *
from src.cmpVarPath import *
from src.formulaDB import *

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

def search_formula(src: dict):
    scores = []
    for expr_name in formula_db.keys():
        if db_tag in formula_db[expr_name]:
            expr_tag = formula_db[expr_name][db_tag]
        else:
            expr_tag = []
        expr_content = formula_db[expr_name][db_content]
        score = compare_combo(src, expr_content)
        scores.append(tuple([expr_name, expr_tag, score]))
    scores = sorted(scores, key=lambda x:x[2], reverse=True)
    tag2score = {}
    for i in range(len(scores)):
        name, tags, score = scores[i]
        for tag in tags:
            if tag in tag2score:
                scores[i] = tuple([name, tags, tag2score[tag]])
            else:
                tag2score[tag] = score
    scores = sorted(scores, key=lambda x: x[2], reverse=True)
    return scores

