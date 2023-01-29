import re
from src.RelativisticPy.general_relativity.indices.gr_indices import GrIndices
from src.RelativisticPy.general_relativity.indices.indices import Indices
from src.RelativisticPy.general_relativity.string_to_sympy.sympy_parser import SympyParser


class IndexRepresentations:
    """
    IMPORTANT: Always try and break this class by checking whether a string passes the match of more than one Category!!
    Optional Use class.
    """
    def __init__(self, indices, basis):
        if isinstance(indices, str):
            self.indices_string = indices
        elif isinstance(indices, Indices) or isinstance(indices, GrIndices):
            self.indices_string = ''
            self.indices_object = indices
        else:
            raise ValueError("The IndexRepresentations only takes strings as arguments, please make sure the object you are passing into this object is a string.")
        if isinstance(basis, str):
            self.basis = SympyParser(basis).convertToSympyObject()
        else:
            self.basis = basis
        if self.is_representation_one():
            self.indices_object = GrIndices(self.indices_string, self.basis)
        
    def is_representation_one(self):
        """
        Example of string to match this category:
            ^{a}^{b}_{theta = 0}_{phi=1}
        
        Conditions for this category to be recognized: 
            - Cannot contain anything but: = or { or } or _ or ^ or [a-zAZ0-9]
            - Has correct pattern: _{}^{}...
            - Between every curly brackets {}, there must be at least one [A-Za-z]+ character/word.
        """
        return bool(re.search("^((\^|\_)(\{)(\}))+$", re.sub('[^\^^\_^\{^\}]',"", self.indices_string).replace(" ",'')))

    def is_representation_two(self):
        """
        Example of string to match this category:
            [^a, ^b, _theta = 0, _phi = 1]
        """
        return NotImplementedError

    def is_representation_three(self):
        """
        Example of string to match this category:
            ^{a}^{b}_{theta:0}_{phi:1}
        
        Conditions for this category to be recognized: 
            - Cannot contain anything but: = or { or } or _ or ^ or [a-zAZ0-9]
            - Has correct pattern: _{}^{}...
            - Between every curly brackets {}, there must be at least one [A-Za-z]+ character/word.
        """
        return NotImplementedError

    def is_latex_representation(self):
        """
        Example of string to match this category:
            _{mu = 0}^{nu sigma = 0 phi}
        """
        return NotImplementedError