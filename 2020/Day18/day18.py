#!/usr/bin/python3
from antlr4 import CommonTokenStream, InputStream, ParseTreeWalker
from day18Lexer import day18Lexer
from day18Parser import day18Parser
from day18Visitor import day18Visitor
from day18_2Lexer import day18_2Lexer
from day18_2Parser import day18_2Parser
from day18_2Visitor import day18_2Visitor


class PartOneVisitor(day18Visitor):
    def visitOperation(self, ctx):
        if ctx.op.text == '+':
            return self.visit(ctx.expr()[0]) + self.visit(ctx.expr()[1])
        elif ctx.op.text == '*':
            return self.visit(ctx.expr()[0]) * self.visit(ctx.expr()[1])

    def visitInteger(self, ctx):
        return int(ctx.INT().getText())

    def visitParentheses(self, ctx):
        return self.visit(ctx.expr())

    def visitLine(self, ctx):
        return self.visit(ctx.expr())

    def visitProg(self, ctx):
        return sum(self.visit(l) for l in ctx.line())


class PartTwoVisitor(day18_2Visitor):
    def visitAddition(self, ctx):
        return self.visit(ctx.expr()[0]) + self.visit(ctx.expr()[1])

    def visitMultiplication(self, ctx):
        return self.visit(ctx.expr()[0]) * self.visit(ctx.expr()[1])

    def visitInteger(self, ctx):
        return int(ctx.INT().getText())

    def visitParentheses(self, ctx):
        return self.visit(ctx.expr())

    def visitLine(self, ctx):
        return self.visit(ctx.expr())

    def visitProg(self, ctx):
        return sum(self.visit(l) for l in ctx.line())


def part_one(inp):
    input_stream = InputStream(inp+'\n')
    lexer = day18Lexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = day18Parser(token_stream)
    tree = parser.prog()
    visitor = PartOneVisitor()
    return visitor.visit(tree)


def part_two(inp):
    input_stream = InputStream(inp+'\n')
    lexer = day18_2Lexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = day18_2Parser(token_stream)
    tree = parser.prog()
    visitor = PartTwoVisitor()
    return visitor.visit(tree)


if __name__ == '__main__':
    from argparse import ArgumentParser, FileType

    args = ArgumentParser()
    args.add_argument("input", help='Your input file', type=FileType('r'))
    options = args.parse_args()

    inp = options.input.read().strip()
    print("Answer for part one is : {res}".format(res=part_one(inp)))
    print("Answer for part two is : {res}".format(res=part_two(inp)))
