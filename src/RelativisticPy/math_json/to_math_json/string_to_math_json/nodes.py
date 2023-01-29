from dataclasses import dataclass

@dataclass
class PlusNode:

    def __init__(self, node):
        self.node = node
        self.dict = { "POSITIVE" : str(self.node)}

    def __repr__(self):
        return f"(+{self.node})"

@dataclass
class MinusNode:

    def __init__(self, node):
        self.node = node
        self.dict = { "NEGATIVE" : str(self.node)}

    def __repr__(self):
        return f"(-{self.node})"

@dataclass
class TensorNode:
    
    def __init__(self, value):
        self.value = value
        self.dict = { "TENSOR" : str(self.value)}

    def __repr__(self):
        return f"({self.value})"

@dataclass
class VariableNode:

    def __init__(self, value):
        self.value = value
        self.dict = { "VAR" : str(self.value)}

    def __repr__(self):
        return f"{self.value}"

@dataclass
class IntNode:

    def __init__(self, value):
        self.value = value
        self.dict = { "NUMBER_INT" : str(self.value)}

    def __repr__(self):
        return f"({self.value})"

@dataclass
class FloatNode:

    def __init__(self, value):
        self.value = value
        self.dict = { "NUMBER_FLOAT" : str(self.value)}

    def __repr__(self):
        return f"({self.value})"

@dataclass
class AddNode:

    def __init__(self, node_a, node_b):
        self.node_a = node_a
        self.node_b = node_b
        self.dict = { "ADD" : [self.node_a, self.node_b]}


    def __repr__(self):
        return f"({self.node_a} + {self.node_b})"

@dataclass
class SubNode:

    def __init__(self, node_a, node_b):
        self.node_a = node_a
        self.node_b = node_b
        self.dict = { "MINUS" : [self.node_a, self.node_b]}

    def __repr__(self):
        return f"({self.node_a} - {self.node_b})"

@dataclass
class MulNode:

    def __init__(self, node_a, node_b):
        self.node_a = node_a
        self.node_b = node_b
        self.dict= { "MULTIPLY" : [self.node_a, self.node_b]}

    def __repr__(self):
        return f"({self.node_a} * {self.node_b})"

@dataclass
class PowNode:

    def __init__(self, node_a, node_b):
        self.node_a = node_a
        self.node_b = node_b
        self.dict= { "POW" : [self.node_a, self.node_b]}

    def __repr__(self):
        return f"({self.node_a} ^ {self.node_b})"

@dataclass
class DivNode:

    def __init__(self, node_a, node_b):
        self.node_a = node_a
        self.node_b = node_b
        self.dict = { "DIV" : [self.node_a, self.node_b]}

    def __repr__(self):
        return f"({self.node_a} / {self.node_b})"

@dataclass
class IntegrateNode:

    def __init__(self, node_a, node_b):
        self.node_a = node_a
        self.node_b = node_b
        self.dict = { "INT" : [self.node_a, self.node_b]}

    def __repr__(self):
        return f"integrate({self.node_a}, {self.node_b})"

@dataclass
class DifferentialNode:

    def __init__(self, node_a, node_b):
        self.node_a = node_a
        self.node_b = node_b
        self.dict = { "DIFF" : [self.node_a, self.node_b]}

    def __repr__(self):
        return f"differential({self.node_a}, {self.node_b})"

@dataclass
class EqualsNode:

    def __init__(self, node_a, node_b):
        self.node_a = node_a
        self.node_b = node_b
        self.dict = { "EQUALITY" : [self.node_a, self.node_b]}

    def __repr__(self):
        return f"{self.node_a} = {self.node_b}"