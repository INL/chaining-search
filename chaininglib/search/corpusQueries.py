def corpus_query(lemma=None, word=None, pos=None):
    '''
    This function builds a query for getting occurances of a given lemma within a given corpus
    Args:
        lemma: a lemma to look for
        word: word form to look for
        pos: POS tag to look for
    Returns:
        a corpus query string
        
    >>> lemma_query = corpus_query(lemma="lopen")
    >>> df_corpus = create_corpus("chn").pattern(lemma_query).kwic()
    >>> display(df_corpus)
    '''
    
    parts = []
    
    if lemma is not None:
        parts.append( r'lemma="'+ lemma + r'"' )
    if word is not None:
        parts.append( r'word="'+ word + r'"' )
    if pos is not None:
        parts.append( r'pos="'+ pos + r'"' )
    
    return r'[' + r' & '.join(parts) + r']'


