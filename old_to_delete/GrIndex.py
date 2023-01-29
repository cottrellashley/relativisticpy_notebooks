import sympy as smp
import re
import numpy as np

class GrIndex:
    def __init__(self, index, order):
        self.index = self.__is_valid_index(index)
        self.order = self.__is_valid_order(order)
        
    def __is_valid_index(self, index):
        return index
    
    def __is_valid_order(self, order):
        return order
    
    def __eq__(self, other):
        if self.retrunIndex(self.index) == self.retrunIndex(other.index):
            return True
        else:
            return False

    def retrunIndex(self, indexStructure):
        return re.search('[a-z]+', indexStructure).group()