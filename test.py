import unittest
from zmedia import Journal
from pathlib import Path
from calendar import monthrange
import time

#For journal entry creation
#---
HEADER='''\
Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.4
Creation-Date: Not Relevant

====== {month} {year} ======

'''
CONTENT='''\
==== {year}/{month}/{day} ====

Log:
    * Generic event
    * Generic event
    * Generic event
    * Generic event
    
Comments:
    * Generic Comment

'''
JOURNALDIR = './test-environment/Journal/'
#---

class TestJournalMediaClass(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        '''Set up the files we need for testing'''
        
        for year in range(2013, 2021):
            year = str(year)                # convert to str for .joinpath()
            year_dir = Path(JOURNALDIR + year)
            year_dir.mkdir(parents=True)
            
            for month in range(1,13):
                entry = ''                  # reset here or it accumulates
                month = str(month)          # same deal as above
                month_path = year_dir.joinpath(month + '.txt')
                entry += HEADER.format(year=year, month=month)
                
                for day in range(1, monthrange(int(year), int(month))[1] + 1):
                    # Populate the entries by day
                    entry += CONTENT.format(year=year, month=month, day=day)
                month_path.write_text(entry)

    @classmethod
    def tearDownClass(cls):
        '''Delete the actual files so we can rmdir recursively in reverse'''
        journal_dir = Path(JOURNALDIR)
        
        for year_dir in journal_dir.iterdir():
            for f in year_dir.iterdir():
                f.unlink()
            year_dir.rmdir()
        journal_dir.rmdir()                #rmdir "Journal"
        Path(journal_dir.parent).rmdir()   #rmdir "test-environment"

    def test_journal_class(self):
        #Test that we can retrieve journal entries
        #-Access headings & contents
        journal = Journal(JOURNALDIR)
    
if __name__ == "__main__":
    unittest.main()
