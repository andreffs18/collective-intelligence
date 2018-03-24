class GetMatchRowsService(object):

    def __init__(self, searcher, query):
        self.searcher = searcher
        self.query = query

    def call(self):
        # string to build the query
        field_list = 'w0.urlid'
        table_list = ''
        clause_list = ''
        word_ids = []
        table_number = 0

        # split words by spaces
        words = self.query.split(" ")
        for word in words:
            # Get word ID from database
            word_row = self._get_word_id(word)
            if word_row is None:
                continue

            word_id = word_row[0]
            word_ids.append(word_id)

            if table_number > 0:
                table_list += ","
                clause_list += ' and '
                clause_list += 'w{}.urlid = w{}.urlid and '.format(
                    table_number - 1, table_number)

            field_list += ', w{}.location'.format(table_number)
            table_list += 'wordlocation w{}'.format(table_number)
            clause_list += 'w{}.wordid = {}'.format(table_number, word_id)
            table_number += 1

        result = self._search_query(field_list, table_list, clause_list)
        return result, word_ids

    def _get_word_id(self, word):
        return self.searcher.con.execute(
            "SELECT rowid FROM wordlist WHERE word='{}'".format(word)
        ).fetchone()

    def _search_query(self, field_list, table_list, clause_list):
        query = "SELECT {} FROM {} WHERE {}".format(
            field_list, table_list, clause_list)
        print("Query: \n> {}".format(query))
        rows = self.searcher.con.execute(query)
        return [row for row in rows]