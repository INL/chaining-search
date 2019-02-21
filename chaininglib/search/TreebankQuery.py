import copy
import urllib
import chaininglib.constants as constants
from chaininglib.search.treebankParse import _parse_treebank_xml
import chaininglib.ui.status as status
from BaseXClient import BaseXClient
import pandas as pd

class TreebankQuery:
    """ A query on a treebank. """

    def __init__(self, treebank = None):
        
        self._treebank = treebank
        self._pattern = None
        self._response = None

    def __str__(self):
        return 'TreebankQuery({0}, {1}, {2})'.format(
            self._treebank, self._pattern, self._response)

    def _copyWith(self, attrName, attrValue):
        c = copy.copy(self)
        setattr(c, attrName, attrValue)
        return c

    def pattern(self, p):
        '''
        Set a treebank search pattern 
        '''
        return self._copyWith('_pattern', p)
    
    
    
    def search(self):
        '''
        Perform a treebank search 
        
        >>> # build a corpus search query
        >>> treebank_obj = create_treebank(some_treebank).pattern(some_pattern).search()

        '''
        
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
        return self._response
            

    def results(self):
        '''
        Get the results (as Pandas DataFrame) of a treebank search 
        
        >>> # build a corpus search query
        >>> treebank_obj = create_treebank(some_treebank).pattern(some_pattern).search()
        >>> # get the results
        >>> df = treebank_obj.results()
        '''
        
        # Instantiate a DataFrame, in which we will gather all the trees
        df_treebank = pd.DataFrame()
        
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
            df_treebank = pd.concat( [df_treebank, df_subtree] ) 
            
        return df_treebank
        
        
            
    def trees(self):
        '''
        Get results (as nested objects) matching a treebank search query
        
        >>> # build a corpus search query
        >>> treebank_obj = create_treebank(some_treebank).pattern(some_pattern).search()
        >>> # get the results as nested objects
        >>> df = treebank_obj.trees()
        '''
        
        trees = _parse_treebank_xml(self._response)
        
        return trees
    
    

def create_treebank(name=None):
    '''
    API constructor
    
    >>> treebank_obj = create_treebank(some_treebank).pattern(some_pattern).search()
    >>> df = treebank_obj.results()
    '''
    return TreebankQuery(name)
