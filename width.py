import sys
import math
import numbers
import functools

try:
    file = sys.argv[1]
except IndexError:
    file = "source.wide"

with open(file) as f:
    source = f.read()

translation = ("ijl", "frtI", "cksvxyzJ", "abdeghnopquL", "FTZ", "ABEKPSVXY", "wCDHNRU", "GOQ", "mM", "W")
chars = "".join(sorted("".join(translation)))
strings = """ !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~\n\t"""


def trans(letter):
    for each in translation:
        if letter in each:
            return translation.index(each)

COMMAND = "COMMAND"
COMMANDS = (2, 5, 6)
NUMBER = "NUMBER"
STRING = "STRING"
DO = "DO"
IF = "IF"
ELSE = "ELSE"
END = "END"
SEPARATOR = "SEPARATOR"


class Token:
    def __init__(self, val, type_):
        self.val = val
        self.type = type_


class Lexer:
    def __init__(self, src):
        self.src = src
        self.pos = 0
        self.char = self.src[self.pos]

    def read(self):
        if self.char is None:
            return None

        command = trans(self.char)

        if command == 0:
            self.advance()
            return Token(0, DO)
        elif command == 1:
            self.advance()
            return Token(1, END)
        elif command == 3:
            self.advance()
            return Token(3, SEPARATOR)
        elif command == 4:
            return self.read_num()
        elif command == 7:
            return self.read_str()
        elif command == 8:
            self.advance()
            return Token(8, IF)
        elif command == 9:
            self.advance()
            return Token(9, ELSE)
        else:
            return self.read_cmd()

    def advance(self):
        self.pos += 1

        try:
            self.char = self.src[self.pos]
        except IndexError:
            self.char = None

    def read_num(self):
        delim = self.char
        self.advance()

        res = ""
        while self.char is not None and self.char != delim:
            res += str(trans(self.char))
            self.advance()

        self.advance()

        return Token(int(res), NUMBER)

    def read_str(self):
        def read_char():
            res_ = str(trans(self.char))
            self.advance()
            res_ += str(trans(self.char))
            self.advance()
            try:
                return strings[int(res_)]
            except IndexError:
                return " "

        delim = self.char
        self.advance()

        res = ""
        while self.char is not None and self.char != delim:
            res += read_char()

        self.advance()

        return Token(res, STRING)

    def read_cmd(self):
        command = ""
        while self.char is not None and trans(self.char) in COMMANDS and len(command) <= 4:
            command += str(COMMANDS.index(trans(self.char)))
            self.advance()

        return Token(command, COMMAND)

source = "".join(filter(lambda c: c in chars, source))

stack = []
backburner = []
counter = 0


def set_counter(val):
    global counter
    counter = int(val)

    if counter < 0:
        counter = 0


def set_stack(val):
    global stack
    stack = val


def num_input():
    inp = input()
    try:
        stack.append(int(inp))
    except ValueError:
        try:
            stack.append(float(inp))
        except ValueError:
            pass


def flip_ends():
    if len(stack) > 1:
        stack[0], stack[-1] = stack[-1], stack[0]


def clear_stack():
    global stack
    stack = []


def reload_stack(is_top):
    global backburner, stack

    if is_top:
        stack.extend(backburner)
    else:
        stack = backburner + stack

    backburner = []


# https://stackoverflow.com/a/15285588/7605753
def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False
    r = int(math.sqrt(n))
    _f = 5
    while _f <= r:
        if n % _f == 0:
            return False
        if n % (_f + 2) == 0:
            return False
        _f += 6
    return True


def error():
    raise Exception

commands = {
    "0": lambda: stack.append(stack[-1]),
    "1": lambda: stack.append(stack.pop(-2)),
    "2": lambda: stack.pop(),
    "00": lambda: set_counter(stack[-1]),
    "01": lambda: stack.append(len(stack)),
    "02": lambda: stack.append(input()),
    "10": num_input,
    "11": lambda: stack.append(str(stack.pop())),
    "12": lambda: stack.append(int(stack.pop())),
    "20": lambda: set_counter(counter + 1),
    "21": lambda: set_counter(counter - 1),
    "22": lambda: print(stack.pop()),
    "000": lambda: stack.append(float(stack.pop())),
    "001": lambda: stack.append(-stack.pop()),
    "002": lambda: stack.append(not stack.pop()),
    "010": lambda: stack.append(stack.pop(-2) + stack.pop()),
    "011": lambda: stack.append(stack.pop(-2) - stack.pop()),
    "012": lambda: stack.append(stack.pop(-2) / stack.pop()),
    "020": lambda: stack.append(stack.pop(-2) // stack.pop()),
    "021": lambda: stack.append(stack.pop(-2) * stack.pop()),
    "022": lambda: stack.append(stack.pop(-2) % stack.pop()),
    "100": lambda: stack.append(math.factorial(stack.pop())),
    "101": lambda: stack.append(str(stack.pop(-2)) + str(stack.pop())),
    "102": lambda: stack.append(math.pow(stack.pop(-2), stack.pop())),
    "110": lambda: stack.append(math.sqrt(stack.pop())),
    "111": lambda: stack.append(math.log(stack.pop(-2), stack.pop())),
    "112": lambda: stack.append(~stack.pop()),
    "120": lambda: stack.append(stack.pop(-2) | stack.pop()),
    "121": lambda: stack.append(stack.pop(-2) & stack.pop()),
    "122": lambda: stack.append(stack.pop(-2) << stack.pop()),
    "200": lambda: stack.append(stack.pop(-2) >> stack.pop()),
    "201": lambda: stack.append(stack.pop(-2)[stack.pop()]),
    "202": lambda: stack.append(str(stack.pop(-2)) * stack.pop()),
    "210": lambda: stack.append(counter),
    "211": lambda: set_counter(stack.pop()),
    "212": lambda: stack.extend(list(str(stack.pop()))),
    "220": flip_ends,
    "221": lambda: stack.append(len(stack[-1])),
    "222": lambda: print(stack[-1]),
    "0000": lambda: stack.reverse(),
    "0001": lambda: stack.sort(),
    "0002": 0,
    "0010": 0,
    "0011": 0,
    "0012": 0,
    "0020": lambda: stack.append(sum(n for n in stack if isinstance(n, numbers.Number))),
    "0021": lambda: stack.append(functools.reduce(lambda x, y: x*y, [n for n in stack if isinstance(n, numbers.Number)], 1)),
    "0022": 0,
    "0100": lambda: (backburner.extend(stack), clear_stack()),
    "0101": lambda: reload_stack(True),
    "0102": lambda: reload_stack(False),
    "0110": lambda: backburner.append(stack.pop()),
    "0111": lambda: backburner.append(list(stack.pop())),
    "0112": lambda: stack.pop().split(stack.pop()),
    "0120": 0,
    "0121": 0,
    "0122": 0,
    "0200": lambda: set_stack([stack.pop().join(stack)]),
    "0201": lambda: set_stack(["".join(stack)]),
    "0202": lambda: (lambda depth=stack.pop(-2): set_stack(stack[-depth:] + [stack.pop().join(stack[:depth])]))(),
    "0210": lambda: (lambda depth=stack.pop(): set_stack(stack[-depth:] + ["".join(stack[:depth])]))(),
    "0211": 0,
    "0212": 0,
    "0220": lambda: stack.append(stack.pop().split(stack.pop())),
    "0221": lambda: stack.append(stack.pop().split(", ")),
    "0222": 0,
    "1000": lambda: stack.append(is_prime(stack[-1])),
    "1001": 0,
    "1002": 0,
    "1010": 0,
    "1011": 0,
    "1012": 0,
    "1020": 0,
    "1021": 0,
    "1022": 0,
    "1100": lambda: stack.append(stack.pop() == stack.pop()),
    "1101": lambda: stack.append(stack.pop() != stack.pop()),
    "1102": lambda: stack.append(stack.pop() > stack.pop()),
    "1110": lambda: stack.append(stack.pop() < stack.pop()),
    "1111": lambda: stack.append(stack.pop() >= stack.pop()),
    "1112": lambda: stack.append(stack.pop() <= stack.pop()),
    "1120": lambda: stack.append(stack.pop() in stack),
    "1121": lambda: stack.append(stack.pop() in backburner),
    "1122": lambda: stack.append(stack.pop() == counter),
    "1200": lambda: set_counter(stack[-1]),
    "1201": 0,
    "1202": 0,
    "1210": 0,
    "1211": 0,
    "1212": 0,
    "1220": 0,
    "1221": 0,
    "1222": 0,
    "2000": lambda: stack.append(math.floor(stack.pop())),
    "2001": lambda: stack.append(math.ceil(stack.pop())),
    "2002": lambda: stack.append(round(stack.pop())),
    "2010": lambda: stack.append(abs(stack.pop())),
    "2011": 0,
    "2012": 0,
    "2020": lambda: stack.append(len(stack.pop())),
    "2021": 0,
    "2022": 0,
    "2100": 0,
    "2101": 0,
    "2102": 0,
    "2110": 0,
    "2111": 0,
    "2112": 0,
    "2120": 0,
    "2121": 0,
    "2122": 0,
    "2200": 0,
    "2201": 0,
    "2202": 0,
    "2210": 0,
    "2211": 0,
    "2212": 0,
    "2220": 0,
    "2221": lambda: print(stack[-1]),
    "2222": lambda: error()
}


def run_cmd(name):
    global stack, counter, backburner

    state = {
        "stack": list(stack),
        "counter": counter,
        "backburner": list(backburner)
    }

    # TODO: unknown command

    try:
        commands[name]()
    except IndexError:
        stack = state["stack"]
        counter = state["counter"]
        backburner = state["backburner"]


class AST:
    pass


class Main(AST):
    def __init__(self):
        self.nodes = []


class Do(AST):
    def __init__(self, node):
        self.node = node


class If(AST):
    def __init__(self, first, second):
        self.first = first
        self.second = second


class Literal(AST):
    def __init__(self, val):
        self.val = val


class Command(AST):
    def __init__(self, val):
        self.val = val


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token = None

    def parse(self):
        pgm = Main()
        self.token = self.lexer.read()

        while self.token is not None and self.token.type != END and self.token.type != ELSE:
            if self.token.type == DO:
                pgm.nodes.append(Do(self.parse()))

            elif self.token.type == NUMBER or self.token.type == STRING:
                pgm.nodes.append(Literal(self.token.val))

            elif self.token.type == IF:
                first = self.parse()

                if self.token.type == ELSE:
                    second = self.parse()
                else:
                    second = None

                pgm.nodes.append(If(first, second))

            elif self.token.type == COMMAND:
                pgm.nodes.append(Command(self.token.val))

            self.token = self.lexer.read()

        return pgm


class Interpreter:
    def __init__(self, tree):
        self.tree = tree

    def visit(self, node):
        method_name = "visit_" + type(node).__name__
        visitor = getattr(self, method_name.lower())
        return visitor(node)

    def interpret(self):
        self.visit(self.tree)

    def visit_main(self, node):
        for each in node.nodes:
            self.visit(each)

    def visit_do(self, node):
        while counter:
            self.visit(node)

    def visit_if(self, node):
        if stack[-1]:
            self.visit(node.first)
        elif node.second:
            self.visit(node.second)

    def visit_literal(self, node):
        stack.append(node.val)

    def visit_command(self, node):
        run_cmd(node.val)


if source == "":
    with open("info.txt") as f:
        info = f.read()

    print(info)
else:
    main = Parser(Lexer(source)).parse()

    interpreter = Interpreter(main)
    interpreter.interpret()

    try:
        sys.exit(stack[-1])
    except IndexError:
        pass
