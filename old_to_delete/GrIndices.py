import sympy as smp
import re
import numpy as np
from GrIndex import GrIndex


class GrIndices(GrIndex):
    def __init__(self, indices):
        self.indices = self.__is_valid_indices(indices)
        self.rank_as_tuple = self.return_rank_structure_as_tuple()

    def __is_valid_indices(self, indices):
        return indices
    
    def __mul__(self, otherIndeces):
        return self.sum_indices(otherIndeces)

    def sum_indices(self, otherIndeces):
        Summed_indices = []
        Total = self.return_index_instances() + otherIndeces.return_index_instances()
        ListA = [x.index for x in Total]
        for i in self.return_index_instances():
            for j in otherIndeces.return_index_instances():
                if i == j:
                    Summed_indices.append([int(i.order), int(j.order)])
                    ListA.remove(i.index)
                    ListA.remove(j.index)
        return ''.join(ListA)
                    
    def return_index_instances(self):
        instance_list = []
        individual_indices = [item for item in re.split('(?=[_^])', self.indices) if item]
        for i in range(len(individual_indices)):
            instance_list.append(GrIndex(individual_indices[i],int(i)))
        return instance_list
    
    def return_rank_structure_as_tuple(self):
        index_identifier_list = [item[0] for item in re.split('(?=[_^])', self.indices) if item]
        lower_index_list = len([i for i in index_identifier_list if i == '_'])
        return (len([i for i in index_identifier_list if i == '_']), len([i for i in index_identifier_list if i == '^']))
