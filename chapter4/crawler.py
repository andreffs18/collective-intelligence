from services.crawler.crawl_service import CrawlService
from services.crawler.get_text_only_service import GetTextOnlyService
from services.crawler.create_index_tables_service import CreateIndexTablesService
from services.crawler.drop_tables_service import DropTablesService
from services.crawler.separate_words_service import SeparateWordsService
from services.crawler.calculate_page_rank_service import CalculatePageRankService
from services.crawler.add_link_to_reference_service import AddLinkReferenceService
from services.crawler.add_to_index_service import AddToIndexService
from services.crawler.get_entry_id_service import GetEntryIdService
from services.crawler.is_indexed_service import IsIndexedService

from sqlite3 import dbapi2 as sqlite


class Crawler(object):

    def __init__(self, dbname="searchindex.db"):
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
        AddLinkReferenceService(self, url_from, url_to, link_text).call()

    def crawl(self, pages, depth=2):
        """
        Starting with a list of pages, do a BFS (breadth first search) to the given depth, 
        indexing pages as we go
        """
        CrawlService(self, pages, depth).call()

    def calculate_page_rank(self, iterations=10):
        """
        Generate page rank scores for all available pages
        """
        CalculatePageRankService(self, iterations).call()

    def create_index_tables(self):
        """
        Create database tables
        """
        CreateIndexTablesService(self).call()

    def drop_tables(self):
        """
        Drop database tables
        """
        DropTablesService(self).call()

