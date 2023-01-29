from src.RelativisticPy.general_relativity.tensor_operation.index_product import IndexProduct

class GrTensorProduct(IndexProduct):
    
    def __init__(self, 
                    TensorA, 
                    TensorB,
                    operation : str
                ):
        self.TensorA = TensorA
        self.TensorB = TensorB
        self.operation = operation
        IndexProduct.__init__(self, 
                                    self.TensorA.tensor_indices, 
                                    self.TensorB.tensor_indices,
                                    self.operation
                                )
        self.return_tensor = self.return_tensor()
        
    def compute_component(self):
        return {'*' : self.return_mult_component,
                '+' : self.return_add_component,
                '-' : self.return_sub_component}
        
    def return_mult_component(self, AnswerIndex):
        A = self.TensorA.all_components
        B = self.TensorB.all_components
        list_of_relevant_indices = self.return_indices_array_for_component(AnswerIndex)
        return sum([A[Indices[0]]*B[Indices[1]] for Indices in list_of_relevant_indices])
    
    def return_add_component(self, AnswerIndex):
        A = self.TensorA.all_components
        B = self.TensorB.all_components
        list_of_relevant_indices = self.return_indices_array_for_component(AnswerIndex)
        return sum([A[Indices[0]]+B[Indices[1]] for Indices in list_of_relevant_indices])
    
    def return_sub_component(self, AnswerIndex):
        A = self.TensorA.all_components
        B = self.TensorB.all_components
        list_of_relevant_indices = self.return_indices_array_for_component(AnswerIndex)
        return sum([A[Indices[0]]-B[Indices[1]] for Indices in list_of_relevant_indices])

    def return_tensor(self):
        zero_tensor = self.indices_result.get_zero_tensor()
        computed_component = self.compute_component()[self.operation]
        for i in self.indices_result:
            zero_tensor[i] = computed_component(i)
        return zero_tensor