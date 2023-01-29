from src.RelativisticPy.general_relativity.string_to_sympy.sympy_parser import SympyParser

# Tensor
"""
        Ex2 = {
                    'index string representation' : '^{b=2}',
                    'order' : 1,
                    'index symbol' : 'b',
                    'running index' : False,
                    'index slice' : slice(2,3),
                    'index space' : 'tangent',
                    'component type' : 'contravariant',
                    'dimention' : 4
                 }
                 """

class Index:
    def __init__(self, index_symbol, order, running_index, component_type, basis, index_value = None):
        self.index_symbol = index_symbol
        self.order = order
        self.running_index = running_index
        self.component_type = component_type
        if isinstance(basis, str):
            self.basis = SympyParser(basis).convertToSympyObject()
        else:
            self.basis = basis
        self.dimention = int(len(self.basis))
        if not self.running_index and isinstance(index_value, int):
            self.index_value = index_value
        elif self.running_index:
            self.index_value = [i for i in range(self.dimention)]
        else:
            raise ValueError("If the index is not a running index (running_index=False) then the index_value argument must be specified as an integer.")
        self._ = slice(0, self.dimention) if self.running_index else slice(self.index_value, self.index_value+1)
        
    def _is_contravariant(self):
        return self.component_type == 'contravariant'
    
    def _is_covariant(self):
        return self.component_type == 'covariant'
    
    def __eq__(self, other):
        if self.index_symbol == other.index_symbol and self.running_index == other.running_index and self.component_type == other.component_type:
            return True
        else:
            return False

    def __neg__(self):
        if self.component_type == 'covariant':
            return Index(self.index_symbol, self.order, self.running_index, 'contravariant', self.basis, self.index_value)
        else:
            return Index(self.index_symbol, self.order, self.running_index, 'covariant', self.basis, self.index_value)

    def __repr__(self):
        """
        Explain method.
        """
        return f"""Index Object:( 
                    'index symbol' : {self.index_symbol}, \n\
                    'order' : {self.order}, \n\
                    'dimention' : {self.dimention}, \n\
                    'running index' : {self.running_index}, \n\
                    'index value(s)' : {self.index_value}, \n\
                    'component type' : {self.component_type} \n\
                )
                """

    def set_start(self):
        """
        Future note: We could easily implement slices feature for indices. So users can see a slice of a tensor specified via the indices.
        Simply add running indices start of slice and end on end of slice.
        """
        if self.running_index:
            return 0
        elif not self.running_index and isinstance(self.index_value, int):
            return self.index_value

    def set_end(self):
        if self.running_index:
            return self.dimention - 1
        elif not self.running_index and isinstance(self.index_value, int):
            return self.index_value
 
    def __iter__(self):
        self.first_index_value = self.set_start()
        self.last_index_value = self.set_end()
        return self

    def __next__(self):
        if self.first_index_value <= self.last_index_value:
            x = self.first_index_value
            self.first_index_value += 1
            return x
        else:
            raise StopIteration

    def __index__(self):
        if not self.running_index:
            return self.constant_value
        else:
            raise ValueError("The index {} you have entered has not been assigned a constant.".format(self.index_symbol))
        
    def __str__(self):
        return self.__repr__()

    def __len__(self):
        return self.dimention
    
    def __mul__(self, other):
        """
        ---- Einstein Summation Convention Inplementation ------
        
        This is a personal definition, for simplicity within the rest of the application.
        When two tensors are multiplied together and the einstein summation convetion is true, this will return the location order of those indices.
        
            Tensor_{a}_{b} * Tensor^{b}_{c} = Tensor_{a}_{c}
        
        This operation will return the following when we aply thit logic to the combinatorials of these indices:
        
            [ [1, 0] ] => Which is saying that the index at location/order 1 of the first tensor is being summed with index at location/order 0 from the second tensor.
        """
        if isinstance(other, Index):
            if self.index_symbol == other.index_symbol and self.component_type != other.component_type and id(self) != id(other):
                return [self.order, other.order]
            else:
                return []
        else:
            raise ValueError("Cannot perform multiplication for the objects you have entered as {}".format(type(other)))
            
    def __add__(self, other):
        """
        ---- Summation of Tesnors ------
        
        This is a personal definition, for simplicity within the rest of the application and simliar but different to the multiplication one.
        When two tensors are added or subtracted together together, the resulting expression is ONLY a tensor expression if the two tensors being added/subtracted have the same index structure.
        However, the indices themselves can sometimes be in different orders:
        
            Tensor_{a}_{b} + Tensor_{b}_{a} = Tensor_{a}_{b}
            Tensor_{a}_{b} - Tensor_{b}_{a} = Tensor_{a}_{b}
            Tensor_{a}_{b} - Tensor_{a}_{b} = Tensor_{a}_{b}
            
        ---- Example One ----
        
            Tensor_{a}_{b} + Tensor_{b}_{a} = Tensor{_{a}_{b}}:
            [ [1, 0],[0,1] ] => Which is saying that the index at location/order 1 of the first tensor is the same as the index at location/order 0 from the second tensor.
                                and index at location/order 0 of the first tensor is the same as the index at location/order 1 from the second tensor.
                                
        ---- Example Two ----
        
            Tensor_{a}_{b} + Tensor_{a}_{b} = Tensor_{a}_{b}:
            [ [0, 0],[1,1] ] => Which is saying that the index at location/order 0 of the first tensor is the same as the index at location/order 0 from the second tensor.
                                and index at location/order 1 of the first tensor is the same as the index at location/order 1 from the second tensor.
        """
        if isinstance(other, Index):
            if self.index_symbol == other.index_symbol and self.component_type == other.component_type and id(self) != id(other):
                return [self.order, other.order]
            else:
                return []
        else:
            raise ValueError("Cannot perform addition for the objects you have entered as {}".format(type(other)))
            
    def __index__(self):
        if not self.running_index:
            return self.index_value
        else:
            raise ValueError("The index {} is a running index and has not been assigned a number. Index class has the slice property as Index._ which you may use to return a slice of the object.".format(self.index_symbol))
