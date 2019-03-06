import copy
import urllib
import chaininglib.constants as constants
from chaininglib.search.treebankParse import _parse_treebank_xml
import chaininglib.ui.status as status
from BaseXClient import BaseXClient
import pandas as pd
import chaininglib.search.treebankQueries as treebankQueries

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
        Returns:
            TreebankQuery object
        
        >>> # build a treebank search query
        >>> treebank_obj = create_treebank(some_treebank).pattern(some_pattern).search()

        '''
        if self._pattern_given:
            if self._lemma or self._word or self._pos:
                raise ValueError('When a pattern (%s) is given, lemma (%s), word (%s) and/or pos (%s) cannot be supplied too. Redundant!' % (self._pattern_given, self._lemma, self._word, self._pos))
            else:
                # Use pattern supplied by user
                self._pattern = copy.copy(self._pattern_given)
        else:
            # Pattern will be built with lemma, word, pos
            if self._lemma or self._word or self._pos:
                self._pattern = treebankQueries.treebank_query(self._lemma, self._word, self._pos)
                print(self._pattern)
            else:
                # If nothing is given: complain
                raise ValueError('A pattern OR a lemma/word/pos is required')
        
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
        Returns:
            XML string
            
        >>> treebank_obj = create_treebank(some_treebank).pattern(some_pattern).search()
        >>> xml_response = treebank_obj.xml()
        '''
        self.check_search_performed()

        return self._response
            

    def kwic(self, align_lemma=None, align_pos=None, align_wordform=None):
        '''
        Get the results (as Pandas DataFrame) of a treebank search, with one keyword in context (KWIC) per row
        Beware: if no align_lemma etc is given, there will be no alignment
        Args:
            align_lemma: the lemma to align all results with (it then behaves as a hit)
            align_pos: same with pos
            align_wordform: same with wordform
        Returns:
            Pandas DataFrame
        
        >>> treebank_obj = create_treebank(some_treebank).pattern(some_pattern).search()
        >>> df = treebank_obj.kwic()
        '''
        
        self.check_search_performed()
        df = pd.DataFrame()
        
        for one_tree in self.trees():
            
            # get the layers
            layers = one_tree.toLayers()
            nr_of_tokens = len(layers)
            
            if align_lemma == None and align_pos == None and align_wordform == None:
                
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
                
            else:
                
                # layers need to get into a 1-dimention array
                # we will gather a left context, followed by the hit in 3 layers (lemma, pos, wordform), and finally a right context
                concatenated_layers = []
                hit_found = False
                
                # left context
                left_context = ""
                left_context_sep = ""
                # hit
                hit_lemma = ""
                hit_pos = ""
                hit_wordform = ""
                # right context
                right_context = ""
                right_context_sep = ""                
                
                for one in layers:
                    
                    current_lemma = one[0]
                    current_pos = one[1]
                    current_wordform = one[2]
                    
                    # build right context
                    if hit_found == True:
                        right_context = right_context + right_context_sep + current_wordform
                        right_context_sep = " "
                    
                    # find hit
                    if ((align_pos == None or align_pos == current_pos) and 
                       (align_lemma == None or align_lemma == current_lemma) and
                       (align_wordform == None or align_wordform == current_wordform )):
                        hit_found = True
                        concatenated_layers = concatenated_layers + [left_context] + [current_lemma] + [current_pos] + [current_wordform]
                        
                    # build left context
                    if hit_found == False:
                        left_context = left_context + left_context_sep + current_wordform
                        left_context_sep = " "
                        
                concatenated_layers = concatenated_layers + [right_context]
                
                columns_lst = ['left context', 'lemma 0', 'pos 0', 'wordform 0', 'right context']
                
                if len(concatenated_layers) == len(columns_lst):
                    df_subtree = pd.DataFrame([concatenated_layers], columns=columns_lst)
                    df = pd.concat( [df, df_subtree], sort=False, ignore_index=True ) 
                
            
        df = df.fillna("")

        # _df_kwic is assigned instead of appended, so kwic() can be called multiple times
        self._df_kwic = df
        return self._df_kwic
        
        
            
    def trees(self):
        '''
        Get results (as nested objects) matching a treebank search query
        Returns:
            list of tree objects
        
        >>> treebank_obj = create_treebank(some_treebank).pattern(some_pattern).search()
        >>> list_of_trees = treebank_obj.trees()
        '''
        
        self.check_search_performed()

        trees = _parse_treebank_xml(self._response)
        
        return trees
    
    

def create_treebank(name=None):
    '''
    API constructor
    Args:
        name: Name of the treebank
    Returns:
        TreebankQuery object
    
    >>> treebank_obj = create_treebank(some_treebank).pattern(some_pattern).search()
    >>> df = treebank_obj.kwic()
    '''
    return TreebankQuery(name)
