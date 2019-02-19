import copy
import urllib
import requests
import chaininglib.constants as constants
import chaininglib.ui.status as status
import chaininglib.search.corpusParse as corpusParse
import chaininglib.search.corpusQueries as corpusQueries

class CorpusQuery:
    """ A query on a token-based corpus. """

    def __init__(self, corpus, pattern = None, lemma = None, word=None, pos=None, detailed_context = False, extra_fields_doc = [], extra_fields_token = [], start_position = 1, metadata_filter={}):
        
        self._corpus = corpus
        self._pattern = pattern        
        self._lemma = lemma
        self._word = word
        self._pos = pos        
        self._detailed_context = detailed_context
        self._extra_fields_doc = extra_fields_doc
        self._extra_fields_token = extra_fields_token
        self._start_position = start_position
        self._metadata_filter = metadata_filter

    def __str__(self):
        return 'CorpusQuery({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9})'.format(
            self._corpus, self._pattern, self._lemma, self._word, self._pos, self._detailed_context, self._extra_fields_doc, self._extra_fields_token, self._start_position, self._metadata_filter)

    def _copyWith(self, attrName, attrValue):
        c = copy.copy(self)
        setattr(c, attrName, attrValue)
        return c

    def pattern(self, p):
        '''
        Set a corpus search pattern 
        '''
        return self._copyWith('_pattern', p)
    
    def lemma(self, l):
        '''
        Set a lemma as part of a corpus search pattern
        '''
        return self._copyWith('_lemma', l)
    
    def word(self, w):
        '''
        Set a word as part of a corpus search pattern
        '''
        return self._copyWith('_word', w)
    
    def pos(self, p):
        '''
        Set a part-of-speech as part of a corpus search pattern
        '''
        return self._copyWith('_pos', p)

    def detailed_context(self, detailed_context=True):
        '''
        Request a corpus search object to return a detailed context.
        If True, every single tokens will be returned with multiple information layers (like lemma, wordfor, part-of-speech, ...)
        If False, only hits will have multiple information layers
        '''
        return self._copyWith('_detailed_context', detailed_context)

    def extra_fields_doc(self, extra_fields_doc):
        '''
        Request a corpus search object to return the named document metadata fields.
        '''
        return self._copyWith('_extra_fields_doc', extra_fields_doc)

    def extra_fields_token(self, extra_fields_token):
        '''
        Request a corpus search object to return the named extra token layers.
        '''
        return self._copyWith('_extra_fields_token', extra_fields_token)

    def start_position(self, start_position):
        '''
        Request a corpus search object to return the stated page number of the whole result pages collection.
        This option might not be used by users, but the search procedure needs this to be able to retrieve
        full results, as those might be spread among more pages.
        '''
        return self._copyWith('_start_position', start_position)

    def metadata(self, metadata_filter):
        '''
        What is the function of this one again????????
        '''
        return self._copyWith('_metadata_filter', metadata_filter)

    def results(self):
        '''
        Request results matching a corpus search query
        
        >>> # build a corpus search query
        >>> corpus_obj = create_corpus(some_corpus).pattern(some_pattern)
        >>> # get the results
        >>> df = corpus_obj.results()
        '''
        if self._corpus not in constants.AVAILABLE_CORPORA:
            raise ValueError("Unknown corpus: " + self._corpus)
            
        # default is: the pattern is supplied by the user
        # if not....
                
        # nothing given
        if self._pattern is None and self._lemma is None and self._word is None and self._pos is None:
            raise ValueError('A pattern OR a lemma/word/pos is required')
         
        # too much given
        if self._pattern is not None and (self._lemma is not None or self._word is not None or self._pos is not None):
                raise ValueError('When a pattern is given, lemma, word and/or pos cannot be supplied too. Redundant!')
        
        # pattern will be built with lemma, word, pos
        if self._pattern is None:
            self._pattern = corpusQueries.corpus_query(self._lemma, self._word, self._pos)
        
         
        # in case we have multiple patterns, get results for each of them and return those in a list
        if type(self._pattern) is list:
            result_dict = {}
            for one_pattern in self._pattern:
                
                cq = CorpusQuery(self._corpus, pattern = one_pattern, lemma = self._lemma, word=self._word, pos=self._pos, detailed_context = self._detailed_context, extra_fields_doc = self._extra_fields_doc, extra_fields_token = self._extra_fields_token, start_position = self._start_position, metadata_filter=self._metadata_filter)
                result_dict[one_pattern] = cq.results()
            return result_dict
            
            
        # show wait indicator
        status.show_wait_indicator('Searching '+self._corpus+ ' at page '+str(self._start_position))   
        
        try:
            # Do request to federated content search corpora, so we get same output format for every corpus
            url = (
                "http://portal.clarin.inl.nl/fcscorpora/clariah-fcs-endpoints/sru?operation=searchRetrieve&queryType=fcs"+
                "&maximumRecords=1000" +
                "&x-fcs-context=" + self._corpus + 
                "&query=" + urllib.parse.quote(self._pattern)
                   )
            #print(url)
            response = requests.get(url)
            response_text = response.text    
            df, next_page = corpusParse._parse_xml(response_text, self._detailed_context, self._extra_fields_doc, self._extra_fields_token)
            # If there are next pages, call search_corpus recursively
            #print(next_page)
            if next_page > 0:
                status.remove_wait_indicator()
                self._start_position = next_page
                df_more = self.results()
                df = df.append(df_more, ignore_index=True)

            status.remove_wait_indicator()

            # show message out of xml, if some error has occured (prevents empty output)
            corpusParse._show_error_if_any(response_text)

            return df
        except Exception as e:
            status.remove_wait_indicator()
            raise ValueError("An error occured when searching corpus " + self._corpus + ": "+ str(e))


def create_corpus(name):
    '''
    API constructor
    
    >>> corpus_obj = create_corpus(some_corpus).pattern(some_pattern)
    >>> df = corpus_obj.results()
    '''
    return CorpusQuery(name)


def get_available_corpora():
    '''
    This function returns the list of the available corpora
    '''
    return list(constants.AVAILABLE_CORPORA.keys())