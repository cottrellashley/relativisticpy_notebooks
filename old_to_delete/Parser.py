import re
import sympy as smp
import numpy as np
from sympy import sin, cos, tan, sinh, cosh, tanh, exp, asin, acos, atan

class BasisValidator:
    def __init__(self, basis_string: str = ""):
        self.Basis = self._is_valid_basis(basis_string)
        self.Dimention = len(self.Basis.replace(']','').replace('[','').split(','))

    def _is_valid_basis_values(self, basis):
        valid_basis_values = Constants["Valid_Basis_Words"]
        pattern0 = "[a-zA-Z][a-zA-Z]+"
        lis = [x for x in re.finditer(pattern0, basis)]
        unrecognizedValues = []
        for i in lis:
            if i.group() not in valid_basis_values:
                unrecognizedValues.append(i.group())
        if basis == "":
            return basis
        elif len(unrecognizedValues) != 0:
            raise ValueError("Some of the values you have entered in the Basis are not valid or recognized.")
        else:
            return basis

    def _is_valid_basis(self, basis):
        basis_after_value_validation = self._is_valid_basis_values(basis)
        B = bool(re.match("^\[(\s*[a-zA-Z]+\s*\,\s*)+(\s*[a-zA-Z]+\s*)\]$", basis_after_value_validation))
        if basis == "":
            return basis
        elif not B:
            raise ValueError("The format of the basis you have entered is not correct.")
        else:
            return basis

class MetricValidator(BasisValidator):
    def __init__(self, metric: str = "", basis: str = ""):
        BasisValidator.__init__(self, basis_string = basis)
        self.Metric = self._is_valid_metric(metric)

    def _metric_brackets_are_valid(self, metric):
        match_all_but_brackets = "[^\[|^\(|^\{|^\]|^\}|^\)]"
        bracketsString = re.sub(match_all_but_brackets, "", metric)
        O = ['{','(','[']
        C = ['}',')',']']
        D = {')':'(','}':'{',']':'['}
        s = Stack()
        for i in bracketsString:
            if i in O:
                s.push(i)
            elif i in C and len(s) != 0:
                if D[i] == s.peek():
                    s.pop()
                else:
                    s.push(i)
            elif i in C and len(s) == 0:
                s.push(i)
        if metric == "":
            return metric
        elif metric and not bool(len(s) == 0):
            raise ValueError("The brackets you have entered for your metric are not balanced.")
        else:
            return metric
    
    def _remove_unwanted_commas(self, metric):
        anythinginoutermost = "\([^\(\)]*\)"
        match_all_but_brackets_and_commas = "[^\[|^\]|^\,]"
        string = metric
        while len([x for x in re.finditer(anythinginoutermost, string)]):
            string = re.sub(anythinginoutermost,'', string)
        return re.sub(match_all_but_brackets_and_commas,'', string)
    
    def _words_in_metric_are_valid(self, metric):
        ListOfSpecialWords = Constants["All_Valid_Words"]
        pattern0 = "[a-zA-Z][a-zA-Z]+"
        lis = [x for x in re.finditer(pattern0, metric)]
        unrecognizedValues = []
        for i in lis:
            if i.group() not in ListOfSpecialWords:
                unrecognizedValues.append(i.group())
        if len(unrecognizedValues) != 0:
            strin = ''
            for i in unrecognizedValues:
                strin = strin + " " + i + ","
            raise ValueError("Value(s)" + strin + " not recognized.")
        else:
            return metric
    
    def _metric_format_is_valid(self, metric):
        if self.Basis:
            metric_without_unwanted_commas = self._remove_unwanted_commas(metric)
            dim = self.Dimention
            pattern0 = "\[(\[(\,){" + str(dim-1) +  "}\]\,){" + str(dim-1) +  "}(\[(\,){" + str(dim-1) +  "}\])\]"
            if not bool(re.search(pattern0, metric_without_unwanted_commas)):
                raise ValueError("The format you have entered for your metric is not valid w.r.t the basis you entered.")
            else:
                return metric
        else:
            return metric

    def _is_valid_metric(self, metric):
        if metric and self.Basis:
            Validation1 = self._metric_brackets_are_valid(metric)
            Validation2 = self._metric_format_is_valid(Validation1)
            Validation3 = self._words_in_metric_are_valid(Validation2)
            return Validation3
        else:
            return metric


class StringParser:
    def __init__(self, StringExpression):
        self.StringExpression = StringExpression
    
    def Functions(self):
        Function = "(?<![a-zA-Z])[a-zA-Z](?=\()"
        RemoveSpaces = self.StringExpression.replace(' ', '')
        FunctionList = []
        List = []
        FunctionList = [x for x in re.finditer(Function, RemoveSpaces)]
        for i in FunctionList:
            List.append(i.group())
        return list(dict.fromkeys(List))
            
    
    def symbolRecognizer(self, Input):
        GreekSymbols = "(theta|phi|omega|sigma|alpha|beta|gamma|epsilon|zeta|eta|kappa|lambda|mu|nu|pi|Theta|Phi|Omega|Sigma|Alpha|Beta|Gamma|Epsilon|Zeta|Eta|Kappa|Lambda|Mu|Nu|Pi)"
        RemoveSpaces = Input.replace(' ', '')
        ListOne = []
        ListOne = [x for x in re.finditer("(?<![a-zA-Z])[a-zA-Z](?![a-zA-Z])", RemoveSpaces)]
        ListTwo = [x for x in re.finditer(GreekSymbols, RemoveSpaces)]

        for i in ListTwo:
            ListOne.append(i)
        return ListOne

    def preDefinedFunctionRecognizer(self):
        SpecialFunctions = ['(sin)', '(cos)', '(tan)', '(sinh)', '(cosh)', '(tanh)', '(asin)', '(atan)', '(acos)', '(asinh)', '(acosh)', '(atanh)', '(exp)', '(pi)']
        RemoveSpaces = self.StringExpression.replace(' ', '')
        ListOfFunctions = []
        for i in SpecialFunctions:
            if [x for x in re.finditer(i, RemoveSpaces)] != []:
                ListOfFunctions.append([x for x in re.finditer(i, RemoveSpaces)])
        return ListOfFunctions

    #symbolRecognizer(Input)[1].group() = "F"
    #symbolRecognizer(Input)[1].span() = (17,18)

    def replacer(self, Input, Replace, Location):
        NewString = Input.replace(' ', '')
        return NewString[:Location[0]] + Replace + NewString[Location[1]:]

    #replacer(Input, 'Q[1]', symbolRecognizer(Input)[1].span())

    def returnLists(self):
        AllSymbolsList = []
        VariableList = []
        FunctionList = []
        
        for i in range(len(self.symbolRecognizer(self.StringExpression))):
            AllSymbolsList.append(self.symbolRecognizer(self.StringExpression)[i].group())
        NoDuplicatesAllSymbolsList = list(dict.fromkeys(AllSymbolsList))
        
        for i in NoDuplicatesAllSymbolsList:
            if i not in self.Functions():
                VariableList.append(i)
            else:
                FunctionList.append(i)

        return [VariableList,FunctionList,AllSymbolsList]

    def returnDictionary(self):
        VariableList = self.returnLists()[0]
        FunctionList = self.returnLists()[1]
        Dic = {}
        if len(VariableList) == 1 and len(FunctionList) == 1:
            for i in range(len(VariableList)):
                Dic.update({VariableList[i] : 'W'.format(i)})
            for i in range(len(FunctionList)):
                Dic.update({FunctionList[i] : 'Q'.format(i)})
        elif len(VariableList) == 1 and len(FunctionList) == 0:
            for i in range(len(VariableList)):
                Dic.update({VariableList[i] : 'W'.format(i)})
        elif len(VariableList) > 1 and len(FunctionList) == 0:
            for i in range(len(VariableList)):
                Dic.update({VariableList[i] : 'W[{}]'.format(i)})
        elif len(VariableList) > 1 and len(FunctionList) > 1:
            for i in range(len(VariableList)):
                Dic.update({VariableList[i] : 'W[{}]'.format(i)})
            for i in range(len(FunctionList)):
                Dic.update({FunctionList[i] : 'Q[{}]'.format(i)})
        elif len(VariableList) == 1 and len(FunctionList) > 1:
            for i in range(len(VariableList)):
                Dic.update({VariableList[i] : 'W'.format(i)})
            for i in range(len(FunctionList)):
                Dic.update({FunctionList[i] : 'Q[{}]'.format(i)})
        elif len(FunctionList) > 1 and len(VariableList) == 1:
            for i in range(len(FunctionList)):
                Dic.update({FunctionList[i] : 'Q[{}]'.format(i)})
            for i in range(len(FunctionList)):
                Dic.update({FunctionList[i] : 'Q'.format(i)})
        elif len(FunctionList) == 1 and len(VariableList) > 1:
            for i in range(len(FunctionList)):
                Dic.update({FunctionList[i] : 'Q'.format(i)})
            for i in range(len(VariableList)):
                Dic.update({VariableList[i] : 'W[{}]'.format(i)})
        return Dic

    def returnSympyString(self):
        New = self.StringExpression
        for i in range(len(self.symbolRecognizer(self.StringExpression))):
            New = self.replacer(New,self.returnDictionary()[self.symbolRecognizer(New)[i].group()], self.symbolRecognizer(New)[i].span())
        return New



class SympyParser:
    def __init__(self, equationString):
        self.equationString = equationString

    # This will convert a list of variables and convert them into one string, in the same order of the List, 
    # so that sympy can parse the string to sympy objects.
    # Input: List = ['x', 'y', 'z']
    # Output: String = 'x y z '
    def convertListToSympyVariableString(self, stringList):
        varableList = []
        for string in stringList:
            varableList.append(string.replace(' ',''))
        variable = ''
        for i in range(len(varableList)):
            variable += varableList[i] + ' '
        return variable
   
    def convertToSympyObject(self):
        VariableSymbolsList = StringParser(self.equationString).returnLists()[0]
        FunctionSymbolList = StringParser(self.equationString).returnLists()[1]
        FunctionSymbols = self.convertListToSympyVariableString(FunctionSymbolList)
        VariableSymbols = self.convertListToSympyVariableString(VariableSymbolsList)
        
        if int(len(StringParser(self.equationString).returnLists()[0])) == 0:
            return smp.symbols(StringParser(self.equationString).returnSympyString())
            #return eval(StringParser(self.equationString, self.functionList).returnSympyString())
        elif int(len(StringParser(self.equationString).returnLists()[1])) == 0:
            W = smp.symbols(VariableSymbols)
            return eval(StringParser(self.equationString).returnSympyString())
        elif int(len(StringParser(self.equationString).returnLists()[1])) >= 1:
            W = smp.symbols(VariableSymbols)
            Q = smp.symbols(FunctionSymbols, cls = smp.Function)
            return eval(StringParser(self.equationString).returnSympyString())