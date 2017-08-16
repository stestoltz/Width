import sys

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
COMMANDS = ("2", "5", "6")
NUMBER = "NUMBER"
STRING = "STRING"
DO = "DO"
IF = "IF"
END = "END"
SEPARATOR = "SEPARATOR"
OUT = "OUT"

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
            return Token(9, OUT)
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
        res = ""
        while self.char is not None and self.char in COMMANDS and len(res) <= 3:
            res += self.char
            self.advance()

        command = 0
        column = 0
        for char in res[::-1]:
            command += COMMANDS.index(char) * 3 ** column
            column += 1

        return Token(command, COMMAND)

source = "".join(filter(lambda c: c in chars, source))

stack = []

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
        elif cmd.type == OUT:
            print(stack.pop())

        cmd = lexer.read()

        """if cmd == 0:
            # Do (code until cmd 1) while ToS is truthy
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
            # If ToS is truthy, Do
        elif cmd == 9:
            # pop and output"""

"""
commands (27 of them):

0 duplicate ToS
1 swap ToS and previous
2 delete ToS
3 input string
4 input number
5 to float
6 to int
7 to string
8 negation
9 not
10 plus
11 mins
12 divide
13 int div
14 times
15 mod
16 concat
17 power
18 root
19 log n
20 bitwise not
21 bitwise or
22 bitwise and
23 factorial
24 index
25 repeat
26 exit
"""