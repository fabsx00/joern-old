import os, re

class CodeTreeWalker:
  
    def __init__(self, projectRoot):
        self.projectRoot = projectRoot
    
    def setFilenameFilterRegex(self, r):
        self.filterRegex = re.compile(r)
        
    def __iter__(self):
        for (dirpath, unused_dirnames, filenames) in os.walk(self.projectRoot):
            for name in filenames:
                if not self.isOfInterest(name): continue
                absoluteName = dirpath + '/' + name
                yield absoluteName
        
    def getDirForFilename(self, filename):
        return '/'.join(filename.split('/')[:-1])

    def isOfInterest(self, filename):
        return self.filterRegex.match(filename)
    