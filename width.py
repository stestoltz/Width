import sys
import math

try:
    file = sys.argv[1]
except IndexError:
    file = "source.wide"

with open(file) as f:
    source = f.read()

info = """\
0: i j l
1: f r t I
2: c k s v x y z J
3: a b d e g h n o p q u L
4: F T Z
5: A B E K P S V X Y
6: w C D H N R U
7: G O Q
8: m M
9: W\
"""

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
        elif command == 3 or command == 9:
            self.advance()
            return Token(3, SEPARATOR)
        elif command == 4:
            return self.read_num()
        elif command == 7:
            return self.read_str()
        elif command == 8:
            self.advance()
            return Token(8, IF)
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
backburner = None
counter = None


def set_counter(val):
    global counter
    counter = val

    if counter < 0:
        counter = 0


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

commands = {
    "0": lambda: stack.append(stack[-1]),
    "1": lambda: stack.append(stack.pop(-2)),
    "2": lambda: stack.pop(),
    "00": lambda: set_counter(stack[-1]),
    "01": lambda: stack.append(len(stack)),
    "02": lambda: stack.append(input()),
    "10": lambda: num_input(),
    "11": lambda: stack.append(str(stack.pop())),
    "12": lambda: stack.append(int(stack.pop())),
    "20": lambda: set_counter(counter + 1),
    "21": lambda: set_counter(counter - 1),
    "22": lambda: print(stack.pop()),
    "000": lambda: stack.append(float(stack.pop())),
    "001": lambda: stack.append(-stack.pop()),
    "002": lambda: stack.append(not stack.pop()),
    "010": lambda: stack.append(stack.pop() + stack.pop()),
    "011": lambda: stack.append(stack.pop() - stack.pop()),
    "012": lambda: stack.append(stack.pop() / stack.pop()),
    "020": lambda: stack.append(stack.pop() // stack.pop()),
    "021": lambda: stack.append(stack.pop() * stack.pop()),
    "022": lambda: stack.append(stack.pop() % stack.pop()),
    "100": lambda: stack.append(math.factorial(stack.pop())),
    "101": lambda: stack.append(str(stack.pop()) + str(stack.pop())),
    "102": lambda: stack.append(math.pow(stack.pop(), stack.pop())),
    "110": lambda: stack.append(math.sqrt(stack.pop())),
    "111": lambda: stack.append(math.log(stack.pop(), stack.pop())),
    "112": lambda: stack.append(~stack.pop()),
    "120": lambda: stack.append(stack.pop() | stack.pop()),
    "121": lambda: stack.append(stack.pop() & stack.pop()),
    "122": lambda: stack.append(stack.pop() << stack.pop()),
    "200": lambda: stack.append(stack.pop() >> stack.pop()),
    "201": lambda: stack.append(stack.pop()[stack.pop()]),
    "202": lambda: stack.append(str(stack.pop()) * stack.pop()),
    "210": lambda: stack.append(counter),
    "211": lambda: set_counter(stack.pop()),
    "212": lambda: stack.extend(list(str(stack.pop()))),
    "220": lambda: flip_ends(),
    "221": lambda: print(stack[-1]),
    "222": lambda: sys.exit(stack[-1]),
    "0000": 0,
    "0001": 0,
    "0002": 0,
    "0010": 0,
    "0011": 0,
    "0012": 0,
    "0020": 0,
    "0021": 0,
    "0022": 0,
    "0100": 0,
    "0101": 0,
    "0102": 0,
    "0110": 0,
    "0111": 0,
    "0112": 0,
    "0120": 0,
    "0121": 0,
    "0122": 0,
    "0200": 0,
    "0201": 0,
    "0202": 0,
    "0210": 0,
    "0211": 0,
    "0212": 0,
    "0220": 0,
    "0221": 0,
    "0222": 0,
    "1000": 0,
    "1001": 0,
    "1002": 0,
    "1010": 0,
    "1011": 0,
    "1012": 0,
    "1020": 0,
    "1021": 0,
    "1022": 0,
    "1100": 0,
    "1101": 0,
    "1102": 0,
    "1110": 0,
    "1111": 0,
    "1112": 0,
    "1120": 0,
    "1121": 0,
    "1122": 0,
    "1200": 0,
    "1201": 0,
    "1202": 0,
    "1210": 0,
    "1211": 0,
    "1212": 0,
    "1220": 0,
    "1221": 0,
    "1222": 0,
    "2000": 0,
    "2001": 0,
    "2002": 0,
    "2010": 0,
    "2011": 0,
    "2012": 0,
    "2020": 0,
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
    "2221": 0,
    "2222": 0
}


def run_cmd(name):
    global stack, counter, backburner

    state = {
        "stack": stack,
        "counter": counter,
        "backburner": backburner
    }

    try:
        commands[name]()
    except IndexError:
        stack = state[stack]
        counter = state[counter]
        backburner = state[backburner]

if source == "":
    print(info)
else:
    lexer = Lexer(source)

    cmd = lexer.read()
    while cmd is not None:

        if cmd.type == DO:
            pass
        elif cmd.type == END:
            pass
        elif cmd.type == SEPARATOR:
            pass
        elif cmd.type == NUMBER:
            stack.append(cmd.val)
        elif cmd.type == STRING:
            stack.append(cmd.val)
        elif cmd.type == IF:
            pass
        elif cmd.type == COMMAND:
            run_cmd(cmd.val)

        cmd = lexer.read()

    try:
        sys.exit(stack[-1])
    except IndexError:
        pass

    """if cmd == 0:
        # Do (code until end) counter > 0
    elif cmd == 1:
        # End Do
    elif cmd == 2:
        # commands
    elif cmd == 3:
        # command separator
    elif cmd == 4:
        # push base 10 number, but with width numbers; terminated with original char
    elif cmd == 5:
        # commands
    elif cmd == 6:
        # commands
    elif cmd == 7:
        # push string literal; sets of 2 width numbers equate to index in printable ASCII; terminated with original char
    elif cmd == 8:
        # If counter > 0, Do; optional else with another cmd 8, Do; End
    elif cmd == 9:
        # command separator """

"""
0 duplicate ToS
1 swap ToS and previous
2 delete ToS

00 set counter to read ToS
01 push height of stack
02 input string
10 input number
11 to string
12 to int
20 inc counter
21 dec counter
22 output

000 to float
001 negation
002 not
010 plus
011 minus
012 divide
020 int div
021 times
022 mod
100 factorial
101 concat
102 power
110 root
111 log n
112 bitwise not
120 bitwise or
121 bitwise and
122 left shift
200 right shift
201 index
202 repeat
210 push counter
211 set counter to pop ToS
212 split ToS by ""
220 swap ToS and bottom
221 read and output
222 exit

0000 reverse stack
0001 sort stack
0002 swap bottom and top
0010 
0011 
0012 
0020 sum of numbers in stack
0021 product of numbers in stack
0022 
0100 pop stack to backburner
0101 push stack from backburner to top of stack
0102 push stack from backburner to bottom of stack
0110 pop ToS to backburner
0111 pop ToS to backburner split on ""
0112 pop ToS to backburner split on y
0120 
0121 
0122 
0200 join stack on ToS
0201 join stack on ""
0202 join y deep into stack on ToS
0210 join ToS deep into stack on ""
0211 
0212
0220 split ToS by y
0221 split ToS by ", "
0222
1000 is prime
1001 is fib
1002
1010
1011
1012
1020
1021
1022
1100
1101
1102
1110
1111
1112
1120
1121
1122
1200 set counter to read ToS
1201
1202
1210
1211
1212
1220
1221
1222
2000 floor
2001 ceil
2002 round
2010 length
2011
2012
2020
2021
2022
2100
2101
2102
2110
2111
2112
2120
2121
2122
2200
2201
2202
2210
2211
2212
2220
2221
2222 error
"""