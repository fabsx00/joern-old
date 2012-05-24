from sourceutils.csvASTs.CSVProcessor import CSVProcessor
from sourceutils.misc.NameToListMap import NameToListMap

class CodeIndexCreator(CSVProcessor):
    def __init__(self):
        CSVProcessor.__init__(self)
        
        self.functionIndex = NameToListMap()
        self.callIndex = NameToListMap()
        self.declarationIndex = NameToListMap()
        self.conditionIndex = NameToListMap()
        
        # self.typeIndex = dict()
        
        self.handlers['func'] = self.functionHandler
        self.handlers['call'] = self.callHandler
        self.handlers['decl'] = self.declHandler
        self.handlers['cond'] = self.condHandler
    
    def registerFunction(self, row):
        functionName = row[5]
        self.currentFunctionName = functionName
        self.functionIndex.add((row, self.currentFile), functionName)
        
    def registerCall(self, row):
        callDstName = row[4]
        self.callIndex.add((row, self.currentFile), callDstName)
    
    def registerDecl(self, row):
        typeName = row[4]
        self.declarationIndex.add((row, self.currentFile), typeName)
    
    def registerCond(self, row):
        cond = row[4]
        self.conditionIndex.add((row, self.currentFile), cond)
    
    def functionHandler(self, row):
        self.registerFunction(row)
    
    def callHandler(self, row):
        self.registerCall(row)
        
    def declHandler(self, row):
        self.registerDecl(row)
    
    def condHandler(self, row):
        self.registerCond(row)
    
    def saveResults(self, projectRoot):
        if projectRoot[-1] == '/': projectRoot = projectRoot[:-1]
        outputDir = projectRoot + '/'
        self.functionIndex.save(outputDir + 'functionIndex.pickl')
        self.callIndex.save(outputDir + 'callIndex.pickl')
        self.declarationIndex.save(outputDir + 'declarationIndex.pickl')
        self.conditionIndex.save(outputDir + 'conditionIndex.pickl')
        