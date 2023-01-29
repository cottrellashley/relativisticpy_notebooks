class MathJSON:
    def __init__(self, dict):
        self.dict = dict
        
    def __add__(self, other):
        return MathJSON({ 'ADD' : [self.dict, other.dict] })
    
    def __mul__(self, other):
        return MathJSON({ 'MUL' : [self.dict, other.dict] })
    
    def __sub__(self, other):
        return MathJSON({ 'MINUS' : [self.dict, other.dict] })

    def __pow__(self, other):
        return MathJSON({ 'POW' : [self.dict, other.dict] })
    
    def __truediv__(self, other):
        return MathJSON({ 'DIV' : [self.dict, other.dict] })

    def func(self, variables):
        return MathJSON({ 'FUNCTION' : [self.dict, variables.dict]})

    def integrate(self, measure):
        return MathJSON({ 'INT' : [self.dict, measure.dict ]})

    def differentiate(self, measure):
        return MathJSON({ 'DIFF' : [self.dict, measure.dict ]})
