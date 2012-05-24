#!/usr/bin/env python2

from CodeTree import CodeTree
import sys

def usage():
    print('usage: %s <sourceCodeRoot>' % (sys.argv[0]))

def main(projectRoot):
   
    print('Creating CodeTree for %s' %(projectRoot))
    codeTree = CodeTree()
    codeTree.create(projectRoot)
    return codeTree

if __name__ == '__main__':
    
    if len(sys.argv) != 2:
        usage()
        sys.exit()
    
    projectRoot = sys.argv[1]    
    main(projectRoot)
    