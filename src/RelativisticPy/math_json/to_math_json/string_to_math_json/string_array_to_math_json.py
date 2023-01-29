import re
import numpy as np
from src.RelativisticPy.math_json.to_math_json.string_to_math_json.string_to_math_json import StringToMathJson

class StringArrayToMathJSON:
    def __init__(self, string_array):
        if isinstance(string_array, str):
            self.string_array = string_array
        else:
            raise ValueError("Expected string as argument.")

    def to_mathJson(self):
        NumpyArray = self.numpyfy_string_array()
        IterableComponentsForArray = lambda Array : list(it.product(np.arange(np.array(Array).shape[0]), repeat = len(np.array(Array).shape)))
        return np.array([StringToMathJson(NumpyArray[i]).calculate().objectJson for i in IterableComponentsForArray(NumpyArray)]).reshape(NumpyArray.shape).tolist()

    def numpyfy_string_array(self):
        StringArray = self.string_array
        empty_string_array = re.sub('[^\[\]\,]','1', StringArray)
        return np.array(StringArray.replace('[','').replace(']','').split(',')).reshape(*np.array(eval(empty_string_array)).shape)