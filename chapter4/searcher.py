from services.get_match_rows_service import GetMatchRowsService
from services.get_scored_list_service import GetScoredListService
from sqlite3 import dbapi2 as sqlite, OperationalError


class Searcher(object):

    def __init__(self, dbname):
        """
        Initialize the Crawler with the name of the database
        """
        self.con = sqlite.connect(dbname)
       
    def __del__(self):
        self.con.close()

    def get_match_rows(self, query):
        """
        Query on given database for links when given words exist
        """
        return GetMatchRowsService(self, query).call()

    def get_scored_list(self, rows, word_ids):
        """
        Given a list of rows and word ids, calculate all the scores of
        relevance of each word
        """
        return GetScoredListService(self, rows, word_ids).call()

    def get_url_name(self, row_id):
        """
        From given row id, return url that associated with it
        """
        return self.con.execute(
            "SELECT url FROM urllist WHERE rowid={}".format(row_id)
        ).fetchone()[0]

    def query(self, query, limit=10):
        """
        Main method to search for links
        """
        try:
            rows, word_ids = self.get_match_rows(query)
        except OperationalError:
            print("No documents found for \"{}\"".format(query))
            return

        scores = self.get_scored_list(rows, word_ids)

        ranked_scores = sorted([(score, url) for (url, score) in scores.items()], reverse=1)
        for (score, urlid) in ranked_scores[0: limit]:
            print("{}\t{}".format(score, self.get_url_name(urlid)))
        return