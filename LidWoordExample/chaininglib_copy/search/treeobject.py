class TreeObject:
    
    def __init__(self, id, begin, end, lemma='', postag='', cat='', word='', rel=''):
        
        self._id = id
        self._begin = begin
        self._end = end
        
        self._lemma = lemma
        self._postag = postag  # leaves
        self._cat = cat        # not leaves
        self._word = word  
        
        self._rel = rel
        
        self._parts = [] # leaves of the tree!   
        
        # we need separators for string storage of tokens and their layers
        self._token_separator = "###"
        self._layer_separator = "@@@"
        
        
    def __str__(self):
        return 'TreeObject({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8})'.format(
            self._id, self._begin, self._end, self._lemma, self._postag, self._cat, self._word, self._rel, self._parts)
    
    
    def setLemma(self, lemma):        
        self._lemma = lemma
    def getLemma(self):        
        return self._lemma
        
        
    def setPostag(self, postag):        
        self._postag = postag
    def getPostag(self):        
        return self._postag
        
        
    def setCat(self, cat):        
        self._cat = cat        
    def getCat(self):        
        return self._cat 
        
        
    def setWord(self, word):        
        self._word = word     
    def getWord(self):        
        return self._word
        
 
    def setRel(self, rel):        
        self._rel = rel    
    def getRel(self):        
        return self._rel

    
    def addPart(self, part):        
        self._parts.append(part)
    def getParts(self):        
        return self._parts
    
    
    
    def extract(self, filiation_arr): 
        '''
        Extract some constituents out of the trees, given a filiation path declared as a list. 
        This list must consist of parts-of-speech or grammatical categories, put in hierarchical order, 
        from the top element to the leaf we are looking for. 
        
        So, let's say we're looking for nouns (N) which must be part of prepositional phrases, the filiation 
        path must be like ['pp', 'N'].
        The same way, if we search for nouns, which must be part of adjectival phrases (ap), which in turn
        must be part of prepositional phrases, the filiation path must be ['pp', 'ap', 'N']. 
        
        >>> tbq = create_treebank().pattern(some_pattern).search()
        >>> trees = tbq.trees()
        >>> 
        >>> list_of_nouns = []
        >>> for tree in trees:
        >>>     nouns = tree.extract(['pp', 'N'])  # a noun (N), which is part of a preposition phrase (pp).
        >>>     list_of_nouns = list_of_nouns + nouns
        >>>     
        >>> display(list_of_nouns)

        '''
        return self._extract(filiation_arr, [])
    
    def _extract(self, filiation_arr, bag_arr): 
        
        pos_searched_for = filiation_arr[0]
        new_filiation_arr = filiation_arr.copy()

        # if we find a match
        if ( ( self._postag == pos_searched_for or self._cat == pos_searched_for ) or 
             ( self._postag.startswith( pos_searched_for+"(" ) or self._cat.startswith( pos_searched_for+"(" ) ) ):

            # Remove the parent from the list of parents to look for            
            new_filiation_arr.pop(0)

            # If we have reached the bottom of the list (leaf), then we are done, so return the result                
            if len(new_filiation_arr) == 0:
                bag_arr.append(self.toString(catTag=False))
        
        # Carry on with the next parent (search deeper) 
        if len(new_filiation_arr) > 0:
            for onePart in self._parts:
                onePart._extract(new_filiation_arr, bag_arr)
            
        # done
        return bag_arr

        
   
    def toString(self, posTag=False, catTag=True):        
        '''
        Transform the tree object into a String representation of it (see example)
        Args:
            posTag: (default False) display parts-of-speech tags (leaves)
            catTag: (default True) display categorial tags (non leaves)
        Returns:
            List, consisting of lists of strings per layer
            
        >>> tbq = create_treebank().pattern(some_pattern).search()
        >>> trees = tbq.trees()
        >>> for tree in trees:            
        >>>    display(tree.toString())
        >>>        
        >>> '[ elkaar verrijking geven ]/inf'
        >>> '[ [ Gods liefde ]/np gestalte geven ]/inf'
        >>> etc
        '''
        
        if len(self._parts) == 0:
            
            return self._word + ( '/' + self._postag if posTag == True else '' )
        
        else:
        
            partsArr = []
            for onePart in self._parts:
                partsArr.append( onePart.toString( posTag, catTag ) )
                
            return ' '.join(partsArr) if catTag == False else ' [ ' + (' '.join(partsArr)) + ' ]/'+self._cat
              
            
            
    def toLayers(self):
        '''
        Transform the tree object into a list of lists of strings per annotation layer (see example)
        Returns:
            List, consisting of lists of strings per layer
            
        >>> tbq = create_treebank().pattern(some_pattern).search()
        >>> trees = tbq.trees()
        >>> for tree in trees:            
        >>>    display(tree.toLayers())
        >>>
        >>> [['eer', 'N(soort,ev,basis,dat)', 'ere'],
        >>>  ['geven', 'WW(inf,vrij,zonder)', 'geven'],
        >>>  ['wie', 'VNW(vb,pron,stan,vol,3p,getal)', 'wie'],
        >>>  ['', '', ''],
        >>>  ['eer', 'N(soort,ev,basis,dat)', 'ere'],
        >>>  ['toekomen', 'WW(pv,tgw,met-t)', 'toekomt']]
        >>> etc
            
        '''
        tokens_str = self._getLayersStr()        
        
        tokens_arr = tokens_str.split(self._token_separator)
        output_arr = []
        
        for one_token_str in tokens_arr:
            layer_parts = one_token_str.split(self._layer_separator)
            
            #nr = str(len(output_arr))
            #layer_parts_arr = {}
            #layer_parts_arr['lemma '+nr] = layer_parts[0]
            #layer_parts_arr['pos '+nr] = layer_parts[1]
            #layer_parts_arr['wordform '+nr] = layer_parts[2]
            
            #output_arr.append(layer_parts_arr)
            output_arr.append(layer_parts)
            
        return output_arr
    
        
    def _getLayersStr(self):
        
        if len(self._parts) == 0:
            
            return self._lemma + self._layer_separator + self._postag + self._layer_separator + self._word
        
        else:        
            partsArr = []
            for onePart in self._parts:
                partsArr.append( onePart._getLayersStr() )
                
            return self._token_separator.join(partsArr)