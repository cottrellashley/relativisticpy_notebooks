import sympy as smp
import re
import numpy as np
from GrTensor import GrTensor

class BaseTensorExpression(GrTensor):
    def __init__(self, A, B):
        self.A = A
        self.B = B
        self.tensor_a_components = self.A.components
        self.tensor_b_components = self.B.components
        self.tensor_a_shape = self.A.shape
        self.tensor_b_shape = self.B.shape
        self.tensor_a_dimention = self.A.dimention
        self.tensor_a_dimention = self.B.dimention
        self.tensor_a_rank = self.A.rank
        self.tensor_b_rank = self.B.rank
        self.tensor_a_list_of_index_instances = A.index_instace_list
        self.tensor_b_list_of_index_instances = B.index_instace_list
        self.tensor_ans_index_as_string = self.return_resulting_indices_as_string()
        self.tensor_ans_list_of_index_instances = self.return_index_instances()
        self.tensor_ans_rank = len(self.tensor_ans_list_of_index_instances)
        self.tensor_ans_zero_components = self.return_tensor_ans_with_zeros()
        self.tensor_ans_shape = self.return_tensor_ans_shape()
        self.tensor_ans_list_of_index_combinatorics = self.return_tensor_ans_index_combinatorics_as_list()

    def return_index_instances(self):
        instance_list = []
        individual_indices = [item for item in re.split('(?=[_^])', self.tensor_ans_index_as_string) if item]
        for i in range(len(individual_indices)):
            instance_list.append(GrIndex(individual_indices[i],int(i)))
        return instance_list
    
    # Takes two lists of indices and is responsible for working out what the resulting index structure is:
    def return_resulting_indices_as_string(self):
        A_instances = self.tensor_a_list_of_index_instances
        B_instances = self.tensor_b_list_of_index_instances
        Total = A_instances + B_instances
        ListA = list(dict.fromkeys([x.index for x in Total]))
        for i in A_instances:
            for j in B_instances:
                if i == j and i.index[0] != j.index[0]:
                    ListA.remove(i.index)
                    ListA.remove(j.index)
        return ''.join(ListA)
    
    def return_tensor_ans_shape(self):
        D = self.tensor_a_dimention
        N = self.tensor_ans_rank
        Ans_shape = ()
        for i in range(N):
            y = list(Ans_shape)
            y.append(D)
            Ans_shape = tuple(y)
        return Ans_shape
    
    def return_tensor_ans_with_zeros(self):
        D = self.tensor_a_dimention
        A = int(self.tensor_ans_rank)
        Shape = self.return_tensor_ans_shape()
        return smp.MutableDenseNDimArray(smp.zeros(D**A), Shape)
    
    def return_tensor_ans_index_combinatorics_as_list(self):
        D = self.tensor_a_dimention
        Shape = self.return_tensor_ans_shape()
        return list(it.product(np.arange(0, D, 1), repeat = len(Shape)))