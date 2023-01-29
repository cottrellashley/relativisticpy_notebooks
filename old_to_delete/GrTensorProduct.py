import sympy as smp
import numpy as np
import re
from BaseTensorExpression import BaseTensorExpression
from GrTensor import GrTensor


class GrTensorProduct(BaseTensorExpression):
    
    def __init__(self, A:GrTensor, B:GrTensor):
        BaseTensorExpression.__init__(self, A, B)
        self.list_of_index_locations_to_sum_over_wrt_each_tensor = self.return_list_of_indices_to_sum_over()
        self.list_of_all_tensor_index_concatinated_combinatorials = list(it.product(np.arange(0, self.tensor_a_dimention, 1), repeat = self.tensor_a_rank + self.tensor_b_rank))
        self.list_of_list_of_summed_index_locations_wrt_both_tensor_indices_concatinanted = [[i[0],i[1] + self.tensor_a_rank] for i in self.list_of_index_locations_to_sum_over_wrt_each_tensor]
        self.flat_list_of_summed_index_locations_wrt_both_tensor_indices_concatinanted = [item for sublist in self.list_of_list_of_summed_index_locations_wrt_both_tensor_indices_concatinanted for item in sublist]
        self.flat_list_of_ans_tensor_index_locations_wrt_both_tensor_indices_concatinanted = [i for i in list(np.arange(0, self.tensor_a_rank + self.tensor_b_rank, 1)) if i not in self.flat_list_of_summed_index_locations_wrt_both_tensor_indices_concatinanted]
        self.flat_list_of_tensor_a_summed_index_locations_wrt_both_tensor_indices_concatinanted = [i[0] for i in self.list_of_list_of_summed_index_locations_wrt_both_tensor_indices_concatinanted]
        self.flat_list_of_tensor_b_summed_index_locations_wrt_both_tensor_indices_concatinanted = [i[1] for i in self.list_of_list_of_summed_index_locations_wrt_both_tensor_indices_concatinanted]
        
    def return_list_of_indices_to_sum_over(self):
        Summed_indices = []
        A_instances = self.tensor_a_list_of_index_instances
        B_instances = self.tensor_b_list_of_index_instances
        Total = A_instances + B_instances
        for i in A_instances:
            for j in B_instances:
                if i == j and i.index[0] != j.index[0]:
                    Summed_indices.append([int(i.order), int(j.order)])
        return Summed_indices
    
    def return_component(self, AnswerIndex):
        A = self.tensor_a_components
        B = self.tensor_b_components
        IndexCombinatorials = self.list_of_all_tensor_index_concatinated_combinatorials
        index_locations_tensor_a = self.flat_list_of_tensor_a_summed_index_locations_wrt_both_tensor_indices_concatinanted
        index_locations_tensor_b = self.flat_list_of_tensor_b_summed_index_locations_wrt_both_tensor_indices_concatinanted
        ans_index_locations = self.flat_list_of_ans_tensor_index_locations_wrt_both_tensor_indices_concatinanted
        Rank = self.tensor_a_rank
        return sum([A[i[:Rank]]*B[i[Rank:]] for i in IndexCombinatorials if itemgetter(*index_locations_tensor_a)(i) == itemgetter(*index_locations_tensor_b)(i) and itemgetter(*ans_index_locations)(i) == AnswerIndex])
    
    def return_tensor(self):
        I = self.tensor_ans_list_of_index_combinatorics
        Tensor = self.tensor_ans_zero_components
        a = self.tensor_a_rank
        b = self.tensor_b_rank
        Shape = self.tensor_ans_shape
        for i in I:
            Tensor[i] = self.return_component(i)
        return Tensor