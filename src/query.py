from src.formulaDB import *

def find_relation(src: fID, relation: fTag):
    if relation not in relation_db:
        return
    result = []
    for reGroup in relation_db[relation]:
        if src in reGroup:
            result.append(reGroup)
    return result