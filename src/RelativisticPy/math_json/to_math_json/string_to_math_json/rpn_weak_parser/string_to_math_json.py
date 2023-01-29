import re
from collections import namedtuple
from src.RelativisticPy.math_json.to_math_json.math_json import MathJSON

class StringToMathJson:
    def __init__(self, string):
        self.string = string
        self.OpBehaviour = namedtuple('OpBehaviour', 'priority lmbd')
        self.operations = {"+": self.OpBehaviour(0, lambda x, y: y+x),
                           "-": self.OpBehaviour(0, lambda x, y: y-x),
                           "/": self.OpBehaviour(1, lambda x, y: y/x),
                           "*": self.OpBehaviour(1, lambda x, y: y*x),
                           "^": self.OpBehaviour(2, lambda x, y: y**x)}

    def tokenize(self):
        string = self.string.replace(' ', '')
        return [ i for i in re.split('(\+|\-|\(|\)|\*|\/)', string) if i]

    def match_tensors(self, i):
        string = i
        pattern = lambda x : "([a-zA-Z]+)([_^]\{[a-zA-Z]+\}|[_^]\{[a-zA-Z]+\=[0-9]}){" + str(x) + "}(?=(\*|\)|\+|\-|\/|$))"
        Total = [[x for x in re.finditer(pattern(j), string)] for j in range(1, 11)]
        return [tensor.group() for nested in Total for tensor in nested]

    def match_operators(self, i):
        """
            Make checks as to what the name of the function is:
                - Integrate
                - solve
                - diff
                - subs
                or just declared functions
                - f(x)
                - etc...
            Then, make checks on the names and structure of the parameters.
            And finally parse the object into the relevant sympy object and return it into the MathJSON object.
        """
        Input = i.replace(' ', '')
        Function = '(?<![a-zA-Z])' + '([a-zA-Z]+)' + '(\(([a-z]+\))' + '|' + '\(([a-z]+\,)*[a-z]\))'
        return [x for x in re.finditer(Function, Input)]

    def json_wrapped_token(self):
        tokens = self.tokenize()
        for i in range(len(tokens)):
            if tokens[i] not in ['+','-','/','(',')','*']:
                if bool(self.match_operators(tokens[i])):
                    tokens[i] = MathJSON({"operators" : tokens[i]})
                elif bool(self.match_tensors(tokens[i])):
                    tokens[i] = MathJSON({"tensor_string_representation" : tokens[i]})
                elif bool(re.match('[0-9]+', tokens[i].replace('.','',1))):
                    tokens[i] = MathJSON({"number" : tokens[i]})
        return tokens

    def to_rpn(self):
        tokens = self.json_wrapped_token()
        rpn_tokens = []
        op_stack = []

        for token in tokens:
            # Add number to rpn tokens
            if isinstance(token, MathJSON):
                rpn_tokens.append(token)
            # Add opening bracket to operation stack
            elif token == "(":
                op_stack.append(token)
            # Consumes all operations until matching opening bracket
            elif token == ")":
                while op_stack[-1] != "(":
                    rpn_tokens.append(op_stack.pop())
                op_stack.pop()
            elif token in list(self.operations.keys()):
                try:
                    # Check if we have operations that have higher priority on
                    # the op_stack and add them to rpn_tokens so that they are evaluated first:
                    token_priority = self.operations[token].priority
                    while op_stack[-1] != "(" and self.operations[op_stack[-1]].priority >= token_priority:
                        rpn_tokens.append(op_stack.pop())
                except IndexError:  # op_stack is empty
                    pass
                # Add the current operation to the op_stack:
                op_stack.append(token)

        # Add remaining operations to rpn tokens
        while len(op_stack) != 0:
            rpn_tokens.append(op_stack.pop())

        return rpn_tokens

    def calculate(self):
        rpn_tokens = self.to_rpn()
        val_stack = []

        for token in rpn_tokens:
            if isinstance(token, MathJSON):
                val_stack.append(token)
            elif token in list(self.operations.keys()):
                args = []
                for x in range(self.operations[token].lmbd.__code__.co_argcount):
                    # If this throws an error user didn't give enough args
                    args.append(val_stack.pop())
                result = self.operations[token].lmbd(*args)
                val_stack.append(result)

        # If the value stack is bigger than one we probably made an error with the input
        assert len(val_stack) == 1
        return val_stack[0]