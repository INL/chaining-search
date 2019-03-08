import json
import pandas as pd
import urllib
import requests
import chaininglib.constants as constants
import chaininglib.ui.status as status
import chaininglib.search.lexiconQueries as lexiconQueries

from chaininglib.search.GeneralQuery import GeneralQuery

class LexiconQuery(GeneralQuery):
    """ A query on a lexicon. """

    def __init__(self, resource, lemma=None, pos=None):
        super().__init__(resource, pattern=None, lemma=lemma, word=None, pos=pos)
        

    def __str__(self):
        return 'LexiconQuery({0}, {1}, {2})'.format(
            self._resource, self._lemma, self._pos)

    def search(self):
        '''
        Perform a lexicon search 

        Returns:
            LexiconQuery object
        
        >>> # build a lexicon search query
        >>> lexicon_obj = create_lexicon(some_lexicon).lemma(some_lemma).search()
        >>> # get the results as table of kwic's
        >>> df = lexicon_obj.kwic()
        '''
        if self._resource not in constants.AVAILABLE_LEXICA:
            raise ValueError("Unknown lexicon: " + self._resource)
        
        if self._pattern_given is not None:
            raise ValueError('In lexicon search, patterns are not allowed. Use lemma and/or a part-of-speech instead.')
            
        if self._lemma is None and self._pos is None:
            raise ValueError('A lemma and/or a part-of-speech is required')
            
        # Reset self._df_kwic, from previous calls of search()
        self._df_kwic = pd.DataFrame()
        # show wait indicator, so the user knows what's happening
        status.show_wait_indicator('Searching '+self._resource)

        lexicon_settings = constants.AVAILABLE_LEXICA[self._resource]
        method = lexicon_settings["method"]

        if method=="sparql":
            endpoint = lexicon_settings["sparql_url"]
            
            sparql_offset = 0
            sparql_limit = 1000 if self._resource == 'diamant' else None
            non_empty_response = True
            
            collection_df = pd.DataFrame()
            
            while non_empty_response:
                
                # show how far we are (update offset indicator)
                status.show_wait_indicator('doing offset '+ str(sparql_offset))

                # build query
                query = lexiconQueries.lexicon_query(self._lemma, self._pos, self._resource, sparql_limit, sparql_offset)
                
                display(query)
                
                try:
                    # Accept header is needed for virtuoso, it isn't otherwise!
                    response = requests.post(endpoint, data={"query":query}, headers = {"Accept":"application/sparql-results+json"})
                except Exception as e:
                    status.remove_wait_indicator()
                    raise ValueError("An error occured when searching lexicon " + self._resource + ": "+ str(e))
                
                # if response is ill formed, show it for debugging!
                try:
                    response_json = json.loads(response.text)                
                except:
                    display(response.text)
                    
                records_json = response_json["results"]["bindings"]
                records_string = json.dumps(records_json)

                # _df_kwic is assigned instead of appended, so kwic() can be called multiple times
                part_df = pd.read_json(records_string, orient="records")
                
                # if the response is not empty, append the data to the whole collection of data
                if part_df.size > 0:
                    collection_df = collection_df.append(part_df)
                    
                # if the response size equals the max allowed size, we might have to collect more data at the next offset
                if (sparql_limit is not None and part_df.size == sparql_limit):
                    sparql_offset = sparql_offset + sparql_limit
                # otherwise, we must have reached the end, so there is no need to query any further
                else:
                    non_empty_response = False          
                    
                # remove previous offset indicator
                status.remove_wait_indicator()


            # _df_kwic is assigned instead of appended, so kwic() can be called multiple times
            self._df_kwic = collection_df
            # make sure cells containing NULL are added too, otherwise we'll end up with ill-formed data
            # CAUSES MALFUNCTION: df = df.fillna('')
            self._df_kwic = self._df_kwic.applymap(lambda x: '' if pd.isnull(x) else x["value"])
                
        elif method=="lexicon_service":
            query_url = constants.LEXICON_SERVICE_URL + "&database=" + self._resource

            if not self._lemma:
                raise ValueError("For this lexicon, a lemma is necessary!")
            query_url += "&lemma=" + self._lemma
            if self._pos:
                query_url += "&pos=" + self._pos
            try:
                response = requests.get(query_url, headers = {"Accept":"application/json"})
            except Exception as e:
                status.remove_wait_indicator()
                raise ValueError("An error occured when searching lexicon " + self._resource + ": "+ str(e))

            response_json = json.loads(response.text)
            records_json = response_json["wordforms_list"]
            records_string = json.dumps(records_json)
            
            # _df_kwic is assigned instead of appended, so kwic() can be called multiple times
            
            for query_result in records_json:
                query_result_string = json.dumps(query_result)
                df_query_result = pd.read_json(query_result_string)
                self._df_kwic = self._df_kwic.append(df_query_result, ignore_index=True)
            self._df_kwic = self._df_kwic.rename(columns={"found_wordforms":"wordform"})
            
            # make sure cells containing NULL are added too, otherwise we'll end up with ill-formed data
            # CAUSES MALFUNCTION: df = df.fillna('')
            #self._df_kwic = self._df_kwic.applymap(lambda x: '' if pd.isnull(x) else x["value"])
        else:
            raise ValueError("Unknown lexicon search method: " + method)
        
        # remove wait indicator, 
        status.remove_wait_indicator()
        
        self._search_performed = True

        # object enriched with response
        return self._copyWith('_response', records_string)
           
    
    

    # OUTPUT    
    
    def json(self):
        '''
        Get the JSON response (unparsed) of a lexicon search

        Returns:
            JSON string
            
        >>> # build a lexicon search query
        >>> lexicon_obj = create_lexicon(some_lexicon).lemma(some_lemma).search()
        >>> # get the JSON response
        >>> df = lexicon_obj.json()
        '''
        self.check_search_performed()

        return self._response
    
    
    def kwic(self):
        '''
        Get the keyword in context (KWIC) results (as Pandas DataFrame) of a lexicon search

        Returns:
            Pandas DataFrame
        
        >>> # build a lexicon search query
        >>> lexicon_obj = create_lexicon(some_lexicon).lemma(some_lemma).search()
        >>> # get the results as table of kwic's
        >>> df = lexicon_obj.kwic()
        '''
        
        self.check_search_performed()
        return self._df_kwic
    
    

def create_lexicon(name):
    '''
    API constructor

    Returns:
        LexiconQuery object
    
    >>> lexicon_obj = create_lexicon(some_lexicon).lemma(some_lemma).search()
    >>> df = lexicon_obj.kwic()
    '''
    return LexiconQuery(name)


def get_available_lexica():
    '''
    This function returns the list of the available lexica
    
    Returns:
        list of lexicon name strings
    '''
    return list(constants.AVAILABLE_LEXICA.keys())