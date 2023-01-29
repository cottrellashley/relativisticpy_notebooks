from enum import Enum


class TokenType(Enum):
    NUMBER = 0
    PLUS = 1
    MINUS = 2
    MULTIPLY = 3
    DIVIDE = 4
    VARIABLE = 5
    OPERATOR = 6
    OBJECT = 7
    LPAREN = 8
    RPAREN = 9
    TENSOR = 10
    FLOAT = 11
    INTEGER = 12
    INTEGRAL = 13
    DIFFERENTIAL = 14
    SOLVER = 15
    FUNCTION = 16
    EQUALS = 17
    COMMA = 18
    POW = 19