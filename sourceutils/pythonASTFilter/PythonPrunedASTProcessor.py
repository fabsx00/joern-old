import pickle

class PythonPrunedASTProcessor():
    def __init__(self):
        self.currentFile = None
    
    def process(self, treefilename):
        self.loadTreeFromFile(treefilename)
        self.handlePrunedTree()
    
    def loadTreeFromFile(self, treefilename):

        self.currentFile = self._treefileToSourceFile(treefilename)
        self.tree = pickle.load(open(treefilename, "rb"))   
        self.functionId = treefilename
    
    def _treefileToSourceFile(self, treefile):
        return ('/'.join(treefile.split('/')[:-2]))
    
    # overload this
    def handlePrunedTree(self):
        pass
    
        