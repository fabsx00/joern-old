import pickle
from sourceutils.pythonCFGs.CFG import CFG #@UnusedImport

class PythonCFGToPrunedCFG():
    
    def __init__(self):
        pass

    def setFilter(self, f):
        self.filter = f
    
    def setRow2StringConverter(self, r):
        self.filter.setRow2StringConverter(r)
    
    def applyFilterToNodes(self, cfgFilename):
        self.cfgFilename = cfgFilename
        cfg = self._loadCfg(cfgFilename)
        self.prunedCfg = self.filter.prune(cfg)
                
    def _loadCfg(self, cfgFilename):
        return pickle.load(file(cfgFilename, 'rb'))
    
    def cfgFilenameToPrunedFilename(self, cfgFilename):
        return '/'.join(cfgFilename.split('/')[:-1]) + '/' + 'prunedCfg.pickl'
    
    def save(self):
        prunedCfgFilename = self.cfgFilenameToPrunedFilename(self.cfgFilename)
        pickle.dump(self.prunedCfg, file(prunedCfgFilename, 'wb'))