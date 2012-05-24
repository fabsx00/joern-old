#!/usr/bin/env python2
from sourceutils.codeTree.CodeTreeWalker import CodeTreeWalker
from CSVToPythonAST import CSVToPythonAST

import sys

def usage():
    print('usage: %s <codeTreeRoot>' % (sys.argv[0]))

def outFilenameFromCSVFilename(csvFilename):
    outputFilename = '/'.join(csvFilename.split('/')[:-1])
    outputFilename += '/' + 'ast.pickl'
    return outputFilename
        
def main(projectRoot):
   
    print('Creating pickle\'d ASTs for %s' %(projectRoot))
    
    codeTreeWalker = CodeTreeWalker(projectRoot)
    codeTreeWalker.setFilenameFilterRegex('ast\.(csv)$')
   
    for csvFilename in codeTreeWalker:
        
        processor = CSVToPythonAST()
        processor.processCSVRows(csvFilename)
        outputFilename = outFilenameFromCSVFilename(csvFilename)
        processor.saveResults(outputFilename)
    
if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        usage()
        sys.exit()
    
    projectRoot = sys.argv[1]    
    main(projectRoot)
    