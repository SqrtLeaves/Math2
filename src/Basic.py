from Func import *

class BlockType:
    VAR = 0,
    EXPR = 1


class Block:

    def __init__(self, source_: str):
        self.source = source_
        if self.source[0] == '$':
            self.type = BlockType.VAR
            return
        self.type = BlockType.EXPR
        self.func, self.content = self.extractFunc()

        sub_block = []
        for sub_src in self.content:
            sub_block.append(Block(sub_src))

    def standard_form(self):
        print("WIP")

    def extractFunc(self):

        tail = self.source.find('(')
        func = self.source[:tail]
        assert func in FUNCS
        content = self.source[tail:]

        assert content[0] == '('
        assert content[-1] == ')'

        content = content[1:-1].split(",")
        assert len(content) == FUNCS[func]

        return func, content


