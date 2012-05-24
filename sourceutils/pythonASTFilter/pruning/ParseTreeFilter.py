
from sourceutils.pythonASTs.PythonASTTreeNode import PythonASTTreeNode

PRUNED = 'pruned'
prunedRow = [PRUNED, '(*)', '(*)', '(*)', '']

class ParseTreeFilter():
    def __init__(self):       
        self.nodeTypesOfInterest = list()
        self.keepNodesOfInterest = True
    
    def setNodeTypesOfInterest(self, l):
        self.nodeTypesOfInterest = l
    
    def setRow2StringConverter(self, r):
        self.row2StringConverter = r
    
    def prune(self, node):    
        if self._mustPruneNode(node):
            r = prunedRow
        else:
            r = node.row
        
        rf = self.row2StringConverter.convert(r)
        
        newRootNode = PythonASTTreeNode(rf)
        self.addPrunedChildren(node, newRootNode)
        return newRootNode
    
    def addPrunedChildren(self, node, root):
        for child in node.children:
            self._attachPruned(child, root)
    
    def _pruneNode(self, node, root):
        # If a leaf is to be pruned, discard it altogether
        if len(node.children) == 0: return
        newNode = PythonASTTreeNode(prunedRow)
        self.addPrunedChildren(node, newNode)
        if len(newNode.children) == 0: return
        root.appendChild(newNode)
    
    def _mustPruneNode(self, node):
        nodeType = node.row[0]
        if (len(self.nodeTypesOfInterest) == 0): return False
        if self.keepNodesOfInterest and (nodeType in self.nodeTypesOfInterest): return False
        if (not self.keepNodesOfInterest) and (not(nodeType in self.nodeTypesOfInterest)): return False 
        return True
    
    def _attachPruned(self, node, root):
        
        if self._mustPruneNode(node):
            self._pruneNode(node, root)
        else:
            newNode = PythonASTTreeNode(self.row2StringConverter.convert(node.row))
            self.addPrunedChildren(node, newNode)
            root.appendChild(newNode)
        