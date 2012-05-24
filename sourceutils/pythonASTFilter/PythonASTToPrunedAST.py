import os, pickle
from sourceutils.pythonASTs.PythonASTProcessor import PythonASTProcessor

class PythonASTToPrunedAST(PythonASTProcessor):
    def __init__(self):
        PythonASTProcessor.__init__(self)
        
        self.handlers['func'] = self.handleFunction
        self.filter = None
    
    def setFilter(self, f):
        self.filter = f

    def setRow2StringConverter(self, row2StringConverter):
        self.filter.setRow2StringConverter(row2StringConverter)
        
    def handleFunction(self, node):
        self._setFunctionRow(node)
        prunedTree = self._pruneTree(node)
        self.handlePrunedTree(prunedTree)
        return False
    
    def _setFunctionRow(self, node):
        self.functionRow = ','.join(node.row)
        self.functionRow += ',' + self.currentFile
    
    def _pruneTree(self, node):
        if not self.filter: return node
        return self.filter.prune(node)
    
    def handlePrunedTree(self, node):       
        self.dumpTree(node)
        
    def dumpTree(self, node):
        csvRow = self.functionRow.split(',')
        functionName = csvRow[5]
        pos = csvRow[1]
        
        outputDir = self.currentFile
        outputDir += '/' + functionName + '_' + pos.replace(':', '_')
        
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        
        outputFilename = outputDir + '/prunedAst.pickl'
        pickle.dump(node, open(outputFilename, 'wb'))
        