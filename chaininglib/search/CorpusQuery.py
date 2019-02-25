import copy
import urllib
import requests
import chaininglib.constants as constants
import chaininglib.ui.status as status
import chaininglib.search.corpusHelpers as corpusHelpers
import chaininglib.search.corpusQueries as corpusQueries
import pandas as pd

class CorpusQuery:
    """ A query on a token-based corpus. """

    def __init__(self, corpus, pattern = None, lemma = None, word=None, pos=None, detailed_context = False, extra_fields_doc = [], extra_fields_token = [], start_position = 0, metadata_filter={}, method="fcs"):
        
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
        self._method = method
        self._response = []
        self._df_kwic = pd.DataFrame()
        self._search_performed = False

    def __str__(self):
        return 'CorpusQuery({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9})'.format(
            self._corpus, self._pattern, self._lemma, self._word, self._pos, self._detailed_context, self._extra_fields_doc, self._extra_fields_token, self._start_position, self._metadata_filter, self._method)

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

    def metadata_filter(self, metadata_filter):
        '''
        Set metadata fields to filter results set on, after query has been performed.
        '''
        return self._copyWith('_metadata_filter', metadata_filter)
    
    def method(self, method):
        '''
        Set method to make request: fcs (Federated Content Search) or blacklab
        '''
        return self._copyWith('_method', method)
    
    def search(self):
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
        
        # FCS starts counting at 1. Adjust 0 (default start position) to 1.
        # Other start positions, which are probably given deliberately, are left as is.
        if self._method=="fcs" and self._start_position == 0:
            self._start_position = 1

        # show wait indicator
        status.remove_wait_indicator()
        status.show_wait_indicator('Searching '+self._corpus+ ' at page '+str(self._start_position))  
         
        # in case we have multiple patterns, get results for each of them and return those in a list
        if type(self._pattern) is list:
            patterns = copy.copy(self._pattern)
            for one_pattern in patterns:
                # Run search method for every pattern
                # Results will get appended
                self._pattern = one_pattern
                self = self.search()
            
             
        
        try:
            if self._method=="fcs":
                
                # FCS does filtering on query results, so we have to request the filter fields in our query
                self._extra_fields_doc = list(set(self._extra_fields_doc + list(self._metadata_filter.keys())))

                # Do request to federated content search corpora, so we get same output format for every corpus
                url = ( "http://portal.clarin.inl.nl/fcscorpora/clariah-fcs-endpoints/sru?operation=searchRetrieve&queryType=fcs"+
                        "&maximumRecords=" + str(constants.RECORDS_PER_PAGE) +
                        "&startRecord=" + str(self._start_position) +
                        "&x-fcs-context=" + self._corpus + 
                        "&query=" + urllib.parse.quote_plus(self._pattern) )
            elif self._method=="blacklab":
                if constants.AVAILABLE_CORPORA[self._corpus] == "":
                    raise ValueError("Blacklab access not available for this corpus.")
                # Blacklab can filter metadata on server
                lucene_filter = corpusHelpers._create_lucene_metadata_filter(self._metadata_filter)
                url = ( constants.AVAILABLE_CORPORA[self._corpus]+ "/hits?"
                        "&number=" + str(constants.RECORDS_PER_PAGE) +
                        "&first=" + str(self._start_position) +
                        "&patt=" + urllib.parse.quote(self._pattern) +
                        "&filter=" + urllib.parse.quote_plus(lucene_filter) )
            else:
                raise ValueError("Invalid request method: " +  self._method + ". Should be one of: 'fcs' or 'blacklab'.")
            response = requests.get(url)
            response_text = response.text
            self._response.append(response_text)
            if self._method=="fcs":
                df, next_page = corpusHelpers._parse_xml_fcs(response_text, self._detailed_context, self._extra_fields_doc, self._extra_fields_token)
            elif self._method=="blacklab":
                df, next_page = corpusHelpers._parse_xml_blacklab(response_text, self._detailed_context, self._extra_fields_doc, self._extra_fields_token)
            # If there are next pages, call search_corpus recursively
            if next_page > 0:
                self._start_position = next_page
                df_more = self.search().kwic()
                df = df.append(df_more, ignore_index=True)

            status.remove_wait_indicator()

            # show message out of xml, if some error has occured (prevents empty output)
            corpusHelpers._show_error_if_any(response_text)

            # Filter results on metadata (performeed after query for FCS)
            if self._method=="fcs":
                if self._metadata_filter:
                    filters = corpusHelpers._create_pandas_metadata_filter(df, self._metadata_filter)
                    df = df[filters]
            
            # Append new entries (df) to existing dataframe (self._df_kwic): this is relevant if calling this function for multiple search queries
            df = self._df_kwic.append(df, ignore_index=True)
            
            self._search_performed = True

            # Save dataframe in object, so it can be retrieved with .kwic()
            return self._copyWith('_df_kwic', df)

        except Exception as e:
            status.remove_wait_indicator()
            raise ValueError("An error occured when searching corpus " + self._corpus + ": "+ str(e))
    
    # OUTPUT

    def xml(self):
        '''
        Get the XML response (unparsed) of a treebank search 
        '''
        if not self._search_performed:
            raise ValueError("First perform search() on this object!")
        if self._method == "fcs" and self._metadata_filter:
            raise ValueError("Retrieving xml not possible for method FCS in combination with metadata filters. Remove metadata filter and try again.")
        return "\n".join(self._response)
    
    def kwic(self):
        '''
        Get the Pandas DataFrame with one keyword in context (KWIC) per row
        '''
        if not self._search_performed:
            raise ValueError("First perform search() on this object!")
        return self._df_kwic



def create_corpus(name):
    '''
    API constructor
    
    >>> corpus_obj = create_corpus(some_corpus).pattern(some_pattern)
    >>> df = corpus_obj.results()
    '''
    return CorpusQuery(name)

def get_available_corpora():
    '''
    This function returns the list of the available lexica
    '''
    return list(constants.AVAILABLE_CORPORA.keys())