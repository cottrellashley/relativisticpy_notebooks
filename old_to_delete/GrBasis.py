import sympy as smp
import re
import numpy as np

class GrBasis:
    def __init__(self, components, coordinate_system : str = None):
        self.coordinate_system = coordinate_system
        self.components = components
        
    def __len__(self):
        return len(self.components)