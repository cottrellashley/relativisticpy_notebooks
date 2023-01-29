from src.RelativisticPy.math_json.to_math_json.string_to_math_json.nodes import AddNode, DifferentialNode, DivNode, FloatNode, IntNode, IntegrateNode, MinusNode, MulNode, PlusNode, PowNode, SubNode, TensorNode, VariableNode
from src.RelativisticPy.math_json.to_math_json.string_to_math_json.types import TokenType
from more_itertools import peekable

class Parser:
    def __init__(self, tokens):
        self.tokens = peekable(tokens)
        self.advance()

    def raise_error(self, error_message):
        raise Exception(error_message)

    def advance(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def parse(self):
        if self.current_token == None:
            return None
        result = self.expr()
        if self.current_token != None:
            self.raise_error("Syntax Error")
        return result

    def find_variables(self):
        tokens = []
        if self.current_token.type != TokenType.VARIABLE:
            self.raise_error("Syntax Error, expecting a VARIABLE token.")
        tokens.append(self.object())
        while self.current_token != None and self.current_token.type == TokenType.COMMA:
            self.advance()
            if self.current_token.type != TokenType.VARIABLE:
                self.raise_error("Syntax Error, expecting a VARIABLE token.")
            tokens.append(self.object())
        return tokens

    def expr(self):
        """
        The expression function will look for expressions, which itself have the structure and rules we define here.
        Steps:

            1. Look for a term, call it X
            2. Advance ---->
            3. If '+' or '-' 
            4. Advance ---->
            5. Look for another term, call it Y
            6. Create a PlusNode or a MinusNode representing X +/- Y
        """
        # First we assign a self.term() which will call the term functions, whose job it is to look for a term.
        # We store that term object in the result variable.
        # This is important as we first need to look for the term which acts as the X in the expr: X (+|-) Y
        X = self.term()
        # The self.term() will end with a self.advance() and if this method is called it will then see if the next is a plus or minus:
        while self.current_token != None and self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.current_token.type == TokenType.PLUS:
                # If we arrive at a + operator, we first advance to the next token and call the self.term() once again,
                # This new self.term() is now finding the Y in the expr: X (+|-) Y as currently we were in the + token -> advance
                self.advance()
                X = AddNode(X, self.term())
            elif self.current_token.type == TokenType.MINUS:
                self.advance()
                X = SubNode(X, self.term())
        return X

    def term(self):
        # First we assign a self.term() which will call the term functions, whose job it is to look for a term.
        # We store that term object in the result variable.
        # This is important as we first need to look for the term which acts as the X in the expr: X (*|/) Y
        result = self.power()
        # The self.term() will end with a self.advance() and if this method is called it will then see if the next is a plus or minus:
        while self.current_token != None and self.current_token.type in (TokenType.MULTIPLY, TokenType.DIVIDE):
            if self.current_token.type == TokenType.MULTIPLY:
                # If we arrive at a + operator, we first advance to the next token and call the self.term() once again,
                # This new self.term() is now finding the Y in the expr: X (+|-) Y as currently we were in the + token -> advance
                self.advance()
                result = MulNode(result, self.power())
            elif self.current_token.type == TokenType.DIVIDE:
                self.advance()
                result = DivNode(result, self.power())
        return result

    def power(self):
        """
        Grammar:

            power : object ((POW) expr)
        """
        result = self.object()
        # The self.term() will end with a self.advance() and if this method is called it will then see if the next is a plus or minus:
        while self.current_token != None and self.current_token.type == TokenType.POW:
            # If we arrive at a + operator, we first advance to the next token and call the self.term() once again,
            # This new self.term() is now finding the Y in the expr: X (+|-) Y as currently we were in the + token -> advance
            self.advance()
            result = PowNode(result, self.object())
        return result

    def object(self):
        token = self.current_token
        if token.type == TokenType.LPAREN:
            self.advance()
            result = self.expr()
            if self.current_token.type != TokenType.RPAREN:
                self.raise_error("Syntax Error, expecting a LPAREN token.")
            self.advance()
            return result
        elif token.type == TokenType.FLOAT:
            self.advance()
            return FloatNode(token.value)
        elif token.type == TokenType.INTEGER:
            self.advance()
            return IntNode(token.value)
        elif token.type == TokenType.TENSOR:
            self.advance()
            return TensorNode(token.value)
        elif token.type == TokenType.VARIABLE:
            self.advance()
            return VariableNode(token.value)
        elif token.type == TokenType.PLUS:
            self.advance()
            return PlusNode(self.object())
        elif token.type == TokenType.MINUS:
            self.advance()
            return MinusNode(self.object())
        #########################################
        # | BELLOW NEEDS IMPROVEMENT | From here on, there woll be a lot of repeated code, which can be wraped in a single function call.
        #########################################
        elif token.type == TokenType.INTEGRAL:
            self.advance()
            if self.current_token.type != TokenType.LPAREN:
                self.raise_error("Syntax Error, expecting a LPAREN token.")
            self.advance()
            expression_to_integrate = self.expr()
            if self.current_token.type != TokenType.COMMA:
                self.raise_error("Syntax Error, expecting a COMMA token.")
            self.advance()
            wrt_variables = self.find_variables()
            if self.current_token.type != TokenType.RPAREN:
                self.raise_error("Syntax Error, expecting a RPAREN token.")
            self.advance()
            return IntegrateNode(expression_to_integrate, wrt_variables)
        elif token.type == TokenType.DIFFERENTIAL:
            self.advance()
            if self.current_token.type != TokenType.LPAREN:
                self.raise_error("Syntax Error, expecting a LPAREN token.")
            self.advance()
            expression_to_integrate = self.expr()
            if self.current_token.type != TokenType.COMMA:
                self.raise_error("Syntax Error, expecting a COMMA token.")
            self.advance()
            wrt_variables = self.find_variables()
            if self.current_token.type != TokenType.RPAREN:
                self.raise_error("Syntax Error, expecting a RPAREN token.")
            self.advance()
            return DifferentialNode(expression_to_integrate, wrt_variables)
        self.raise_error("Syntax Error")