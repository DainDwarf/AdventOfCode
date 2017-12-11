#!/usr/bin/python3
from __future__ import print_function
from myjsonListener import myjsonListener
from myjsonLexer import myjsonLexer
from myjsonParser import myjsonParser
import antlr4

def antlrStr(tok):
    """Transform antlr token/expression into manipulable lower string."""
    return tok.getText().encode('utf-8').lower()

def getTree(s):
    """Returns antlr4's parse tree for input."""
    stream = antlr4.InputStream(s)
    lexer = myjsonLexer(stream)
    tokens = antlr4.CommonTokenStream(lexer)
    parser = myjsonParser(tokens)
    return parser.elem()

class NumCounter(myjsonListener):
    def __init__(self):
        self.count = 0

    def exitNum(self, ctx:myjsonParser.NumContext):
        self.count += int(antlrStr(ctx.NUMBER()))

    def getCount(self):
        return self.count

class NoRedCounter(myjsonListener):
    def __init__(self):
        self.count = 0

    def exitNum(self, ctx:myjsonParser.NumContext):
        enclosing_ctx = ctx
        while hasattr(enclosing_ctx, 'parentCtx'):
            if hasattr(enclosing_ctx, 'red'):
                if enclosing_ctx.red:
                    return
            enclosing_ctx = enclosing_ctx.parentCtx

        self.count += int(antlrStr(ctx.NUMBER()))

    def getCount(self):
        return self.count

class RedPainter(myjsonListener):
    def exitObj_param(self, ctx:myjsonParser.Obj_paramContext):
        if antlrStr(ctx.elem()) == b'"red"':
            ctx.parentCtx.red = True

# That's handy, the Advent of Code gives unittests.
def UnitTest():
    ex1 = '[1,2,3]'
    ex2 = '{"a":2,"b":4}'
    ex3 = '[[[3]]]'
    ex4 = '{"a":{"b":4},"c":-1}'
    ex5 = '{"a":[-1,1]}'
    ex6 = '[-1,{"a":1}]'
    ex7 = '[]'
    ex8 = '{}'

    print("Unit test for Part One.")
    print("Test {inp} gives {res}".format(inp=ex1, res=partOne(ex1)))
    print("Test {inp} gives {res}".format(inp=ex2, res=partOne(ex2)))
    print("Test {inp} gives {res}".format(inp=ex3, res=partOne(ex3)))
    print("Test {inp} gives {res}".format(inp=ex4, res=partOne(ex4)))
    print("Test {inp} gives {res}".format(inp=ex5, res=partOne(ex5)))
    print("Test {inp} gives {res}".format(inp=ex6, res=partOne(ex6)))
    print("Test {inp} gives {res}".format(inp=ex7, res=partOne(ex7)))
    print("Test {inp} gives {res}".format(inp=ex8, res=partOne(ex8)))


    ex11 = '[1,2,3]'
    ex12 = '[1,{"c":"red","b":2},3]'
    ex13 = '{"d":"red","e":[1,2,3,4],"f":5}'
    ex14 = '[1,"red",5]'

    print("")
    print("Unit test for Part Two.")
    print("Test {inp} gives {res}".format(inp=ex11, res=partTwo(ex11)))
    print("Test {inp} gives {res}".format(inp=ex12, res=partTwo(ex12)))
    print("Test {inp} gives {res}".format(inp=ex13, res=partTwo(ex13)))
    print("Test {inp} gives {res}".format(inp=ex14, res=partTwo(ex14)))


def partOne(inp):
    parseTree = getTree(inp)
    walker = antlr4.ParseTreeWalker()
    counter = NumCounter()
    walker.walk(counter, parseTree)

    return counter.getCount()

def partTwo(inp):
    parseTree = getTree(inp)
    walker = antlr4.ParseTreeWalker()

    painter = RedPainter()
    walker.walk(painter, parseTree)

    counter = NoRedCounter()
    walker.walk(counter, parseTree)

    return counter.getCount()

if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("-t", "--test", help='Unit tests', action='store_true')
    args.add_argument("-i", "--input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    if options.test:
        UnitTest()
    if options.input:
        inp = options.input.read().strip()
        print("Answer for part one is : {res}".format(res=partOne(inp)))
        print("Answer for part two is : {res}".format(res=partTwo(inp)))
