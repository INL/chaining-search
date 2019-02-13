from chaininglib.search.Query import check_valid_df

def diamant_get_synonyms(df):
    '''
    This function gets lemmata or definitions out of a Pandas DataFrame with Diamant data. 
    The output set content depends on the result type.
    
    Args:
        df: a Pandas DataFrame containing Diamant data
    Returns:
        a set of lemmata OR a set of synonym definitions
        
    >>> query = lexicon_query(word=search_word, pos= '', lexicon=lexicon)
    >>> df_lexicon = search_lexicon(query, lexicon)
    >>> syns = diamant_get_synonyms(df_lexicon) 
    >>> display( 'Synoniemen voor ' + search_word + ': ' + ", ".join(syns)))
    '''
    
    check_valid_df("diamant_get_synonyms", df)
    
    # Depending on the result type, we return the lemma or the definition text
    lemmas = set(df[df["inputMode"]=="defText"]["n_ontolex_writtenRep"])
    defTexts = set(df[df["inputMode"]=="lemma"]["n_syndef_definitionText"])
    return lemmas|defTexts
