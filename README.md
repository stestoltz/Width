# Width
Stack-based esoteric programming language based on character widths

The only valid commands in Width are the letters of the alphabet, uppercase and lowercase. All other characters are stripped out of the source and ignored.

Letters are mapped to numbers based on their width. The following table shows how letters map to numbers.

| # | Letters |
| - | ------- |
| `0` | `i j l` |
| `1` | `f r t I` |
| `2` | `c k s v x y z J` |
| `3` | `a b d e g h n o p q u L` |
| `4` | `F T Z` |
| `5` | `A B E K P S V X Y` |
| `6` | `w C D H N R U` |
| `7` | `G O Q` |
| `8` | `m M` |
| `9` | `W` |

Width is stack-based. It has a main stack, a counter, and a backburner (storage) stack. Each number, as outlined above, is interpreted according to the following rules:

| # | Action | Description |
| - | ------ | ----------- |
| `0` | While | do block while counter > 0 |
| `1` | End | end current block; if not in a block, end program |
| `2` | Command | value of 0 in commands list below |
| `3` | Separator | no-op; mostly used to separate commands |
| `4` | Integer | push base 10 number, using left side row titles (width numbers); terminated with original char |
| `5` | Command | value of 1 in commands list below |
| `6` | Command | value of 2 in commands list below |
| `7` | String | push string literal; sets of 2 width numbers equate to index in printable ASCII string below; terminated with original char |
| `8` | If | if top of stack, do block  |
| `9` | Else | else; if if reaches else before end, do block |

An explanation of some of the actions follows.

# String Literals

The following are the 97 characters that you can use in string literals. String literals are started with value `7`, (letters `GOQ`). They expect sets of two letters, which create base-10 numbers. These base-10 numbers are the index in the below string of the current char. A string literal is terminated with the original char the started it, and then pushed to the stack.

```
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~\n\t
```
 
 where `\n` is a literal newline and `\t` is a literal tab.

For example, the following pushes the string `Hello, World!`:

```
GZiwWOwQROWIkilBAQWmkOCDmifG
```

The string starts with `G`. Each set of two letters in the string maps to a number `00`-`99`, which maps to an index in the above string, as follows:

```
Zi = 40 = H
wW = 69 = e
Ow = 76 = l
QR = 76 = l
OW = 79 = o
Ik = 12 = ,
il = 00 =  
BA = 55 = W
QW = 79 = o
mk = 82 = r
OC = 76 = l
Dm = 68 = d
if = 01 = !
```

#Number Literals

Number literals are formed very similarly to string literals. Note that you cannot push negative literals or float literals, only positive integers - you'll have to use commands (subtraction, negation, and/or division, see below) to form those.

Number literals are started with value `4` (letters `FTZ`). The following letters are read as a base-10 number, where each letter's value is its associated number above. A number literal is terminated with the original char the started it, and then pushed to the stack.

For example, the following pushes `435923785`:

```
FZaXMsoOMAF
```

# Commands

Commands interact with the main stack, with STDIN, with STDOUT, with the counter, and/or with the backburner stack.

Commands are formed using actions `2`, `5`, and `6`. A (hopefully up-to-date) list of commands can be found in `info.txt`. A fully-up-to-date list of commands can be found in the `commands` dict in the interpreter.

In the `info.txt` page and in the `commands` dict, `2` maps to `0`, `5` maps to `1`, and `6` maps to `2`. Think of ternary numbers, but allowing leading `0`s.

Commands are formed by one to four letters in `2`, `5`, or `6` in a row. To separate sequential commands, use the no-op, `3`.
