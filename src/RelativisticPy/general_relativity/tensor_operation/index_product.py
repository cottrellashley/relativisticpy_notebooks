from src.RelativisticPy.general_relativity.indices.indices import Indices
from operator import itemgetter
import itertools as it

class IndexProduct:
    """
    Make this class dependent on Indices Base class which has the data strcuture of all the base components we need in order to calculate the thing we want.
    The goal here is to make all classes completly independeny of the "_{a}^{b}" implementation. This string encodes the inforamtion we need in order to fill in
    the base class data. The base class AND the class which makes the conversion both can be put in as arguments to this class.
    """
    def __init__(self, indices1, indices2, operation):
        self.indices1 = indices1
        self.indices2 = indices2
        self.operation = self._operation_is_valid(operation)
        self.resultant_indices = self.dic()[self.operation]
        self.is_valid_tensor_expression = self._is_valid_tensor_expression()[self.operation]
        self.transpose_resulting_indices = self.transpose_list(self.resultant_indices)
        if self.is_valid_tensor_expression:
            self.indices_result = Indices(self.indices1*self.indices2, indices1.basis)
        else:
            raise ValueError("The indices and operation you have entered do not amount to a valid Tesnor expression. Please enter a valid tensor expression.")
    
    def _is_valid_tensor_expression(self):
        return {'*' : self.dic()['+'] == [],
                '+' : self.indices1 == self.indices2,
                '-' : self.indices1 == self.indices2}
    
    def dic(self):
        return {'*' : [i*j for i in self.indices1.index_objects for j in self.indices2.index_objects if len(i*j) > 0],
                '+' : [i+j for i in self.indices1.index_objects for j in self.indices2.index_objects if len(i+j) > 0],
                '-' : [i+j for i in self.indices1.index_objects for j in self.indices2.index_objects if len(i+j) > 0]}
    
    def _operation_is_valid(self, op):
        if op.replace(' ', '') in ['*', '-', '+']:
            return op.replace(' ', '')
        else:
            raise ValueError('Opperation input must be one of the following strings: + or - or *')
    
    def expression_is_covariant(self):
        boolean = True
        if self.operation == "*" and len(self.return_list_of_repeated_indices()) > 0:
            boolean = False
        elif self.operation == "-" and len(self.return_list_of_indices_to_sum_over()) > 0:
            boolean = False
        elif self.operation == "+" and len(self.return_list_of_indices_to_sum_over()) > 0:
            boolean = False
        return boolean
    
    def get_list(self):
        ListA = []
        ListB = []
        for i in self.indices1.index_objects:
            for j in self.indices_result.index_objects:
                if i == j:
                    ListA.append(i.order)
        for i in self.indices2.index_objects:
            for j in self.indices_result.index_objects:
                if i == j:
                    ListB.append(i.order)
        return [ListA, ListB]
    
    def transpose_list(self, l):
        """
        This will transpose a list.
        Note: This might be a function used else where, so might be good to place this in a helper file.
        
        Input : [[1,2],[3,4],[5,6]]
        Output: [[1,3,5],[2,4,6]]
        """
        return list(map(list, zip(*l)))
    
    """
    The following needs to work for:
    
    '+' : Check whether it is a correct expression and return the correct order, specified by the tensors indices.
    '-' : Same story as above.
    '*' : 
    """
    
    def ans_indices_locations(self):
        if self.operation == '*':
            return ([i for i in range(len(self.indices1)) if i not in self.transpose_resulting_indices[0]], [i for i in range(len(self.indices2)) if i not in self.transpose_resulting_indices[1]])
        else:
            raise ValueError('This function does not apply to any operation other than: *')
    
    def return_combinatorial_indices(self):
        #[(IndexA, IndexB) for (IndexA, IndexB) in list(it.product(self.indices1,self.indices2)) if itemgetter(*self.transpose_resulting_indices)(IndexA) == itemgetter(*self.transpose_resulting_indices)(IndexB)]
        return [(IndexA, IndexB) for (IndexA, IndexB) in list(it.product(self.indices1,self.indices2)) if itemgetter(*self.transpose_resulting_indices[0])(IndexA) == itemgetter(*self.transpose_resulting_indices[1])(IndexB)]
    
    def return_indices_array_for_component(self, components = None):
        """
        The following needs to work for:
        '+' : Check whether it is a correct expression and return the correct order, specified by the tensors indices.
        '-' : Same story as above.
        '*' : 
        Clumsy needs to be redone more elegantly. But for now it works and will return:
        Tensor Product
        Scalars
        Sums and subtractions
        All based on the indices you have done.
        """
        if not self.indices_result.is_scalar and components != None and self.operation == '*':
            _ = self.get_list()
            _1 = [i for i in range(len(_[0]))]
            _2 = [i for i in range(len(_[0]), len(_[0]) + len(_[1]))]
            return [(IndicesA, IndicesB) for (IndicesA, IndicesB) in self.return_combinatorial_indices() if itemgetter(*_[0])(IndicesA) == itemgetter(*_1)(components) \
                    and itemgetter(*_[1])(IndicesB) == itemgetter(*_2)(components)]
        
        elif not self.indices_result.is_scalar and components != None and self.operation in ['+', '-']:
            return [(IndicesA, IndicesB) for (IndicesA, IndicesB) in self.return_combinatorial_indices() if IndicesA == tuple(components)]

        else:
            return self.return_combinatorial_indices()

