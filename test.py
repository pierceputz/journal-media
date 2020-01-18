import unittest
import time
from calendar import monthrange
from datetime import date
from pathlib import Path
from zmedia import Journal

#For journal entry creation
#---
METADATA='''\
Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.4
Creation-Date: Not Relevant
'''
HEADER='''\
====== {month} {year} ======

'''
ENTRY_HEADER='''\
==== {year}/{month}/{day} ====
'''
ENTRY_CONTENT='''\
Log:
    * Generic event
    * Generic event
    * Generic event
    * Generic event
    
Comments:
    * Generic Comment

'''
ENTRY = ENTRY_HEADER + ENTRY_CONTENT
JOURNALDIR = './test-environment/Journal/'
MINYEAR, MAXYEAR = 2013, 2021
#---

class TestJournalMediaClass(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        '''Set up the files we need for testing'''
        
        for year in range(MINYEAR, MAXYEAR):
            year = str(year)                # convert to str for .joinpath()
            year_dir = Path(JOURNALDIR + year)
            year_dir.mkdir(parents=True)
            
            for month in range(1,13):
                entry = ''                  # reset here or it accumulates
                month = str(month)          # same deal as above
                month_path = year_dir.joinpath(month + '.txt')
                entry += METADATA + HEADER.format(year=year, month=month)
                
                for day in range(1, monthrange(int(year), int(month))[1] + 1):
                    # Populate the entries by day
                    entry += ENTRY.format(year=year, month=month, day=day)
                month_path.write_text(entry)

    @classmethod
    def tearDownClass(cls):
        '''Delete the actual files then rmdir recursively in reverse'''
        journal_dir = Path(JOURNALDIR)
        
        for year_dir in journal_dir.iterdir():
            for f in year_dir.iterdir():
                f.unlink()
            year_dir.rmdir()
        journal_dir.rmdir()                #rmdir "Journal"
        Path(journal_dir.parent).rmdir()   #rmdir "test-environment"

    def test_journal_integrity(self):
        '''Test that we can create journals and retrieve their contents
        -Verify headings & contents
        -Add a heading for media links
        Search a directory for media to add to entries'''
        
        #load and verify journal contents
        journal = Journal(JOURNALDIR)
        for log in journal.logs:
            self.assertEqual(METADATA, log.metadata)
            self.assertTrue(log.path.exists())
            self.assertNotEqual(log.entries, [])
            #ensure each journal entry has: date, header, contents 
            for entry in log.entries:
                self.assertEqual(ENTRY_CONTENT, entry.contents)
                self.assertTrue(type(entry.date) == type(date()))
    
    def test_media_referencing(self):
        '''Link media to journal entries by date'''
        
        journal = Journal(JOURNALDIR)
        
        #journal.attachMedia(MEDIA_DIR)
        
    
if __name__ == "__main__":
    unittest.main()
