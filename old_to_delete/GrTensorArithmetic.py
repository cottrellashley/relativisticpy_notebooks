import sympy as smp
import numpy as np
import re
from BaseTensorExpression import BaseTensorExpression
from GrTensor import GrTensor

class GrTensorArithmetic(BaseTensorExpression):
    
    def __init__(self, A:GrTensor, B:GrTensor):
        BaseTensorExpression.__init__(self, A, B)
        self.list_of_repeated_index_locations_wrt_each_tensor = self.return_list_of_repeated_indices()
        self.list_of_all_tensor_index_concatinated_combinatorials = list(it.product(np.arange(0, self.tensor_a_dimention, 1), repeat = self.tensor_a_rank + self.tensor_b_rank))
        self.list_of_list_of_repeated_index_locations_wrt_both_tensor_indices_concatinanted = [[i[0],i[1] + self.tensor_a_rank] for i in self.list_of_repeated_index_locations_wrt_each_tensor]
        self.flat_list_of_repeated_index_locations_wrt_both_tensor_indices_concatinanted = [item for sublist in self.list_of_list_of_repeated_index_locations_wrt_both_tensor_indices_concatinanted for item in sublist]
        self.flat_list_of_ans_tensor_index_locations_wrt_both_tensor_indices_concatinanted = [i for i in list(np.arange(0, self.tensor_a_rank + self.tensor_b_rank, 1)) if i not in self.flat_list_of_repeated_index_locations_wrt_both_tensor_indices_concatinanted]
        self.flat_list_of_tensor_a_repeated_index_locations_wrt_both_tensor_indices_concatinanted = [i[0] for i in self.list_of_list_of_repeated_index_locations_wrt_both_tensor_indices_concatinanted]
        self.flat_list_of_tensor_b_repeated_index_locations_wrt_both_tensor_indices_concatinanted = [i[1] for i in self.list_of_list_of_repeated_index_locations_wrt_both_tensor_indices_concatinanted]
    
    def return_list_of_repeated_indices(self):
        Same_indices = []
        A_instances = self.tensor_a_list_of_index_instances
        B_instances = self.tensor_b_list_of_index_instances
        Total = A_instances + B_instances
        for i in A_instances:
            for j in B_instances:
                if i == j and i.index[0] == j.index[0]:
                    Same_indices.append([int(i.order), int(j.order)])
        return Same_indices
    
    def return_component(self, AnswerIndex, operation):
        A = self.tensor_a_components
        B = self.tensor_b_components
        IndexCombinatorials = self.list_of_all_tensor_index_concatinated_combinatorials
        index_locations_tensor_a = self.flat_list_of_tensor_a_repeated_index_locations_wrt_both_tensor_indices_concatinanted
        index_locations_tensor_b = self.flat_list_of_tensor_b_repeated_index_locations_wrt_both_tensor_indices_concatinanted
        Rank = self.tensor_a_rank
        if operation == "+":
            return [A[i[:Rank]]+B[i[Rank:]] for i in IndexCombinatorials if itemgetter(*index_locations_tensor_a)(i) == itemgetter(*index_locations_tensor_b)(i) and itemgetter(*index_locations_tensor_a)(i) == AnswerIndex]
        elif operation == "-":
            return [A[i[:Rank]]-B[i[Rank:]] for i in IndexCombinatorials if itemgetter(*index_locations_tensor_a)(i) == itemgetter(*index_locations_tensor_b)(i) and itemgetter(*index_locations_tensor_a)(i) == AnswerIndex]
    
    def return_tensor(self, operation):
        I = self.tensor_ans_list_of_index_combinatorics
        Tensor = self.tensor_ans_zero_components
        a = self.tensor_a_rank
        b = self.tensor_b_rank
        Shape = self.tensor_ans_shape
        for i in I:
            Tensor[i] = self.return_component(i, operation)[0]
        return Tensor