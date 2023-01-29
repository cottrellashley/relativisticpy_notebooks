import sympy as smp
from sympy.tensor.array import MutableDenseNDimArray
from src.RelativisticPy.general_relativity.string_to_sympy.sympy_parser import SympyParser



# Note: Parser does not work when all numbers imputs
class Tensor:
    """
    Tensor Class
    
    This class can be used to define tensors, but they are also the Base classes for the GrTensor class.
    """
    def __init__(self, components, basis):
        """
        Constructor

        Parameters
        ----------
        components : str OR MutableDenseNDimArray
            If componets of type str, then we generate a MutableDenseNDimArray from the string using SympyParser.
            If componets of type MutableDenseNDimArray, then we pass directly to the class property.
        basis : str OR MutableDenseNDimArray
            If componets of type str, then we generate a MutableDenseNDimArray from the string using SympyParser.
            If componets of type MutableDenseNDimArray, then we pass directly to the class property.
            
        """
        if isinstance(components, str):
            self.components = SympyParser(components).convertToSympyObject()
        elif isinstance(components, MutableDenseNDimArray):
            self.components = components
        else:
            raise ValueError("Component input must be either a string or a sympy object of type MutableDenseNDimArray.")
    
        self.dimention = None
        #else:
        #    raise ValueError("Basis input must be either a string or a sympy object of type MutableDenseNDimArray.")

    def __str__(self):
        """
        Explain method.
        """
        return str(self.components)
    
    def __repr__(self):
        """
        Explain method.
        """
        return f"""Tensor Object:( \n\
        Components : {self.components}
        )
        """
    
    def __mul__(self, other):
        """
        Multiplication
        """
        return smp.tensorproduct(self.components, other.components)
    
    def __rmul__(self, other):
        return self.__mul__(other)