import copy
import urllib
import requests

import chaininglib.constants as constants
from chaininglib.search.corpus import *
from chaininglib.wait import *
from chaininglib.search.corpus import _parse_xml, _show_error_if_any



class CorpusQuery:
    """ A query on a token-based corpus. """

    def __init__(self, corpus, pattern = None, detailed_context = False, extra_fields_doc = [], extra_fields_token = [], start_position = 1, metadata_filter={}):
        self._corpus = corpus
        self._pattern = pattern
        self._detailed_context = detailed_context
        self._extra_fields_doc = extra_fields_doc
        self._extra_fields_token = extra_fields_token
        self._start_position = start_position
        self._metadata_filter = metadata_filter

    def __str__(self):
        return 'CorpusQuery({0}, {1}, {2}, {3}, {4}, {5}, {6})'.format(
            self._corpus, self._pattern, self._detailed_context, self._extra_fields_doc, self._extra_fields_token, self._start_position, self._metadata_filter)

    def _copyWith(self, attrName, attrValue):
        c = copy.copy(self)
        setattr(c, attrName, attrValue)
        return c

    def pattern(self, p):
        return self._copyWith('_pattern', p)

    def detailed_context(self, detailed_context=True):
        return self._copyWith('_detailed_context', detailed_context)

    def extra_fields_doc(self, extra_fields_doc):
        return self._copyWith('_extra_fields_doc', extra_fields_doc)

    def extra_fields_token(self, extra_fields_token):
        return self._copyWith('_extra_fields_token', extra_fields_token)

    def start_position(self, start_position):
        return self._copyWith('_start_position', start_position)

    def metadata(self, metadata_filter):
        return self._copyWith('_metadata_filter', metadata_filter)

    def results(self):
        
        if self._corpus not in constants.AVAILABLE_CORPORA:
            raise ValueError("Unknown corpus: " + self._corpus)
        
        if self._pattern is None:
            raise ValueError('A pattern is required')
         
        # in case we have multiple patterns, get results for each of them and return those in a list
        if type(self._pattern) is list:
            result_dict = {}
            for one_pattern in self._pattern:
                cq = create_corpus(self._corpus).pattern(one_pattern)
                result_dict[one_pattern] = cq.results()
            return result_dict
            
            
        # show wait indicator
        show_wait_indicator('Searching '+self._corpus+ ' at page '+str(self._start_position))   
        
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
            df, next_page = _parse_xml(response_text, self._detailed_context, self._extra_fields_doc, self._extra_fields_token)
            # If there are next pages, call search_corpus recursively
            #print(next_page)
            if next_page > 0:
                remove_wait_indicator()
                self._start_position = next_page
                df_more = self.results()
                df = df.append(df_more, ignore_index=True)

            remove_wait_indicator()

            # show message out of xml, if some error has occured (prevents empty output)
            _show_error_if_any(response_text)

            return df
        except Exception as e:
            remove_wait_indicator()
            raise ValueError("An error occured when searching corpus " + self._corpus + ": "+ str(e))


def create_corpus(name):
    return CorpusQuery(name)

