import pickle

class NameToDictMap():
    def __init__(self):
        self.d = dict()
    
    def add(self, itemToAdd, name):
        if not name in self.d:
            self.d[name] = dict()
        
        if not itemToAdd in self.d[name]:
            self.d[name][itemToAdd] = 1
        else:
            self.d[name][itemToAdd] += 1
    
    def getNumberOfEntries(self):
        return len(self.d.keys())
    
    def save(self, filename):
        pickle.dump(self, open(filename, 'wb'), protocol=2)
    