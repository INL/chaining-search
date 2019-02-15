import json
import pandas as pd
import copy
import urllib
import requests
import chaininglib.constants as constants
import chaininglib.ui.status as status
import chaininglib.search.lexiconQueries as lexiconQueries

class LexiconQuery:
    """ A query on a lexicon. """

    def __init__(self, lexicon, lemma = None, pos = None):
        self._lexicon = lexicon
        self._lemma = lemma
        self._pos = pos
        

    def __str__(self):
        return 'LexiconQuery({0}, {1}, {2})'.format(
            self._lexicon, self._lemma, self._pos)

    def _copyWith(self, attrName, attrValue):
        c = copy.copy(self)
        setattr(c, attrName, attrValue)
        return c

    def lemma(self, l):
        return self._copyWith('_lemma', l)
    
    def pos(self, p):
        return self._copyWith('_pos', p)

    def results(self):
        
        if self._lexicon not in constants.AVAILABLE_LEXICA:
            raise ValueError("Unknown lexicon: " + self._lexicon)
            
        if self._lemma is None and self._pos is None:
            raise ValueError('A lemma and/or a part-of-speech is required')
            
        # build query
        query = lexiconQueries.lexicon_query(self._lemma, self._pos, self._lexicon)
            
        # show wait indicator, so the user knows what's happening
        status.show_wait_indicator('Searching '+self._lexicon)

        # default endpoint, except when diamant is invoked
        endpoint = constants.AVAILABLE_LEXICA[self._lexicon]        

        try:
            # Accept header is needed for virtuoso, it isn't otherwise!
            response = requests.post(endpoint, data={"query":query}, headers = {"Accept":"application/sparql-results+json"})

            response_json = json.loads(response.text)
            records_json = response_json["results"]["bindings"]
            records_string = json.dumps(records_json)    
            df = pd.read_json(records_string, orient="records")

            # make sure cells containing NULL are added too, otherwise we'll end up with ill-formed data
            # CAUSES MALFUNCTION: df = df.fillna('')
            df = df.applymap(lambda x: '' if pd.isnull(x) else x["value"])         

            # remove wait indicator, 
            status.remove_wait_indicator()

            return df
        except Exception as e:
            status.remove_wait_indicator()
            raise ValueError("An error occured when searching lexicon " + self._lexicon + ": "+ str(e))


def create_lexicon(name):
    return LexiconQuery(name)
