from datetime import date
from pathlib import Path

class Journal():
    '''An entire journal of entries'''
    
    def __init__(self, entries=[], path=Path()):
        self.entries, self.path = entries, path

class Media():
    '''a media file'''
    
    def __init__(self, date, path):
        self.date, self.path = date, path

class Entry():
    '''a journal entry'''
    
    def __init__(self, date, contents, media_dir):
        #more work to be done
        pass

if __name__ == "__main__":
    pass
