import urllib
import requests
import copy
import chaininglib.constants as constants
import chaininglib.ui.status as status
import chaininglib.search.corpusHelpers as corpusHelpers
import chaininglib.search.corpusQueries as corpusQueries
import pandas as pd

from chaininglib.search.GeneralQuery import GeneralQuery

class CorpusQuery(GeneralQuery):
    """ A query on a token-based corpus. """

    def __init__(self, resource, pattern = None, lemma = None, word=None, pos=None, detailed_context = False, extra_fields_doc = [], extra_fields_token = [], start_position = 0, max_results= constants.RECORDS_PER_PAGE, metadata_filter={}, method=None):
        
        super().__init__(resource, pattern, lemma, word, pos)
        self._detailed_context = detailed_context
        self._extra_fields_doc = extra_fields_doc
        self._extra_fields_token = extra_fields_token
        self._start_position = start_position
        self._max_results = max_results
        self._metadata_filter = metadata_filter
        self._response = []
        self._df_kwic = pd.DataFrame()
        self._search_performed = False
        
        if self._resource not in constants.AVAILABLE_CORPORA:
            raise ValueError("Unknown corpus: " + self._resource)

        if method is not None:
            # If method supplied by user, use it
            self._method = method
        # Otherwise, use default method given in config
        elif "default_method" in constants.AVAILABLE_CORPORA[self._resource]:
            self._method = constants.AVAILABLE_CORPORA[self._resource]["default_method"]
        # Last resort: try FCS
        else:
            self._method="fcs"

    def __str__(self):
        return 'CorpusQuery({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9})'.format(
            self._resource, self._pattern_given, self._lemma, self._word, self._pos, self._detailed_context, self._extra_fields_doc, self._extra_fields_token, self._start_position, self._metadata_filter, self._method)

    def detailed_context(self, detailed_context=True):
        '''
        Request a CorpusQuery object to return a detailed context.
        
        Args:
            detailed_context: If True, every single tokens will be returned with multiple information layers (like lemma, wordfor, part-of-speech, ...). If False, only hits will have multiple information layers

        
        Returns:
            CorpusQuery object
        '''
        return self._copyWith('_detailed_context', detailed_context)

    def extra_fields_doc(self, extra_fields_doc):
        '''
        Request a CorpusQuery object to return the named document metadata fields.
        
        Args:
            extra_fields_doc: List of extra document metadata fields
       
        Returns:
            CorpusQuery object
        '''
        return self._copyWith('_extra_fields_doc', extra_fields_doc)

    def extra_fields_token(self, extra_fields_token):
        '''
        Request a CorpusQuery object to return the named extra token layers.
        
        Args:
            extra_fields_token: List of extra token layers
        
        Returns:
            CorpusQuery object
        '''
        return self._copyWith('_extra_fields_token', extra_fields_token)

    def start_position(self, start_position):
        '''
        Request a CorpusQuery object to return the stated page number of the whole result pages collection.
        This option might not be used by users, but the search procedure needs this to be able to retrieve
        full results, as those might be spread among more pages.
        
        Args:
            start_position: result page number to be requested.
        
        Returns:
            CorpusQuery object
        '''
        return self._copyWith('_start_position', start_position)

    def max_results(self, max_results):
        '''
        Limit the maximum number of results returned.
        
        Args:
            max_results: maximum number of results.
        
        Returns:
            CorpusQuery object
        '''
        return self._copyWith('_max_results', max_results)

    def metadata_filter(self, metadata_filter):
        '''
        Set metadata fields to filter results set on. If method is FCS, results will be filtered after the request. For Blacklab, filtered results will be requested from the server.
        
        Args:
            metadata_filter: Dictionary of conditions. The key represents the column to be filtered. If the value is a string, the value will be matched exactly. If the value is a list, it will be interpreted as a numerical interval.
        
        Returns:
            CorpusQuery object
        '''
        return self._copyWith('_metadata_filter', metadata_filter)
    
    def method(self, method):
        '''
        Set method to make request

        Args:
            method: fcs (Federated Content Search) or blacklab

        Returns:
            CorpusQuery object
        '''
        return self._copyWith('_method', method)
    
    def search(self):
        '''
        Request results matching a corpus search query

        Returns:
            CorpusQuery object
        
        >>> # build a corpus search query
        >>> corpus_obj = create_corpus(some_corpus).pattern(some_pattern)
        >>> # get the results
        >>> df = corpus_obj.search().kwic()
        '''
        
        # _pattern_given keeps unchanged so as to be able to call the same corpus object multiple times
        # only _pattern is set differently if needed
        
        
        if self._pattern_given:
            if self._lemma or self._word or self._pos:
                raise ValueError('When a pattern (%s) is given, lemma (%s), word (%s) and/or pos (%s) cannot be supplied too. Redundant!' % (self._pattern_given, self._lemma, self._word, self._pos))
            else:
                # Use pattern supplied by user
                self._pattern = copy.copy(self._pattern_given)
        else:
            # Pattern will be built with lemma, word, pos
            if self._lemma or self._word or self._pos:
                self._pattern = corpusQueries.corpus_query(self._lemma, self._word, self._pos)
            else:
                # If nothing is given: complain
                raise ValueError('A pattern OR a lemma/word/pos is required')

        
        
        # FCS starts counting at 1. Adjust 0 (default start position) to 1.
        # Other start positions, which are probably given deliberately, are left as is.
        if self._method=="fcs" and self._start_position == 0:
            self._start_position = 1

        # show wait indicator
        status.remove_wait_indicator()
        
        status.show_wait_indicator('Searching '+self._resource+ ' at result '+str(self._start_position))  
        
        amount_to_fetch = min(constants.RECORDS_PER_PAGE, max(0,self._max_results - self._start_position))
        

        try:
            if self._method=="fcs":
                # FCS does filtering on query results, so we have to request the filter fields in our query
                self._extra_fields_doc = list(set(self._extra_fields_doc + list(self._metadata_filter.keys())))

                # Do request to federated content search corpora, so we get same output format for every corpus
                url = ( constants.FCS_URL +
                        "&maximumRecords=" + str(amount_to_fetch) +
                        "&startRecord=" + str(self._start_position) +
                        "&x-fcs-context=" + self._resource + 
                        "&query=" + urllib.parse.quote_plus(self._pattern) )
            elif self._method=="blacklab":
                if "blacklab_url" not in constants.AVAILABLE_CORPORA[self._resource]:
                    raise ValueError("Blacklab access not available for this corpus.")
                    
                # Blacklab can filter metadata on server
                lucene_filter = corpusHelpers._create_lucene_metadata_filter(self._metadata_filter)
                
                url = ( constants.AVAILABLE_CORPORA[self._resource]["blacklab_url"] + "/hits?"
                        "&number=" + str(amount_to_fetch) +
                        "&first=" + str(self._start_position) +
                        "&patt=" + urllib.parse.quote(self._pattern) +
                        "&filter=" + urllib.parse.quote_plus(lucene_filter) )
            else:
                raise ValueError("Invalid request method: " +  self._method + ". Should be one of: 'fcs' or 'blacklab'.")
                
            
            #print ('Corpus Query url:' + url)
            
            response = requests.get(url)
            response_text = response.text
            self._response.append(response_text)
            if self._method=="fcs":
                df, next_page = corpusHelpers._parse_xml_fcs(response_text, self._detailed_context, self._extra_fields_doc, self._extra_fields_token)
            elif self._method=="blacklab":
                df, next_page = corpusHelpers._parse_xml_blacklab(response_text, self._detailed_context, self._extra_fields_doc, self._extra_fields_token)
                
            # If there are next pages, call search_corpus recursively (could result in )
            
            retrieved_so_far = self._start_position + len(df.index)

            #print("# results now:" + str(retrieved_so_far) + " max: " + str(self._max_results))

            if next_page > 0 and retrieved_so_far < self._max_results:
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
            df = df.fillna("")
            #df = self._df_kwic.append(df, ignore_index=True)
            
            self._search_performed = True
            
            
            # Save dataframe in object, so it can be retrieved with .kwic()
            return self._copyWith('_df_kwic', df)

        except Exception as e:
            status.remove_wait_indicator()
            raise ValueError("An error occured when searching corpus " + self._resource + ": "+ str(e))
    
    
    
    # OUTPUT

    def xml(self):
        '''
        Get the XML response (unparsed) of a Corpus search
        
        Returns:
            XML string
            
        >>> corpus_obj = create_corpus(some_corpus).pattern(some_pattern)
        >>> xml = corpus_obj.search().xml()
        '''
        self.check_search_performed()
        if self._method == "fcs" and self._metadata_filter:
            raise ValueError("Retrieving xml not possible for method FCS in combination with metadata filters. Remove metadata filter and try again.")
        return "\n".join(self._response)
    
    
    def kwic(self):
        '''
        Get the Pandas DataFrame with one keyword in context (KWIC) per row
        
        Returns:
            Pandas DataFrame
        '''
        self.check_search_performed()
        return self._df_kwic



def create_corpus(name):
    '''
    API constructor
    
    Args:
        name: corpus name
    
    Returns:
        CorpusQuery object
    
    >>> corpus_obj = create_corpus(some_corpus).pattern(some_pattern)
    >>> df = corpus_obj.search().kwic()
    '''
    return CorpusQuery(name)

def get_available_corpora(exclude=[]):
    '''
    This function returns the list of the available corpora
    
    Returns:
        list of corpus name strings
        
    >>> # get list of corpora at our disposal and query each of them
    >>> for one_corpus in get_available_corpora(exclude=["nederlab"]):
    >>>     c = create_corpus(one_corpus).lemma("woordenboek").detailed_context(True).search()
    >>>     df_corpus = c.kwic() 
    '''
    return [x for x in list(constants.AVAILABLE_CORPORA.keys()) if x not in exclude]