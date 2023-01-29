import sympy as smp
import re
import numpy as np
from BaseFunctions import BaseFunctions

class DerivativeCalculation(BaseFunctions):
    def __init__(self, Metric, Basis, TensorObject, covariant = False):
        BaseFunctions.__init__(self, Metric, Basis, len(Basis))
        self.TensorObject = TensorObject
        self.covariant = covariant
    
    def return_derivative(self,rank_tuple):
        derivative = { 
                'normal' : self.TDerivative,
                '(1,1)' : self.CovariantD11,
                '(0,1)' : self.CovariantD01,
                '(1,0)' : self.CovariantD10,
                '(0,2)' : self.CovariantD02,
                '(2,0)' : self.CovariantD20
                }
        if self.covariant:
            return derivative[rank_tuple](self.TensorObject)
        else:
            return derivative['normal'](self.TensorObject)
        