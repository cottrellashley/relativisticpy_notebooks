import sympy as smp
import re
import numpy as np
from GrIndices import GrIndices
from GrTensorArithmetic import GrTensorArithmetic
from GrTensorProduct import GrTensorProduct

class GrTensor(GrIndices):
    def __init__(self, components, indices):
        GrIndices.__init__(self, indices)
        self.components = components
        self.shape = smp.shape(self.components)
        self.dimention = int(self.shape[0])
        self.rank = len(self.shape)
        self.index_instace_list = self.return_index_instances()
        
    def __add__(self, other):
        expression = GrTensorArithmetic(GrTensor(self.components, self.indices),GrTensor(other.components, other.indices))
        return GrTensor(expression.return_tensor("+"),expression.tensor_ans_index_as_string)
    
    def __radd__(self, other):
        expression = GrTensorArithmetic(GrTensor(self.components, self.indices),GrTensor(other.components, other.indices))
        return GrTensor(expression.return_tensor("+"),expression.tensor_ans_index_as_string)
    
    def __mul__(self, other):
        if type(other) == float or type(other) == int:
            return GrTensor(other*self.components,self.indices)
        else:
            expression = GrTensorProduct(GrTensor(self.components, self.indices),GrTensor(other.components, other.indices))
            return GrTensor(expression.return_tensor(),expression.tensor_ans_index_as_string)
        
    def __rmul__(self, other):
        if type(other) == float or type(other) == int:
            return GrTensor(other*self.components,self.indices)
        else:
            expression = GrTensorProduct(GrTensor(self.components, self.indices),GrTensor(other.components, other.indices))
            return GrTensor(expression.return_tensor(),expression.tensor_ans_index_as_string)
    
    def __sub__(self, other):
        expression = GrTensorArithmetic(GrTensor(self.components, self.indices),GrTensor(other.components, other.indices))
        return GrTensor(expression.return_tensor("-"),expression.tensor_ans_index_as_string)
    
    def __truediv__(self, other):
        if type(other) == float or type(other) == int:
            return GrTensor(self.components/other,self.indices)
        else:
            raise ValueError("Cannot divide with anything other than int or float.")
    
    def return_tensor_ans_with_numbers(self, number):
        D = self.dimention
        A = int(self.rank)
        Shape = self.return_tensor_ans_shape()
        return smp.MutableDenseNDimArray(smp.ones(D**A)*number, Shape)