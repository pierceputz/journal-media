import re
from datetime import date
from pathlib import Path
from zim.parsing import parse_date      #requires access to zim-wiki


class Journal():
    '''An entire journal of entries'''
    
    def __init__(self, path):
        '''store path and recurse for entries if applicable'''
        self.path = Path(path)
        self.logs = [ Log(child) for child in 
                      self.path.rglob('*.txt') ]

class Log():
    '''a zim-wiki journal log (considered a collection of entries)'''
    
    def __init__(self, path):
        '''import a full journal from the top-level recursively'''
        
        self.metadata, self.contents = str(), str()
        self.entries = []
        with open(path, 'r') as f:
            for n, line in enumerate(f):
                if n < 3: 
                    self.metadata += line
                    continue
                self.contents += line

class Entry():
    '''an entry created from a log file'''
    
    def __init__(self, log):
        pass
    
    def addMediaReference(self, link):
        pass

class Media():
    '''a media file'''
    
    def __init__(self, date, path):
        self.date, self.path = date, path

if __name__ == "__main__":
    pass
