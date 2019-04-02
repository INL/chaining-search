import copy
import pandas as pd

class GeneralQuery:
    """ A general query """

    def __init__(self, resource, pattern = None, lemma = None, word=None, pos=None):
        
        self._resource = resource
        self._pattern_given = pattern
        self._pattern = None
        self._lemma = lemma
        self._word = word
        self._pos = pos
        self._query_type = 'get_wordforms'

        self._response = []
        self._df_kwic = pd.DataFrame()
        self._search_performed = False
        
    def _copyWith(self, attrName, attrValue):
        c = copy.copy(self)
        setattr(c, attrName, attrValue)
        return c

    def pattern(self, p):
        '''
        Set a search pattern

        Args:
            p: pattern

        Returns:
            search object
        '''
        return self._copyWith('_pattern_given', p)
   
    def query_type(self, t):
        '''
        Set a query type

        Args:
            t: query type

        Returns:
            search object
        '''
        return self._copyWith('_query_type', t)

    def lemma(self, l):
        '''
        Set a lemma as part of a search pattern

        Args:
            l: lemma

        Returns:
            search object
        '''
        return self._copyWith('_lemma', l)
    
    def word(self, w):
        '''
        Set a word form as part of a search pattern

        Args:
            w: word form

        Returns:
            search object
        '''
        return self._copyWith('_word', w)
    
    def pos(self, p):
        '''
        Set a part-of-speech as part of a search pattern

        Args:
            p: part-of-speech (POS) tag
            
        Returns:
            search object
        '''
        return self._copyWith('_pos', p)
    
    
    # OUTPUT

    def check_search_performed(self):
        '''
        Check if a search has been performed
        '''
        if not self._search_performed:
            raise ValueError("First perform search() on this object!")
