import pickle

from sourceutils.csvASTs.CSVProcessor import CSVProcessor
from sourceutils.csvASTs.CSVRowAccessors import getCSVRowLevel
from sourceutils.pythonASTs.PythonASTTreeNode import PythonASTTreeNode


class CSVToPythonAST(CSVProcessor):
    def __init__(self):
        CSVProcessor.__init__(self)
        
        self.rootNode = PythonASTTreeNode(None)
        self.parentStack = []
        self.previousNode = self.rootNode
        
        self.defaultHandler = self.handleNode
    
    def handleNode(self, row):
        
        newNode = PythonASTTreeNode(row)
        
        # code below fails if level ever
        # increases by more than one at once
        level = int(getCSVRowLevel(row))
        if level > len(self.parentStack) - 1:
            # moved down one level, push previous node
            self.parentStack.append(self.previousNode)
        elif level < len(self.parentStack) -1:
            while(level < len(self.parentStack) - 1):
                self.parentStack.pop()
        else:
            # stayed on a level, no need to adjust parentStack
            pass
                
        parentNode = self.parentStack[-1]
        parentNode.appendChild(newNode)
        
        self.previousNode = newNode
    
    def prettyPrintTree(self):
        numberOfTabs = 0
        self._prettyPrintTree(self.rootNode, numberOfTabs)
    
    def _prettyPrintTree(self, node, numberOfTabs):
        outString = '\t'*numberOfTabs
        outString += str(node.row)
        print(outString)
        for child in node.children:
            self._prettyPrintTree(child, numberOfTabs + 1)
    
    def saveResults(self, filename):
        pickle.dump(self.rootNode, open(filename, 'wb'))


