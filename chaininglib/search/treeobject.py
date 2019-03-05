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
        
   
    def toString(self, posTag=False):
        
        if len(self._parts) == 0:
            
            return self._word + ( '/' + self._postag if posTag == True else '' )
        
        else:
        
            partsArr = []
            for onePart in self._parts:
                partsArr.append( onePart.toString() )
                
            return ' [ ' + (' '.join(partsArr)) + ' ]/'+self._cat
            
            
            
            
    def toLayers(self):
        '''
        Transform the tree object into a list of list of strings per annotation layer
        Returns:
            List, consisting of list of strings per layer
        '''
        layers_str = self._getLayersStr()        
        
        layers_input_arr = layers_str.split('###')
        layers_output_arr = []
        
        for one_layer_str in layers_input_arr:
            layer_parts = one_layer_str.split('@@@')
            
            #nr = str(len(layers_output_arr))
            #layer_parts_arr = {}
            #layer_parts_arr['lemma '+nr] = layer_parts[0]
            #layer_parts_arr['pos '+nr] = layer_parts[1]
            #layer_parts_arr['wordform '+nr] = layer_parts[2]
            
            #layers_output_arr.append(layer_parts_arr)
            layers_output_arr.append(layer_parts)
            
        return layers_output_arr
    
        
    def _getLayersStr(self):
        
        if len(self._parts) == 0:
            
            return self._lemma + '@@@' + self._postag + '@@@' + self._word
        
        else:        
            partsArr = []
            for onePart in self._parts:
                partsArr.append( onePart._getLayersStr() )
                
            return '###'.join(partsArr)