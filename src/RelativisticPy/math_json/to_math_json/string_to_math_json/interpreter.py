from src.RelativisticPy.math_json.to_math_json.math_json import MathJSON

class Interpreter:

    def compute(self, node):
        if type(node).__name__ == 'AddNode':
            return MathJSON(node.node_a.dict)+MathJSON(node.node_a.dict)

    def visit(self, node):
        if isinstance(node, list):
            return [getattr(self, f"visit_{type(i).__name__}")(i).dict for i in node]
        else:
            method_name = f"visit_{type(node).__name__}"
            method = getattr(self, method_name)
            return method(node)

    def visit_IntNode(self, node):
        return MathJSON(node.dict)

    def visit_FloatNode(self, node):
        return MathJSON(node.dict)

    def visit_TensorNode(self, node):
        return MathJSON(node.dict)

    def visit_VariableNode(self, node):
        return MathJSON(node.dict)

    def visit_PowNode(self, node):
        return MathJSON(self.visit(node.node_a).dict) ** MathJSON(self.visit(node.node_b).dict)

    def visit_AddNode(self, node):
        return MathJSON(self.visit(node.node_a).dict) + MathJSON(self.visit(node.node_b).dict)

    def visit_SubNode(self, node):
        return MathJSON(self.visit(node.node_a).dict) - MathJSON(self.visit(node.node_b).dict)

    def visit_MulNode(self, node):
        return MathJSON(self.visit(node.node_a).dict) * MathJSON(self.visit(node.node_b).dict)

    def visit_DivNode(self, node):
        return MathJSON(self.visit(node.node_a).dict) / MathJSON(self.visit(node.node_b).dict)

    def visit_DifferentialNode(self, node):
        return MathJSON(self.visit(node.node_a).dict).differentiate(MathJSON(self.visit(node.node_b)))

    def visit_IntegrateNode(self, node):
        return MathJSON(self.visit(node.node_a).dict).integrate(MathJSON(self.visit(node.node_b)))

