import pickle
from sourceutils.pythonASTs.PythonASTTreeNode import PythonASTTreeNode #@UnusedImport

                
class PythonASTProcessor():
    def __init__(self):
        
        self.handlers = dict()
        self.currentFile = None
        
    def loadTreeFromFile(self, treefilename):

        self.currentFile = self._treefileToSourceFile(treefilename)
        self.tree = pickle.load(open(treefilename, "rb"))
    
    def _treefileToSourceFile(self, treefile):
        return ('/'.join(treefile.split('/')[:-1]))
    
    def processTree(self, node):
        
        traverseChildren = self._callHandlers(node)
        if traverseChildren:
            self.processChildren(node)

    def processChildren(self, node = None):
        if node == None:
            node = self.tree
        
        for child in node.children:
            self.processTree(child)

    def _callHandlers(self, node):
        nodeType = node.row[0]
        if nodeType in self.handlers:
            handler = self.handlers[nodeType]
            return handler(node)

