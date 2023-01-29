import sympy as smp
import re
import numpy as np
from GrIndices import GrIndices
from BaseFunctions import BaseFunctions
from DerivativeCalculation import DerivativeCalculation
from GrTensor import GrTensor

class GrDerivative(GrIndices, BaseFunctions):
    def __init__(self, basis, index, metric = None, covariant = False):
        GrIndices.__init__(self, index)
        self.basis = basis
        self.dim = len(basis)
        self.index = index
        self.metric = metric
        self.covariant = covariant
        
    def __mul__(self, TensorObject):
        derivative  = DerivativeCalculation(self.metric, self.basis, TensorObject.components, self.covariant)
        return GrTensor(derivative.return_derivative(self.return_type_of_derivative(TensorObject)), self.sum_indices(GrIndices(TensorObject.indices)))
    
    def return_type_of_derivative(self, TensorObject):
        return str(TensorObject.rank_as_tuple)

    def answerIndex(self, other):
        add = other + self.index
        for i in other:
            for j in self.index:
                if i[0] == j[0] and i[1] != j[1]:
                    add.remove(i)
                    add.remove(j)
                elif i[0] == j[0] and i[1] == j[1]:
                    add.remove(i)
        return add