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

    def __init__(self, lexicon):
        self._lexicon = lexicon
        self._lemma = None
        self._pos = None
        self._response = None
        

    def __str__(self):
        return 'LexiconQuery({0}, {1}, {2})'.format(
            self._lexicon, self._lemma, self._pos)

    def _copyWith(self, attrName, attrValue):
        c = copy.copy(self)
        setattr(c, attrName, attrValue)
        return c

    def lemma(self, l):
        '''
        Set a lemma as part of a lexicon search pattern
        '''
        return self._copyWith('_lemma', l)
    
    def pos(self, p):
        '''
        Set a part-of-speech as part of a lexicon search pattern
        '''
        return self._copyWith('_pos', p)
    
    

    def search(self):
        '''
        Perform a lexicon search 
        
        >>> # build a lexicon search query
        >>> lexicon_obj = create_lexicon(some_lexicon).lemma(some_lemma).search()
        >>> # get the results
        >>> df = lexicon_obj.results()
        '''
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
            
            # remove wait indicator, 
            status.remove_wait_indicator()
            
            # object enriched with response
            return self._copyWith('_response', records_string)
           
        except Exception as e:
            status.remove_wait_indicator()
            raise ValueError("An error occured when searching lexicon " + self._lexicon + ": "+ str(e))
    
    

    # OUTPUT    
    
    def json(self):
        '''
        Get the JSON response (unparsed) of a lexicon search 
        '''
        return self._response
    
    
    def results(self):
        '''
        Get the results (as Pandas DataFrame) of a lexicon search 
        
        >>> # build a lexicon search query
        >>> lexicon_obj = create_lexicon(some_lexicon).lemma(some_lemma).search()
        >>> # get the results
        >>> df = lexicon_obj.results()
        '''
        
        records_string = self.json()
        
        df = pd.read_json(records_string, orient="records")

        # make sure cells containing NULL are added too, otherwise we'll end up with ill-formed data
        # CAUSES MALFUNCTION: df = df.fillna('')
        df = df.applymap(lambda x: '' if pd.isnull(x) else x["value"])  

        return df
    
    

def create_lexicon(name):
    '''
    API constructor
    
    >>> lexicon_obj = create_lexicon(some_lexicon).lemma(some_lemma).search()
    >>> df = lexicon_obj.results()
    '''
    return LexiconQuery(name)


def get_available_lexica():
    '''
    This function returns the list of the available lexica
    '''
    return list(constants.AVAILABLE_LEXICA.keys())