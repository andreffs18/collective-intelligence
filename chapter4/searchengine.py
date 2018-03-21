from services.crawl_service import CrawlService
from services.get_text_only_service import GetTextOnlyService
from services.create_index_tables_service import CreateIndexTablesService
from services.separate_words_service import SeparateWordsService
from services.add_to_index_service import AddToIndexService
from services.get_entry_id_service import GetEntryIdService
from services.is_indexed_service import IsIndexedService
from pysqlite2 import dbapi2 as sqlite


class Crawler(object):

    def __init__(self, dbname):
        """
        Initialize the Crawler with the name of the database
        """
        self.con = sqlite.connect(dbname)
       
    def __del__(self):
        self.con.close()
    
    def db_commit(self):
        self.con.commit()
    
    def get_entry_id(self, table, field, value, create_new=True):
        """
        Auxilliary function for getting an entry id an adding it if its not present
        """
        return GetEntryIdService(self, table, field, value, create_new).call()

    def add_to_index(self, url, soup):
        """
        Index an individual page
        """
        AddToIndexService(self, url, soup).call()

    def get_text_only(self, soup):
        """
        Extract text from a HML page (no tags)
        """
        return GetTextOnlyService(self, soup).call()

    def separate_words(self, text):
        """
        Separate the words by a non-whitespace character
        """
        return SeparateWordsService(text).call()

    def is_indexed(self, url):
        """
        Return True if given url is already indexed
        """
        return IsIndexedService(self, url).call()

    def add_link_ref(self, url_from, url_to, link_text):
        """
        Add link between two pages
        """
        pass

    def crawl(self, pages, depth=2):
        """
        Starting with a list of pages, do a BFS (breadth first search) to the given depth, 
        indexing pages as we go
        """
        CrawlService(self, pages, depth).call()

    def create_index_tables(self):
        """
        Create database tables
        """
        CreateIndexTablesService(self).call()
