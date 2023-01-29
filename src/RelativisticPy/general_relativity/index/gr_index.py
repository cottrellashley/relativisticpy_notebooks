import re
from src.RelativisticPy.general_relativity.index.index import Index

class GrIndex(Index):
    """
    THIS WILL BECOME A STRING PARSER FOR SPECIFIC REPRESENTATION OF A STRING.
    CHANGE NAME TO SOMETHING SPECIFIC TO THIS PARSER.
    Class Representing an index in General Relativity, encoded as covariant or contravariant and also summation convation.
    
    Here are a few examples of how the data structure of the class can look like:
    
    This class decodes the string representation of the form: _{ index_symbol (= index_value) }
    
        Ex1 = {
                    'index string representation' : '_{a}',
                    'order' : 0,
                    'index symbol' : 'a',
                    'running index' : True,
                    'index slice' : slice(0, dimention),
                    'index space' : 'cotangent',
                    'component type' : 'covariant',
                    'dimention' : 4
                 }

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
                 
    Some ideas to extend this class are:
        - Notice how everything is generic, but the string representation. In other words, the representation encodes most of the properties of the class.
          So, inprinciple we can simple define other representations which encode the same information, say for instance Latex index format.
          The class should be written such that as long as everything within the class carries from the representation and dimention, then the whole package
          should still work. I.e. the class should be extensible to other index string representations.
    
    Note:   
    Covariant => Lower indices
    Contravariant => Upper indices

    """
    integers = {'0': 0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9}
    def __init__(self, index_representation, order, coordinate_basis):
        """
        Explain Constructor parameters
        This class inherits the Index class:
            Index(index_symbol, order, running_index, component_type, basis, index_value = None)
            
        """
        integers = {'0': 0, '1':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9}
        self.index_string_representation = self.__str_rep_is_valid(index_representation)
        Index.__init__(self, 
                       index_symbol = re.search('[a-zA-Z]+', self.index_string_representation).group(),
                       order = self.__is_valid_order(order),
                       running_index = not bool(re.search('^[^=]*(=)([0-9]+)[^=]*$', self.index_string_representation)),
                       component_type = 'covariant' if (self.index_string_representation[0] == "_") else 'contravariant',
                       basis = self.__is_valid_basis(coordinate_basis),
                       index_value = integers[re.split('[=]', self.index_string_representation.replace('{','').replace('}','').replace('_','').replace('^',''))[1].replace(" ","")] if bool(re.match('^[^=]*(=)([0-9]+)[^=]*$', self.index_string_representation)) else None
                       )

        
    def __is_valid_basis(self, basis):
        return basis
    
    def __str_rep_is_valid(self, index):
        index_ = index.replace(" ", "")
        condition1 = index_[0] == "_" or index_[0] == "^"
        condition2 = index_[1] == "{"
        condition3 = index_[-1] == "}"
        condition4 = bool(re.search('^[^=]*(=)([0-9]+)[^=]*$', index_)) or bool(re.search('^[^=]*[a-zA-Z]+[^=]*$', index_))
        if not condition1:
            raise ValueError("The index {} you have entered, does not contain the necessary characters _ OR ^ to indicate covariace or contravariance.".format(index_))
        elif not condition2 or not condition3:
            raise ValueError("The index {} you have entered, does not contain closing OR opening curly brakets.".format(index_))
        elif not condition4:
            raise ValueError("The following characters you have entered in the index are not recognized: {}".format(index_.replace('{','').replace('}','').replace('_','').replace('^','')))
        else:
            return index_

    def __is_valid_order(self, order):
        valid = type(order) == int
        if valid:
            return order
        else:
            raise ValueError("Index order must be of type: int")
        

    def __eq__(self, other):
        if self.index_string_representation == other.index_string_representation:
            return True
        else:
            return False

    def __neg__(self):
        if self.index_string_representation[0] == '_':
            return GrIndex(self.index_string_representation.replace('_', '^'), self.order, self.basis)
        else:
            return GrIndex(self.index_string_representation.replace('^', '_'), self.order, self.basis)

    def __repr__(self):
        """
        Explain method.
        """
        return f"""GrIndex Object:( 
                    'index string representation' : {self.index_string_representation}, \n\
                    'index symbol' : {self.index_symbol}, \n\
                    'order' : {self.order}, \n\
                    'dimention' : {self.dimention}, \n\
                    'running index' : {self.running_index}, \n\
                    'index value(s)' : {self.index_value}, \n\
                    'component type' : {self.component_type} \n\
                )
                """

    def __index__(self):
        if not self.running_index:
            str_num = re.split('[=]', self.index_string_representation.replace('{','').replace('}','').replace('_','').replace('^',''))[1]
            if str_num in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                return int(eval(str_num))
            else:
                raise ValueError("The index {} you have entered, is not an integer number.".format(self.index_string_representation))
        else:
            raise ValueError("The index {} you have entered has not been assigned a constant.".format(self.index_string_representation))
