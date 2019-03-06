import re

def treebank_query(lemma=None, word=None, pos=None):
    '''
    This function builds a query for getting occurances of a given lemma within a treebank

    Args:
        lemma: a lemma to look for
        word: wordform to look for
        pos: POS tag to look for
        
    Returns:
        a treebank query string
        
    >>> tb = create_treebank().word("kat")
    >>> df_trees = tb.search().kwic()
    >>> display(df_trees)
    '''
    
    parts = []
    
    if lemma is not None:
        parts.append( r'@root="'+ lemma + r'"' )
    if word is not None:
        parts.append( r'@word="'+ word + r'"' )
        
    # if no features are provided, we need to query for pos in 'pt', with the query string in lower case
    # but if we do have features, we'll be searching for pos in 'postag' (no need for lower case there)
    
    if pos is not None:
        if (re.match("^[A-Za-z]+$", pos)):
            parts.append( r'@pt="'+ pos.lower() + r'"' )
        else:
            parts.append( r'@postag="'+ pos + r'"' )
            
    return r'xquery //node[' + r' and '.join(parts) + r']'


