#!/usr/bin/env python2
from CSVToCFG import CSV2CFG
from sourceutils.codeTree.CodeTreeWalker import CodeTreeWalker

def extractCSVCFGs(projectRoot):

    codeTreeWalker = CodeTreeWalker(projectRoot)
    codeTreeWalker.setFilenameFilterRegex('(.*)\.(csv)$')
       
    for metaDataFile in codeTreeWalker:
        # print metaDataFile
        processor = CSV2CFG()
        processor.processCSVRows(metaDataFile)
        processor.terminateFunction()
    
def main(projectRoot):
    print("Creating PythonCFGs for " + projectRoot)
    extractCSVCFGs(projectRoot)

if __name__ == '__main__':
    import sys
    main(sys.argv[1])