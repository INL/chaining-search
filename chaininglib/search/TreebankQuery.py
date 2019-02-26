import copy
import urllib
import chaininglib.constants as constants
from chaininglib.search.treebankParse import _parse_treebank_xml
import chaininglib.ui.status as status
from BaseXClient import BaseXClient
import pandas as pd

from chaininglib.search.GeneralQuery import GeneralQuery

class TreebankQuery(GeneralQuery):
    """ A query on a treebank. """

    def __init__(self, resource = None):
        super().__init__(resource)

    def __str__(self):
        return 'TreebankQuery({0}, {1}, {2})'.format(
            self._resource, self._pattern_given, self._response)

    
    
    
    def search(self):
        '''
        Perform a treebank search 
        
        >>> # build a corpus search query
        >>> treebank_obj = create_treebank(some_treebank).pattern(some_pattern).search()

        '''
        self._pattern = self._pattern_given
        try:
            # show wait indicator, so the user knows what's happening
            status.show_wait_indicator('Searching treebanks')
            
            # create session
            session = BaseXClient.Session('svowgr01.ivdnt.loc', 1984, 'admin', 'admin')

            # perform command and returned xml response
            session.execute("open CGN_ID")
            response = session.execute(self._pattern)

            # close session
            session.close()
            
            # remove wait indicator, 
            status.remove_wait_indicator()            
            
            self._search_performed = True

            # object enriched with response
            return self._copyWith('_response', response)
        
        except Exception as e:
            status.remove_wait_indicator()
            raise ValueError("An error occured when searching the treebank : "+ str(e))


            
    # OUTPUT    
            
    def xml(self):
        '''
        Get the XML response (unparsed) of a treebank search 
        '''
        self.check_search_performed()

        return self._response
            

    def kwic(self):
        '''
        Get the results (as Pandas DataFrame) of a treebank search 
        
        >>> # build a corpus search query
        >>> treebank_obj = create_treebank(some_treebank).pattern(some_pattern).search()
        >>> # get the results as table of kwic's
        >>> df = treebank_obj.kwic()
        '''
        
        self.check_search_performed()
        df = pd.DataFrame()
        for one_tree in self.trees():
            
            # get the layers
            layers = one_tree.toLayers()
            nr_of_tokens = len(layers)
            
            # layers need to get into a 1-dimention array
            concatenated_layers = []
            for one in layers:
                concatenated_layers = concatenated_layers + one
            
            
            columns_lst = []
            for i in range(0, nr_of_tokens, 1):
                columns_lst = columns_lst + ['lemma '+str(i), 'pos '+str(i), 'wordform '+str(i)]
            
            #print(columns_lst)
            #print(concatenated_layers)
            
            df_subtree = pd.DataFrame([concatenated_layers], columns=columns_lst)
            df = pd.concat( [df, df_subtree], sort=False, ignore_index=True ) 
        df = df.fillna("")

        # _df_kwic is assigned instead of appended, so kwic() can be called multiple times
        self._df_kwic = df
        return self._df_kwic
        
        
            
    def trees(self):
        '''
        Get results (as nested objects) matching a treebank search query
        
        >>> # build a corpus search query
        >>> treebank_obj = create_treebank(some_treebank).pattern(some_pattern).search()
        >>> # get the results as nested objects
        >>> df = treebank_obj.trees()
        '''
        
        self.check_search_performed()

        trees = _parse_treebank_xml(self._response)
        
        return trees
    
    

def create_treebank(name=None):
    '''
    API constructor
    
    >>> treebank_obj = create_treebank(some_treebank).pattern(some_pattern).search()
    >>> df = treebank_obj.kwic()
    '''
    return TreebankQuery(name)
