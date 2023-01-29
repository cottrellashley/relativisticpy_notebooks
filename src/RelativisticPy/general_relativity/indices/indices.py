import itertools as it
from src.RelativisticPy.general_relativity.index.index import Index
from src.RelativisticPy.general_relativity.string_to_sympy.sympy_parser import SympyParser
from sympy.tensor.array import MutableDenseNDimArray


class Indices:
    
    """
    Note before alteration of this class:
    
    Do not create a dependence between this class and any of the deserializing classes.
    
    The responsibility of the serializing classes is to decompose the information from strings,
    of different formats. Then to pass those information into this Indices class.
    
    -------- EXMAPLE --------
    
    Index Object:( 
                    'index symbol' : a, 
                    'Coordinate basis' : [t, r, theta, phi],
                    'order' : 0, 
                    'dimention' : 4, 
                    'running index' : True, 
                    'index value(s)' : [0, 1, 2, 3], 
                    'component type' : covariant 
                )

    Index Object:( 
                    'index symbol' : b, 
                    'Coordinate basis' : [t, r, theta, phi],
                    'order' : 1, 
                    'dimention' : 4, 
                    'running index' : True, 
                    'index value(s)' : [0, 1, 2, 3], 
                    'component type' : covariant 
                )
                
    Resulting Indices Object:

    Indices Object:(
                'index objects' : [Index, Index],
                'Coordinate basis' : [t, r, theta, phi],
                'is valid index structure' : True,
                'dimention' : 4,
                'rank' : (0,2),
                'tensor components shape' : (4, 4),
                'is a scalar' : False,
                'summed indices' : []
            )
    """
    def __init__(self, index_objects, basis):
        self.index_objects = index_objects
        if isinstance(basis, str):
            self.basis = SympyParser(basis).convertToSympyObject()
        else:
            self.basis = basis
        self.is_valid_index_structure = self.__validate_index_structure()
        self.dimention = int(len(self.basis))
        self.rank_as_tuple = self.return_rank_structure_as_tuple()
        self.is_scalar = len(self.index_objects) == 0
        self.tensor_component_shape = tuple([i.dimention for i in self.index_objects])
        self._ = [x._ for x in self.index_objects]
        self.__indices_iterator = list(it.product(*[x for x in self.index_objects]))

    def __validate_index_structure(self):
        """
            Does the index's orders match the order to which they are within the list? -> No? -> raise Error
            Are all the index's dimentions the same? -> No? raise Error
            Are all the index's basis the same? -> No? raise Error
            Are all the index's symbols different to one another |-> No? -> is one a contravariant and another a covariant? |-> No? raise Error
                                                                 |-> Yes? -> do nothing
                                                                                                                            |-> Yes? add to summed indices
        """
        return True
    
    def __iter__(self):
        self.__length = int(len(self.__indices_iterator))
        self.__i = 1
        return self

    def __next__(self):
        """
        Method called when object is passed thorugh an iteration (for or while loops)
        For our case, we simply iterate through the combinations of all the combinatorials.
        These combinatorials are reflective of 
        """
        if self.__i <= self.__length:
            x = self.__i
            self.__i += 1
            return self.__indices_iterator[x-1]
        else:
            raise StopIteration
            
    def __repr__(self):
        """
        Explain method.
        """
        return f"""Indices Object:( 
                    'index objects' : {self.index_objects}, \n\
                    'Coordinate basis' : {self.basis}, \n\
                    'is valid index structure' : {self.is_valid_index_structure}, \n\
                    'dimention' : {self.dimention}, \n\
                    'rank' : {self.rank_as_tuple}, \n\
                    'tensor components shape' : {self.tensor_component_shape}, \n\
                    'is a scalar' : {self.is_scalar} \n\
                )
                """
    def __eq__(self, other_indices):
        """
        When both indices have equal symbols and equal number of covarient and/or contravariant indices in any order:
        ---- TRUE example ---
        _{a}_{b} == _{b}_{a} -> true (We can letter use this as a property to define commutator of indices)
        _{a}_{b} == _{a}_{b} -> true
        ^{a}_{b} == _{b}^{a} -> true
        
        ---- FALSE example ---
        _{a}^{b} == _{b}^{a} -> false
        _{a}_{b} == ^{b}_{a} -> false
        _{a}_{b} == _{a}_{b}_{c} -> false
        _{a}_{b} == _{a}_{c} -> false
        
        """
        boolean_combinatorial_list = [i==j for (i, j) in list(it.product(self.index_objects, other_indices.index_objects))]
        return boolean_combinatorial_list.count(True) == len(self)

    def _is_valid_indices(self, indices):
        return indices

    def __mul__(self, other_indices):
        
        A = self.index_objects
        B = other_indices.index_objects

        # Remove both sumed indices from result if indices are summed over.
        # Remove only last index if they are repeated.
        for (i, j) in list(it.product(self.index_objects, other_indices.index_objects)):
            if len(i*j) > 0:
                A.remove(i)
                B.remove(j)
            elif len(i+j) > 0:
                B.remove(j)
        Result = A + B
        
        # Re-enter orders / locations w.r.t new tensor indices
        for i in range(len(Result)):
            Result[i].order = i

        return Result
    
    def __add__(self, other_indices):
        return Indices(self, self.basis)
    
    def __sub__(self, other_indices):
        return Indices(self, self.basis)

    def return_rank_structure_as_tuple(self):
        return (int([x.component_type for x in self.index_objects].count('contravariant')), int([x.component_type for x in self.index_objects].count('covariant')))
    
    def return_new_index(self, other_indices, order, running_index, component_type, index_value = None):
        index_symbols_list = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
                          "theta","phi","alpha","beta","mu","nu","sigma","delta","omega","gamma","alpha","beta","epsilon","zeta",
                          "eta","kappa","lambda","pi"]
        list_of_indices= [i.index_symbol for i in self.index_objects] + [i.index_symbol for i in other_indices.index_objects]
        new_index_symbol_not_in_others = list(set(index_symbols_list) - set(list_of_indices))[0]
        return Index(new_index_symbol_not_in_others, order, running_index, component_type, self.basis, index_value)
    
    def __len__(self):
        return len(self.index_objects)
    
    def get_zero_tensor(self):
        return MutableDenseNDimArray.zeros(*self.tensor_component_shape)
