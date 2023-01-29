import sympy as smp
from src.RelativisticPy.general_relativity.tensor.tensor_representations import TensorStringRepresentations

class ComputeMathJson:
    def __init__(self, x):
        database = {}
        self.operations = {"Add" : lambda List : ComputeMathJson(List[0])+ComputeMathJson(List[1]),
                           "Mul" : lambda List : ComputeMathJson(List[0])*ComputeMathJson(List[1]),
                           "Sub" : lambda List : ComputeMathJson(List[0])-ComputeMathJson(List[1]),
                           "Div" : lambda List : ComputeMathJson(List[0])/ComputeMathJson(List[1]),
                           "Diff" : lambda List : smp.diff(List[0], List[1]),
                           "Int" : lambda List : smp.integrate(List[0], List[1]),
                           "Eq" : lambda List : database.update({List[0] : ComputeMathJson(List[1]).x}),
                           "integer" : lambda x : int(x),
                           "tensor_string_representation" : lambda x : TensorStringRepresentations(x)}
        
        if isinstance(x, dict):
            if [i for i in x][0] == "Diff":
                self.x = self.operations["Diff"](x["Diff"])
            elif [i for i in x][0] == "Int":
                self.x = self.operations["Int"](x["Int"])
            elif [i for i in x][0] == "integer":
                self.x = self.operations["integer"](x["integer"])
            elif [i for i in x][0] == "tensor_string_representation":
                self.x = self.operations["tensor_string_representation"](x["tensor_string_representation"])
            else:
                self.x = self.operations[[i for i in x][0]](x[[i for i in x][0]])
        else:
            self.x = x
            
            
    def __add__(self, other):
        return self.x + other.x
    
    def __mul__(self, other):
        return self.x*other.x
    
    def __sub__(self, other):
        return self.x-other.x
    
    def __truediv__(self, other):
        return self.x/other.x