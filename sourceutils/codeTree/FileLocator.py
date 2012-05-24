"""
FileLocator: Recursively locates all files in a directory where
the filename matches the supplied regular expression
"""

import os, re

class FileLocator:
    def __init__(self, sourceDirectory, regex):

        self.regex = re.compile(regex)

        if not os.path.exists(sourceDirectory):
            raise RuntimeError("%s does not exist" %(sourceDirectory))

        if sourceDirectory[-1] == '/':
            sourceDirectory = sourceDirectory[:-1]

        self.sourceDirectory = sourceDirectory
        self.initializeMembers()

    def initializeMembers(self):
        self.filesFound = list()

    def findFiles(self):

        for dirname, unused, files in os.walk(self.sourceDirectory, topdown=False):
            names = [dirname + '/' + name
                     for name in files if self.regex.match(name)]
            self.filesFound.extend(names)
        return self.filesFound

