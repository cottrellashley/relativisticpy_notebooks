import sympy as smp
import re
import numpy as np
from GrTensor import GrTensor

# 'Metric^{a}^{b}' vs 'Metric_{a}_{b}'
class MetricTensor(GrTensor):
    def __init__(self, components, indices, basis):
        GrTensor.__init__(self, self.__is_valid_components(components, basis), self.__is_valid_indices(indices, basis, components))
        self.basis = basis
        
    def __is_valid_indices(self, indices, basis, components):
        diag_form = smp.MutableDenseNDimArray(smp.diag(*[1 for i in range(len(basis))]))
        list_of_indices = [item for item in re.split('(?=[_^])', indices) if item]
        if int(len(list_of_indices)) == 2:
            if list_of_indices[0][0] != list_of_indices[1][0] and components != diag_form:
                raise ValueError("Invalid metric, the index you have entered must be unitary.")
            else:
                return indices
        else:
            raise ValueError("Your Metric tensor must have two indices.")
            
    def __is_valid_components(self, components, basis):
        if smp.shape(components) == (len(basis), len(basis)):
            return components
        else:
            raise ValueError("Invalid metric component form, please make sure the components you enter are NxN.")