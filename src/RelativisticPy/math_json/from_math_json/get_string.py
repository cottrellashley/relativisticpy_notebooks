
class MathJsonToString:
    """
    CURRENTLY NOT WORKING YET

    BUT THIS GIVES AN IDEA
    """
    def __init__(self, x):
        self.operations = {"Add" : lambda List : "(" + str(List[0]) + "+" + str(List[1]) + ")",
                           "Mul" : lambda List : "(" + str(List[0]) + "+" + str(List[1]) + ")",
                           "Sub" : lambda List : "(" + str(List[0]) + "+" + str(List[1]) + ")",
                           "Div" : lambda List : "(" + str(List[0]) + "+" + str(List[1]) + ")",
                           "Diff" : lambda List : "diff(" + str(List[0]) + "," + str(List[1]) + ")",
                           "Int" : lambda List : "integrate(" + str(List[0]) + "," + str(List[1]) + ")",
                           "Eq" : lambda List : str(List[0]) + " = " + str(List[1]),
                           "integer" : lambda x : str(x),
                           "tensor" : lambda x : x}
        
        if isinstance(x, dict):
            if [i for i in x][0] == "Diff":
                self.x = self.operations["Diff"](x["Diff"])
            elif [i for i in x][0] == "Int":
                self.x = self.operations["Int"](x["Int"])
            elif [i for i in x][0] == "integer":
                self.x = self.operations["integer"](x["integer"])
            else:
                self.x = self.operations[[i for i in x][0]](x[[i for i in x][0]])
        else:
            self.x = x

    def get_string(self):
        return self.x