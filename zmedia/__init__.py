from datetime import date
from pathlib import Path

class Journal():
    '''An entire journal of entries'''
    
    def __init__(self, path):
        '''store path and recurse for entries if applicable'''
        self.path = Path(path)
        self.entries = [ Entry(child) for child in 
                         self.path.rglob('*.txt') ]

class Media():
    '''a media file'''
    
    def __init__(self, date, path):
        self.date, self.path = date, path

class Entry():
    '''a zim-wiki journal entry'''
    
    def __init__(self, path):
        '''import a full journal from the top-level recursively'''
        self.metadata, self.contents = str(), str()
        
        with open(path, 'r') as f:
            for n, line in enumerate(f):
                if n < 3: self.metadata += line
                else: self.contents += line

if __name__ == "__main__":
    pass
