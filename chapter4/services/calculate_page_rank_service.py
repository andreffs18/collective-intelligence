

class CalculatePageRankService(object):

    def __init__(self, crawler, iterations=20):
        self.crawler = crawler
        self.iterations = iterations

    def call(self):
        # clear out the current PageRank scores
        self._clean_page_rank_scores()

        # initialize every PageRank score to 1.0
        self._init_page_rank_scores()

        for i in range(self.iterations):
            print("Iteration {} of {}...".format(i + 1, self.iterations))

            url_ids = self.crawler.con.execute("SELECT rowid FROM urllist")
            for (url_id, ) in url_ids:
                page_rank = 0.15

                # loop through all the pages that link to this one
                links = self._get_associated_links(url_id)
                for (link, ) in links:
                    link_page_rank_score = self._get_page_rank_score(link)
                    link_count = self._get_url_count(link)
                    page_rank += 0.85 * (link_page_rank_score / link_count)

                self._update_page_rank_score(url_id, page_rank)
            self.crawler.db_commit()

    def _get_associated_links(self, url_id):
        return self.crawler.con.execute(
            "SELECT DISTINCT fromid FROM link WHERE toid={}".format(url_id))

    def _get_page_rank_score(self, url_id):
        return self.crawler.con.execute(
            "SELECT score FROM pagerank WHERE urlid={}".format(url_id)
        ).fetchone()[0]

    def _get_url_count(self, url_id):
        return self.crawler.con.execute(
            "SELECT COUNT(*) FROM link WHERE fromid={}".format(url_id)
        ).fetchone()[0]

    def _update_page_rank_score(self, url_id, new_page_rank):
        return self.crawler.con.execute(
            "UPDATE pagerank SET score={} WHERE urlid={}"
            "".format(new_page_rank, url_id))

    def _clean_page_rank_scores(self):
        self.crawler.con.execute("DROP TABLE IF EXISTS pagerank")
        self.crawler.con.execute("CREATE TABLE pagerank(urlid PRIMARY KEY, score)")

    def _init_page_rank_scores(self):
        self.crawler.con.execute("INSERT INTO pagerank SELECT rowid, 1.0 FROM urllist")
        self.crawler.db_commit()