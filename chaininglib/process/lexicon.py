import chaininglib.utils.dfops as dfops

# beware: just like chaininglib.utils.dfops, this file contains function operating on DataFrames.
# However the functions in this file aim to manipulate DataFrames with lexicon data, 
# whereas the functions in dfops are more general

def get_diamant_synonyms(df):    
    '''
    This function gets lemmata or definitions out of a Pandas DataFrame with Diamant data. 
    The output set content depends on the result type.
    
    Args:
        df: a Pandas DataFrame containing Diamant data
    Returns:
        a set of lemmata OR a set of synonym definitions
        
    >>> df_lexicon = create_lexicon(lexicon).word(search_word).results()
    >>> syns = diamant_get_synonyms(df_lexicon) 
    >>> display( 'Synoniemen voor ' + search_word + ': ' + ", ".join(syns)))
    '''
    
    dfops.check_valid_df("get_diamant_synonyms", df)
    
    # Depending on the result type, we return the lemma or the definition text
    lemmas = set(df[df["inputMode"]=="defText"]["n_ontolex_writtenRep"])
    defTexts = set(df[df["inputMode"]=="lemma"]["n_syndef_definitionText"])
    return lemmas|defTexts
