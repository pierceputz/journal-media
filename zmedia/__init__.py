import re
from datetime import date
from pathlib import Path
from zim.parsing import parse_date      #requires access to zim-wiki
import logging

logging.basicConfig(level=logging.DEBUG)

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
        self.logs = [ Log(child) for child in 
                      self.path.rglob('*.txt') ]

class Log():
    '''a zim-wiki journal log (considered a collection of entries)'''
    
    def __init__(self, path):
        '''import a full journal from the top-level recursively'''
        
        self.path = Path(path)
        self.metadata, self.header = str(), str()
        self.entries= []
        startparsing = False
        entry = str()
        
        with open(path, 'r') as f:
            for n, line in enumerate(f):
                if n < 3: 
                    self.metadata += line
                    continue
                #Rewrite entirely. I think it get confused and turns off 
                #the parser because the first heading is the log heading
                #not an entry heading
                #Should probably use regex
                if is_heading(line) and startparsing != True:
                    logging.debug('Entry parsing started for %s', line)
                    self.header = 
                    startparsing == True
                    entry += line
                elif is_heading(line) == False and startparsing == True:
                    entry += line
                    logging.debug(entry)
                elif is_heading(line) and startparsing == True:
                    logging.debug('Entry ready to be created: %s', entry)
                    self.entries.append(Entry(entry))
                    startparsing, entry = False, ''
            #else:                                       # capture last entry
            #    if startparsing == True:
            #        self.entries.append(Entry(entry))

class Entry():
    '''an entry created from a log file'''
    
    def __init__(self, entry):
        self.header = entry.split('\n')[0]
        self.contents = entry.replace(self.header, '')
        self.date = date(*parse_date(self.header))
    
    def addMediaReference(self, link):
        pass

class Media():
    '''a media file'''
    
    def __init__(self, date, path):
        self.date, self.path = date, path

if __name__ == "__main__":
    pass
