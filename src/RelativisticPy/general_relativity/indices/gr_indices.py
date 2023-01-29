import re

from src.RelativisticPy.general_relativity.indices.indices import Indices
from src.RelativisticPy.general_relativity.index.gr_index import GrIndex
from src.RelativisticPy.general_relativity.string_to_sympy.sympy_parser import SympyParser


class GrIndices(Indices):
    
    """
    Note before alteration of this class:
    
    Do not create a dependence between this class and any of the deserializing classes.
    
    The responsibility of the serializing classes is to decompose the information from strings,
    of different formats. Then to pass those information into this Indices class.
    
    
    
    Index = {
                'index' : '_{a}',
                'order' : 0,
                'symbol' : 'a',
                'running index' : True,
                'constant' : None,
                'index space' : 'cotangent',
                'component type' : 'covariant',
                'dimention' : 4
            }

    Index = {
                'index' : '_{b}',
                'order' : 1,
                'symbol' : 'b',
                'running index' : True,
                'constant' : None,
                'index space' : 'cotangent',
                'component type' : 'covariant',
                'dimention' : 4
            }

    indices = {
                'indices string representation' : '_{a}_{b}',
                'index objects' : [Index, Index],
                'indices slice' : slice,
                'dimention' : 4,
                'rank' : (0,2),
                'scalar' : False,
                'tensor is covariant' : bool,
                'summed indices' : []
            }
    """
    def __init__(self, indices, basis):
        
        # ----- Public ------
        self.indices_string_representation = self._is_valid_indices(indices)
        if isinstance(basis, str):
            self.basis = SympyParser(basis).convertToSympyObject()
        else:
            self.basis = basis
        Indices.__init__(self, self.return_index_objects(), self.basis)
        
    def return_index_objects(self):
        lis = []
        individual_indices = [item for item in re.split('(?=[_^])', self.indices_string_representation) if item]
        for i in range(len(individual_indices)):
            lis.append(GrIndex(individual_indices[i], i, self.basis))
        return lis
            
    def __repr__(self):
        """
        Explain method.
        """
        return f"""GrIndex Object:( 
                    'index string representation' : {self.indices_string_representation}, \n\
                    'index objects' : {self.index_objects}, \n\
                    'Coordinate basis' : {self.basis}, \n\
                    'is valid index structure' : {self.is_valid_index_structure}, \n\
                    'dimention' : {self.dimention}, \n\
                    'rank' : {self.rank_as_tuple}, \n\
                    'tensor components shape' : {self.tensor_component_shape}, \n\
                    'is a scalar' : {self.is_scalar} \n\
                )
                """

    def return_slices(self):
        return tuple([x.slc() for x in self.return_index_instances()])

    def _is_valid_indices(self, indices):
        return indices    

    def get_tensor_index(self, index_key):
        address = self._index_address.get(index_key)
        if not address:
            raise ValueError(index_key)
        return address

    def metric_product_from_index_structure(self):
        index_list = [item for item in re.split('(?=[_^])', self.indices_string_representation) if item]
        List_ = self.indices_string_representation
        list_metric_indices = []
        list_originaltensor = []
        #for i in self.return_index_instances():
        #    if i.is_contravariant:
        return list_metric_indices
    
    def return_new_index(self, indices, List):
        li = [i for i in indices]
        contra = "^{" + [i for i in List if i not in li][0] + "}"
        cov = "_{" + [i for i in List if i not in li][0] + "}"
        return [contra, cov]
    