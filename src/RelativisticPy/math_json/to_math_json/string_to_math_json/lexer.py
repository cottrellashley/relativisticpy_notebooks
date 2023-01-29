import re
from src.RelativisticPy.math_json.to_math_json.string_to_math_json.token import Token
from src.RelativisticPy.math_json.to_math_json.string_to_math_json.types import TokenType
from more_itertools import peekable

WHITESPACE         = ' \n\t'
DIGITS             = '0987654321'
LOWERCASES         = 'abcdefghijklmnopqrstuvwxyz'
UPPERCASES         = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
CHARS              = UPPERCASES + LOWERCASES + DIGITS
CHARACTERS         = '{}[]_^=.:'
OBJECT_CHARACTERS  = CHARACTERS + UPPERCASES + LOWERCASES + DIGITS

re_float           = '^(\d+)(\.)(\d+)$'
re_integer         = '^(\d+)$'
regex_integral     = '^(integrate)$'
regex_diff         = '^(diff)$'
regex_solve        = '^(solve)$'
re_variable        = '[a-z]+'

def match_tensors(i):
    string = i
    rank = string.count('_') + string.count('^')
    if rank > 0:
        pattern = lambda x : "([a-zA-Z]+)([_^]\{[a-zA-Z]+\}|[_^]\{[a-zA-Z]+\=[0-9]}){" + str(x) + "}(?=(\*|\)|\+|\-|\/|$))"
        Total = re.match(pattern(rank), string)
        return bool(Total)
    else:
        return False

class Lexer:
    def __init__(self, text):
        self.text = peekable(text)
        self.advance()

    def advance(self):
        try:
            self.current_char = next(self.text)
        except StopIteration:
            self.current_char = None

    def generate_tokens(self):
        while self.current_char != None:
            # If the current character is a empty space or new line, then move on to the next character.
            if self.current_char in WHITESPACE:
                self.advance()
            # If the current character is a . or a digit, then we should keep iterating through while its still a number.
            # When we do not have a .09090 OR 1212.1313 OR 23213 when we stop and returns a number Token, then continue the lexer.
            elif self.current_char == '.' or self.current_char in CHARS:
                yield self.generate_object()
            elif self.current_char == '+':
                self.advance()
                yield Token(TokenType.PLUS, None)
            elif self.current_char == '*':
                yield self.generate_operation()
            elif self.current_char == '-':
                self.advance()
                yield Token(TokenType.MINUS, None)
            elif self.current_char == '/':
                self.advance()
                yield Token(TokenType.DIVIDE, None)
            elif self.current_char == '(':
                self.advance()
                yield Token(TokenType.LPAREN, None)
            elif self.current_char == ')':
                self.advance()
                yield Token(TokenType.RPAREN, None)
            elif self.current_char == '=':
                self.advance()
                yield Token(TokenType.EQUALS, None)
            elif self.current_char == ',':
                self.advance()
                yield Token(TokenType.COMMA, None)
            else:
                raise Exception(f"Illegal Character '{self.current_char}'")

    def generate_operation(self):
        num = ''
        while self.current_char != None and self.current_char == '*':
            num += self.current_char
            self.advance()
        if num.count('*') == 1:
            return Token(TokenType.MULTIPLY, None)
        elif num.count('*') == 2:
            return Token(TokenType.POW, None)
        else:
            raise Exception(f"Illegal Character '{num}'")

    def generate_object(self):
        obj_str = self.current_char
        self.advance()
        while self.current_char != None and self.current_char in OBJECT_CHARACTERS:
            if self.current_char in CHARS and self.text.peek() == '(':
                obj_str += self.current_char
                self.advance()
                if re.match(regex_integral, obj_str):
                    return Token(TokenType.INTEGRAL, obj_str)
                elif re.match(regex_diff, obj_str):
                    return Token(TokenType.DIFFERENTIAL, obj_str)
                elif re.match(regex_solve, obj_str):
                    return Token(TokenType.SOLVER, obj_str)
                else:
                    return Token(TokenType.FUNCTION, obj_str)
            else:
                obj_str += self.current_char
                self.advance()

        if re.match(re_integer, obj_str):
            return Token(TokenType.INTEGER, int(obj_str))

        elif re.match(re_variable, obj_str):
            return Token(TokenType.VARIABLE, obj_str)

        elif re.match(re_float, obj_str):
            return Token(TokenType.FLOAT, float(obj_str))

        elif match_tensors(obj_str):
            return Token(TokenType.TENSOR, obj_str)
