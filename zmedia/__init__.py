import re
from datetime import date
from pathlib import Path
from zim.parsing import parse_date      #requires access to zim-wiki
import logging

logging.basicConfig(level=logging.DEBUG)

#work in progress, might be worthless
re_entry = re.compile(r"={2,6} \d+.\d+.\d+ ={2,6}\nLog:[\w:* \t\n]*")

# easier to roll my own here than import from zim.formats.wiki
def is_heading(header):
    '''Parse heading and determine it's level'''
    
    try:
        assert header.startswith('=')
        assert header.endswith('\n')
    except AssertionError:
        return False
    
    contents = header.split(' ')
    if contents[0] != contents[2].strip():
        return False
    
    return True

class Journal():
    '''An entire journal of entries'''
    
    def __init__(self, path):
        '''store path and recurse for entries if applicable'''
        
        logging.debug('creating Journal() for %s', path)
        self.path = Path(path)
        self.logs = [ Log(child) for child in self.path.rglob('*.txt') ]

class Log():
    '''a zim-wiki journal log (considered a collection of entries)'''
    
    def __init__(self, path):
        '''import a full journal from the top-level recursively'''
        
        self.path = Path(path)
        self.metadata, self.header = str(), str()
        self.entries= []
        log = str()
        
        with open(path, 'r') as f:
            for n, line in enumerate(f):
                if n < 3: 
                    self.metadata += line
                    continue
                log += line

        for entry in re_entry.findall(log):
                self.entries.append(Entry(entry))

class Entry():
    '''an entry created from a log file'''
    
    def __init__(self, entry):
        self.header = entry.split('\n')[0]
        self.contents = entry.replace(self.header+'\n', '')
        #parsedate accepts YYYY MM without DD, avoid errors
        try:
            self.date = date(*parse_date(self.header))
        except ValueError as e:
            logging.warning('Skipping ValueError for date: %s', e)
    
    def addMediaReference(self, link):
        pass

class Media():
    '''a media file'''
    
    def __init__(self, date, path):
        self.date, self.path = date, path

if __name__ == "__main__":
    pass
