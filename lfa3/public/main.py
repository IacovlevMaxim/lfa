import re
from typing import List, Dict, Union

TYPE_NONE = 0
INT = 1
FLOAT = 2
ASG = 3
ADD = 4
SUB = 5
DIV = 6
MUL = 7
EQ = 8
GT = 9
LT = 10
NOT = 11
AND = 12
OR = 13
PRINT = 14
INPUT = 15
WHILE = 16
IF = 17
ELSE = 18
PUNCT = 19
L_BRACE = 20
R_BRACE = 21
OPERATION = 22
COND_OP = 23
VALUE = 24
ID = 25

IS_VAR = r'^[a-zA-Z][a-zA-Z0-9_]*'
var_regex = re.compile(IS_VAR)


class Variable:
    def __init__(self, name: str, var_type: int, value: Union[int, float] = 0):
        self.name = name
        self.type = var_type
        self.value = value


class Node:
    def __init__(self, tok_class: int = TYPE_NONE, tok_type: int = TYPE_NONE, value: str = "", line: int = 0):
        self.tok_class = tok_class
        self.tok_type = tok_type
        self.value = value
        self.line = line
        self.next = None


class Stack:
    def __init__(self):
        self.top = None

    def append(self, node: Node) -> bool:
        if not self.top:
            self.top = node
        else:
            node.next = self.top
            self.top = node
        return True

    def print_stack(self):
        current = self.top
        while current:
            print(
                f"Token Class: {current.tok_class}, Token Type: {current.tok_type}, Value: {current.value}, Line: {current.line}")
            current = current.next

def is_integer(s: str) -> bool:
    if not s:
        return False
    if s[0] in '+-':
        s = s[1:]
    return s.isdigit()


def is_float(s: str) -> bool:
    if not s:
        return False
    if s[0] in '+-':
        s = s[1:]
    parts = s.split('.')
    if len(parts) != 2:
        return False
    return parts[0].isdigit() and parts[1].isdigit()


def get_op_type(s: str) -> int:
    op_map = {
        "asg": ASG, "add": ADD, "sub": SUB, "div": DIV, "mul": MUL,
        "eq": EQ, "gt": GT, "lt": LT, "not": NOT, "and": AND,
        "or": OR, "print": PRINT, "input": INPUT
    }
    return op_map.get(s, TYPE_NONE)


def get_cond_op_type(s: str) -> int:
    cond_op_map = {"while": WHILE, "if": IF, "else": ELSE}
    return cond_op_map.get(s, TYPE_NONE)


def tokenize(code: str, stack: Stack, variables: List[Variable], debug: bool = False) -> None:
    curr_type = TYPE_NONE
    var_amount = 0
    line_count = 1
    depth = 0
    skip_append = False
    token = ""

    for i, c in enumerate(code):
        if debug:
            print(f"looking at '{c}' ({ord(c)})")
        if c not in {' ', '\n', '\t'}:
            if debug:
                print(f"skipping '{c}'")
            token += c
            continue

        if not token:
            if debug:
                print("skipping empty token")
            continue

        if c == '\n':
            line_count += 1

        if debug:
            print(f"checking '{token}'")

        curr = Node(line=line_count)
        op_type = get_op_type(token)
        cond_op_type = get_cond_op_type(token)

        if token == "int":
            if curr_type != TYPE_NONE:
                raise ValueError(f"Lexer error: Illegal '{token}' placement during variable definition on line {line_count}")
            if depth > 0:
                raise ValueError(f"Lexer error: Definition of variable in main block on line {line_count}")
            curr_type = INT
            skip_append = True
        elif token == "float":
            if curr_type != TYPE_NONE:
                raise ValueError(f"Lexer error: Illegal '{token}' placement during variable definition on line {line_count}")
            if depth > 0:
                raise ValueError(f"Lexer error: Definition of variable in main block on line {line_count}")
            curr_type = FLOAT
            skip_append = True
        elif token == "{":
            depth += 1
            if depth != 1:
                curr.tok_class = PUNCT
                curr.tok_type = L_BRACE
                curr.value = "{"
            else:
                skip_append = True
        elif token == "}":
            depth -= 1
            if depth < 0:
                raise ValueError(f"Lexer error: Extra right bracket on line {line_count}")
            if depth > 0:
                curr.tok_class = PUNCT
                curr.tok_type = R_BRACE
                curr.value = "}"
            else:
                skip_append = True
        elif op_type != TYPE_NONE:
            if curr_type != TYPE_NONE:
                raise ValueError(f"Lexer error: Illegal operation placement '{token}' during variable definition on line {line_count}")
            curr.tok_class = OPERATION
            curr.tok_type = op_type
            curr.value = token
        elif cond_op_type != TYPE_NONE:
            if curr_type != TYPE_NONE:
                raise ValueError(f"Lexer error: Illegal conditional operation placement '{token}' during variable definition on line {line_count}")
            curr.tok_class = COND_OP
            curr.tok_type = cond_op_type
            curr.value = token
        elif is_integer(token):
            curr.tok_class = VALUE
            curr.tok_type = INT
            curr.value = token
        elif is_float(token):
            curr.tok_class = VALUE
            curr.tok_type = FLOAT
            curr.value = token
        elif var_regex.match(token):
            if depth == 0:
                skip_append = True
            var_type = TYPE_NONE

            for var in variables:
                if var.name == token:
                    var_type = var.type
                    break

            if var_type == TYPE_NONE:
                if var_amount == MAX_VAR_AMOUNT:
                    raise ValueError(f"Lexer error: Reached max amount of variables ({MAX_VAR_AMOUNT})")
                new_var = Variable(token, curr_type)
                variables.append(new_var)
                var_amount += 1
            elif curr_type != TYPE_NONE:
                raise ValueError(f"Lexer error: Redefining variable '{token}' on line {line_count}")

            curr.tok_class = ID
            curr.tok_type = var_type if var_type != TYPE_NONE else curr_type

            if curr.tok_type == TYPE_NONE:
                raise ValueError(f"Lexer error: No type definition for variable '{token}'")

            curr.value = token

            if debug:
                print(f"next char after {token} is: '{code[i]}'")
            if code[i] == '\n':
                curr_type = TYPE_NONE
        else:
            raise ValueError(f"Lexer error: Unexpected token '{token}' on line {line_count}")

        token = ""
        if debug:
            print(f"to append: '{curr.value}'")
        if skip_append:
            skip_append = False
            continue
        if not stack.append(curr):
            raise ValueError(f"Lexer error: failed to append token '{curr.value}'")

    if depth != 0:
        raise ValueError("Lexer error: Not all code blocks are enclosed")


if __name__ == "__main__":
    code = """
    int a
    float b
    {
      asg a 44
      asg b 0.01
      print mul a b
    }
    """
    stack = Stack()
    variables = []
    MAX_VAR_AMOUNT = 100
    tokenize(code, stack, variables, debug=False)
    stack.print_stack()