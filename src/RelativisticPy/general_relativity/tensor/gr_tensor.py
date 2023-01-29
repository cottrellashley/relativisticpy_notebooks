from src.RelativisticPy.general_relativity.indices.indices_patterns import IndexRepresentations
from src.RelativisticPy.general_relativity.tensor_operation.gr_tensor_product import GrTensorProduct
from src.RelativisticPy.general_relativity.indices.gr_indices import GrIndices

import sympy as smp

class GrTensor:
    """
    A class used to represent an Animal

    ...

    Attributes
    ----------
    says_str : str
        a formatted string to print out what the animal says
    name : str
        the name of the animal
    sound : str
        the sound that the animal makes
    num_legs : int
        the number of legs the animal has (default 4)

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """
    def __init__(self,
                 components,
                 indices,
                 name : str = 'none'
                 ):
        """
        Parameters
        ----------
        components : MutableDenseNDimArray
            The actual sympy components of the tensor.
        indices : Indices
            The indices of the tensor, which itself contains basis and index structure of the tensor.
        name : string
            The name of tensor, this does not affect calculations, it is merely for indentification.
        """

        self.tensor_indices = IndexRepresentations(indices, basis if isinstance(indices,str) else indices.basis ).indices_object
        self.basis = self.tensor_indices.basis
        self.all_components = components
        self.components = self.all_components[tuple(self.tensor_indices._)]
        self.name = name
        if self.tensor_indices.is_scalar:
            self.shape = 1
            self.rank = self.shape
        else:
            self.shape = smp.shape(self.components)
            self.rank = len(self.shape)
        self.dimention = self.tensor_indices.dimention
        
    def __add__(self, other):
        return GrTensorProduct(self, other, "+").return_tensor()
    
    def __radd__(self, other):
        return GrTensorProduct(other, self, "+").return_tensor()
    
    def __mul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return GrTensor(other*self.components, self.basis, self.tensor_indices)
        elif isinstance(other, GrTensor):
            product = GrTensorProduct(self, other, "*")
            return GrTensor(product.return_tensor(), product.indices_result)
        else:
            raise ValueError("Object {} is not compatible with operation * with a GrTensor object.".format(other))
        
    def __rmul__(self, other):
        if isinstance(other, float) or isinstance(other, int):
            return GrTensor(other*self.components, self.tensor_indices)
        elif isinstance(other, GrTensor):
            return GrTensorProduct(other, self, "*").return_tensor()
        else:
            raise ValueError("Object {} is not compatible with operation * with a GrTensor object.".format(other))
    
    def __sub__(self, other):
        return GrTensorProduct(self, other, "-").return_tensor()
    
    def __rsub__(self, other):
        return GrTensorProduct(other, self, "-").return_tensor()
    
    def __truediv__(self, other):
        if type(other) == float or type(other) == int:
            return GrTensor(self.components/other,self.tensor_indices)
        else:
            raise ValueError("Cannot divide with anything other than int or float.")
            
    def gr_tensor_as_dict(self):
        return {
                'name' : self.name,
                'components' : str(self.components),
                'basis' : str(self.basis),
                'dimention' : self.dimention,
                'indices' : GrIndices(self.indices).indices_as_dict()
                }
    
    def return_tensor_ans_with_numbers(self, number):
        D = self.dimention
        A = int(self.rank)
        Shape = self.return_tensor_ans_shape()
        return smp.MutableDenseNDimArray(smp.ones(D**A)*number, Shape)
