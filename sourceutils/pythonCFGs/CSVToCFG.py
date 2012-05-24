import pickle, os

from sourceutils.csvASTs.CSVProcessor import CSVProcessor
from sourceutils.csvASTs.CSVRowAccessors import getCSVRowType, getCSVRowLevel
from sourceutils.pythonCFGs.CFG import CFG, BasicBlock

labelNode = 'label'
returnNode = 'return'
breakNode = 'break'
continueNode = 'continue'
gotoNode = 'goto'
breakOrContinue = set([breakNode, continueNode])
controlStatementNodes = set([returnNode, gotoNode]) | breakOrContinue
ifNode = 'if'
conditionNode = 'cond'
switchNode = 'switch'
elseNode = 'else'
doNode = 'do'
loopNodes = set(['for', 'while', doNode])
scopeIncreaseNodes = set([ifNode, switchNode, conditionNode, elseNode]) | loopNodes

class CSV2CFG(CSVProcessor):
    
    def __init__(self):
        CSVProcessor.__init__(self)
        self.currentCFG = None
        self.resetStacks() 
        self.defaultHandler = self.handleNode
        self.functionLevel = -1
    
    def resetStacks(self):
        self.scopeStack = []
        self.returnStack = []
        self.breakContinueStack = []
        self.ifBodyStack = []
        self.gotoList = []
        
    def _initCFG(self, row):
        self.currentCFG = CFG()
        self.currentCFG.addNode(BasicBlock(row))
        self.currentLevel = int(getCSVRowLevel(row)) + 1
        self.functionLevel = self.currentLevel - 1
        self.functionName = row[5]
        self.functionPos = row[1]
        self.resetStacks()    
    
    def handleNode(self, row):
        lineType = getCSVRowType(row)
        if self._isInFunction():
            self.handleNodeInFunction(row)
        else:
            if lineType == 'func':
                self._initCFG(row)
    
    def handleNodeInFunction(self, row):
        level = int(getCSVRowLevel(row))
        
        if self.isInScope(level):
            self.handleNodeInScope(row, level)
        else:
            self.leaveScope(row, level)
    
    def handleNodeInScope(self, row, level):
        
        if self.isScopeIncreaseNode(row):
            self.handleScopeIncreaseNode(row, level)
        elif self.isControlStatementNode(row):
            self.handleControlStatement(row, level)
        elif self.isLabelNode(row):
            self.handleLabelNode(row, level)
        else:
            self.defaultNodeHandler(row, level)
    
    def isInScope(self, level):
        return level >= self.getCurrentLevel()
    
    def isScopeIncreaseNode(self, row):
        return getCSVRowType(row) in scopeIncreaseNodes

    def isControlStatementNode(self, row):
        return getCSVRowType(row) in controlStatementNodes

    def isLabelNode(self, row):
        return getCSVRowType(row) == labelNode
    
    # loops, if, else, switch
    
    def handleScopeIncreaseNode(self, row, level):
        
        currentNodeId = self.currentCFG.getCurrentNodeId()
        nodeType = getCSVRowType(row)
        currentNode = self.currentCFG.getNodeById(currentNodeId)
        
        if nodeType == elseNode:
            self.handleElseNode(currentNodeId, row)
            return
        
        if currentNode.rows != [] and nodeType != conditionNode:
            self.createAndConnectNode(row)
        else:
            self.currentCFG.appendToLatestNode(row)
        
        self.enterScope(row)
    
    def getCondition(self, predNodeId):
        predNode = self.currentCFG.getNodeById(predNodeId)
        return predNode.getCondition()
        
    
    def handleElseNode(self, currentNodeId, row):
        (predNodeId, unused1, predNodeLevel) = self.scopeStack[-1]
        
        conditionStr = self.getCondition(predNodeId)
        conditionStr += ' == False'
        
        self.currentCFG.addEdge(predNodeId, currentNodeId + 1, conditionStr)
        self.currentCFG.addNode(BasicBlock(row))
        self.ifBodyStack.append((currentNodeId, predNodeLevel))
        self.enterScope(row)
    
    def createAndConnectNode(self, row = None, conditionStr=None):
        newBasicBlock = BasicBlock(row)
        if row: newBasicBlock.blockType = row[0]
        newNodeId = self.currentCFG.addNode(newBasicBlock)
        self.currentCFG.addEdge(newNodeId - 1, newNodeId, conditionStr)
    
    def enterScope(self, row):
        # TODO: simplify: just push nodeId and row
        currentNodeId = self.currentCFG.getCurrentNodeId()
        level = int(getCSVRowLevel(row))
        nodeType = getCSVRowType(row)
        self.scopeStack.append((currentNodeId, nodeType, level))
        self.currentLevel = level + 1
        # print 'enter scope: %s'  % (self.scopeStack)

    def handleControlStatement(self, row, level):
        currentNodeId = self.currentCFG.getCurrentNodeId()
        rowType = getCSVRowType(row)
        
        if rowType == returnNode:
            self.returnStack.append(currentNodeId)
        elif rowType in breakOrContinue:
            self.breakContinueStack.append((currentNodeId, rowType, level))
        elif rowType == gotoNode:
            self.gotoList.append((currentNodeId, row))
        
        self.currentCFG.appendToLatestNode(row)
    
    def handleLabelNode(self, row, level):
        currentNodeId = self.currentCFG.getCurrentNodeId()
        currentNode = self.currentCFG.getNodeById(currentNodeId)
        
        if currentNode.rows != []:
            self.currentCFG.addNode(BasicBlock(row))
            
            currentNodeId = self.currentCFG.getCurrentNodeId()
            
            previousNode = self.currentCFG.getNodeById(currentNodeId -1)
            lastInstrType = previousNode.getLastInstrType()
            if not lastInstrType in controlStatementNodes:
                self.currentCFG.addEdge(currentNodeId -1, currentNodeId)
        else:
            self.currentCFG.appendToLatestNode(row)
        
        self.currentCFG.labeledNodes.append((currentNodeId,row))
        
    def defaultNodeHandler(self, row, level):   
        self.currentCFG.appendToLatestNode(row)
    
    #####
    
    def connectPredicateToExitNode(self, predicateNodeId):
        conditionStr = self.getCondition(predicateNodeId)
        conditionStr += ' == False'
        self.currentCFG.addEdge(predicateNodeId,
                                self.currentCFG.getCurrentNodeId(),
                                conditionStr)
        
    def onCFGFinished(self):
           
        labelDict = self._genLabelDict()
        
        for (nodeId, row) in self.gotoList:
            dstLabel = row[4].strip()
            self.currentCFG.removeEdgesFrom(nodeId)
            
            if not labelDict.has_key(dstLabel):
                print 'can\'t resolve label : ' + dstLabel
                continue
            
            dstNodeId = labelDict[dstLabel]
            self.currentCFG.addEdge(nodeId, dstNodeId)
        
        self.createAndConnectNode()
        exitNodeId = self.currentCFG.getCurrentNodeId()
        for nodeId in self.returnStack:
            self.currentCFG.removeEdge(nodeId, nodeId + 1)
            self.currentCFG.addEdge(nodeId, exitNodeId)
        
        self.currentCFG.registerSuccessors()
        
        
         
    def _genLabelDict(self):
        d = dict()
        for (nodeId, row) in self.currentCFG.labeledNodes:
            label = row[4][:-1].strip()
            d[label] = nodeId
        return d
    
    
    def leaveScope(self, row, level):
    
        while level < self.currentLevel:
            
            if self.scopeStack == []:
                if level > self.functionLevel:
                    print 'Error: scopeStack empty but level > functionLevel: %d > %d' % (level, self.functionLevel)
                self.onCFGFinished()
                self.outputAndReset()
                self.currentLevel = -1
                if row[0] == 'func':
                    self._initCFG(row)
                return
            
            previousLevel = self.currentLevel
            (predicateNodeId, predicateNodeType) = self.exitScope()
        
            if self.leavingIfScope(predicateNodeType):
                self.leaveIfScope(previousLevel, predicateNodeId)
            elif self.leavingSwitchScope(predicateNodeType):
                self.leaveSwitchScope(predicateNodeId)
            elif self.leavingConditionScope(predicateNodeType):
                conditionStr = self.getCondition(predicateNodeId)
                conditionStr += ' == True'
                self.createAndConnectNode(None, conditionStr)
              
            if predicateNodeType in (loopNodes | set([switchNode])):
                self.leaveLoopOrSwitch(predicateNodeType, predicateNodeId)
                
        # Now all scopes, which were closed by this row are closed.
        self.handleNodeInScope(row, level)


    def leaveIfScope(self, previousLevel, predicateNodeId):
        self.createAndConnectNode()
        exitNodeId = self.currentCFG.getCurrentNodeId()
                
        if self.ifBodyStack != []:
            (ifBodyId, ifBodyLevel) = self.ifBodyStack.pop()
           
            if ifBodyLevel != previousLevel -1:
                self.ifBodyStack.append((ifBodyId, ifBodyLevel))
                self.connectPredicateToExitNode(predicateNodeId)
            else:
                self.currentCFG.addEdge(ifBodyId, exitNodeId)
        else:
            self.connectPredicateToExitNode(predicateNodeId)

    def leaveSwitchScope(self, predicateNodeId):
        self.createAndConnectNode()
               
        labeledNodesCopy = self.currentCFG.labeledNodes[:]
        
        while labeledNodesCopy != []:
            (labelNodeId, labelRow) = labeledNodesCopy.pop()
            labelLevel = int(getCSVRowLevel(labelRow))
            if labelLevel <= self.getCurrentLevel():
                break
            conditionStr = self.getCondition(predicateNodeId)
            conditionStr += ' == ' + labelRow[4]
            self.currentCFG.addEdge(predicateNodeId, labelNodeId, conditionStr)

    def leaveLoopOrSwitch(self, predicateNodeType, predicateNodeId):
        if predicateNodeType == doNode:
            exitNodeId = self.leaveDoScope(predicateNodeId)
        elif predicateNodeType == switchNode:
            exitNodeId = self.currentCFG.getCurrentNodeId()
        else:
            self.currentCFG.addNode(BasicBlock(None))
            exitNodeId = self.currentCFG.getCurrentNodeId()
            conditionStr = self.getCondition(predicateNodeId) + ' == False'
            self.currentCFG.addEdge(predicateNodeId, exitNodeId, conditionStr)
            self.currentCFG.addEdge(exitNodeId - 1, predicateNodeId)
            
        self.attachBreakAndContinueNodes(exitNodeId, predicateNodeId)


    
    def leaveDoScope(self, predicateNodeId):
        self.createAndConnectNode()
        condNodeId = self.currentCFG.getCurrentNodeId()
        
        conditionStr1 = self.getCondition(predicateNodeId)
        
        conditionStr = conditionStr1 + ' == False'
        self.createAndConnectNode(None, conditionStr)
        exitNodeId = self.currentCFG.getCurrentNodeId()
        
        conditionStr = conditionStr1 + ' == True'
        self.currentCFG.addEdge(condNodeId, predicateNodeId, conditionStr)
        
        self.currentCFG.removeEdgesFrom(predicateNodeId)
        self.currentCFG.addEdge(predicateNodeId, predicateNodeId + 1)
        
        predicateNode = self.currentCFG.getNodeById(predicateNodeId)
        condition = predicateNode.rows[:]
        predicateNode.rows = []
        
        self.currentCFG.getNodeById(condNodeId).rows.extend(condition)
        
        predicateNode.blockType = 'do'
        
        return exitNodeId      
    
    
    def attachBreakAndContinueNodes(self, currentNodeId, predicateNodeId):
        
        while self.breakContinueStack != []:
            (breakNodeId, breakNodeType, breakNodeLevel) = self.breakContinueStack.pop()
            if breakNodeLevel <= self.currentLevel:
                self.breakContinueStack.append((breakNodeId, breakNodeType, breakNodeLevel))
                break
            
            self.currentCFG.removeEdge(breakNodeId, breakNodeId + 1)
            
            if breakNodeType == breakNode:
                self.currentCFG.addEdge(breakNodeId, currentNodeId)
            elif breakNodeType == continueNode:
                self.currentCFG.addEdge(breakNodeId, predicateNodeId)
                
  
    def exitScope(self):
        (predicateNodeId, predicateNodeType, unusedNodeLevel) = self.scopeStack.pop()
        
        self.adjustIfBodyStack()
        
        try:
            self.currentLevel = self.scopeStack[-1][2] + 1
        except:
            self.currentLevel = self.functionLevel + 1
        
        # print 'exitScope %s %d' %(self.scopeStack, self.currentLevel)
        return (predicateNodeId, predicateNodeType)
        
    def terminateFunction(self):
        row = ['exitNode', '0:0', '0:0', '%d' % (self.functionLevel)]
        self.handleNode(row)
                
    def _isInFunction(self):
        return self.currentCFG != None
    
    def _resetCFG(self):
        self.currentCFG = None
        self.functionLevel = -1
        
    def outputAndReset(self):
        self.save()
        self._resetCFG()
   
    def leavingScope(self, level):
        return (level < self.getCurrentLevel())

    def leavingConditionScope(self, predicateNodeType):
        return (predicateNodeType == conditionNode)

    def leavingElseScope(self, predicateNodeType):
        return (predicateNodeType == elseNode)
    
    def leavingIfScope(self, predicateNodeType):
        return (predicateNodeType == ifNode)
    
    def leavingSwitchScope(self, predicatedNodeType):
        return (predicatedNodeType == switchNode)
    
    def enteringElseScope(self, currentNodeType):
        return (currentNodeType == elseNode)
    
    def getCurrentLevel(self):
        return self.currentLevel
    
    def adjustIfBodyStack(self):
        self.ifBodyStack = [i for i in self.ifBodyStack if i[1] <= self.currentLevel]
    
    def save(self):
        
        outputDir = '/'.join(self.currentFile. split('/')[:-1])
        outputDir += '/' + self.functionName + '_' + self.functionPos.replace(':', '_')
        if not os.path.exists(outputDir):
            os.mkdir(outputDir)
        outputFilename = outputDir + '/cfg.pickle'
        
        f = open(outputFilename, 'wb')
        pickle.dump(self.currentCFG, f)
        f.close()
        