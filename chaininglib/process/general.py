
from chaininglib.queries import containsRegex, lexicon_query
from chaininglib.search.lexicon import search_lexicon_all, search_lexicon
from chaininglib.search.corpus import search_corpus
from chaininglib.search.Query import check_valid_df
from chaininglib.search.CorpusQuery import *
from chaininglib.search.LexiconQuery import *

import numpy as np
import pandas as pd

def property_freq(df, column_name):
    '''
    Count values for a certain property in a results DataFrame, and sort them by frequency
    Args:
        df: DataFrame with results, one row per found token
        column_name: Column name (property) to count
    Returns:
        a DataFrame of the most values for this property, sorted by frequency. Column 'token count' contains the number of tokens, column 'perc' gives the percentage.
    '''
    df = df.groupby(column_name).size().reset_index(name="token count").sort_values("token count",ascending=False).reset_index(drop=True)
    total = df.sum(numeric_only=True, axis=0)
    df["perc"] = df["token count"] / total.iloc[0]
    return df

def df_filter(df_column, regex_or_set, method='contains'):
    '''
    Helper function to build some condition to filter a Pandas DataFrame, 
    given a column and some value(s) to filter this column with
    
    Args:
        df_column: a Pandas DataFrame column to filter on
        regex_or_set: a regular expression or a list 
        method: "contains" or "isin"
    Returns:
        a condition
        
    >>> words_ending_with_e = df_filter( df_lexicon["wordform"], 'e$' )
    >>> df_lexicon_final_e = df_lexicon[ words_ending_with_e ]
    '''
    check_valid_df("df_filter", df_column)
    
    if method=="contains":
        filter_condition = df_column.str.contains(regex_or_set)    
    elif method=="isin":
        filter_condition = df_column.isin(regex_or_set)
    else:
        raise ValueError("Choose one of 'contains' or 'isin' as method for df_filter.")
        
    return filter_condition


def join_df(df_arr, join_type=None):
    
    '''
    This function joins two dataframes (=concat along axis 1) 
    Args:
        df_arr: array of Pandas DataFrames
        join_type: {inner, outer (default)}
    Returns:
        a single Pandas DataFrame 
        
    >>> new_df = join_df( [dataframe1, dataframe2] )
    >>> display_df(new_df)
    '''
    
    # ref: https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
    
    if join_type is None:
        concat_df = pd.concat( df_arr, axis=1 )
    else:
        concat_df = pd.concat( df_arr, axis=1, join=join_type )
    
    return concat_df

def column_difference(df_column1, df_column2):
    '''
    This function computes differences and similarities between two Pandas DataFrames
    Args:
        df_column1: a Pandas DataFrame, filtered by one column
        df_column2: a Pandas DataFrame, filtered by one column
    Returns:
        diff_left: array of words only in df_column1
        diff_right: array of words only in df_column2
        intersec: array of words both in df_column1 and df_column2
        
    >>> diff_left, diff_right, intersec = column_difference(df_corpus1["word 1"], df_corpus2["word 1"])
    >>> display( 'These words are only in DataFrame #1 : ' + ", ".join(diff_left) )
    >>> display( 'These words are only in DataFrame #2 : ' + ", ".join(diff_right) )
    >>> display( 'These words are common to both DataFrame : ' + ", ".join(intersec) )
    '''
    
    check_valid_df("column_difference", df_column1)
    check_valid_df("column_difference", df_column2)
    
    set_df1 = set(df_column1)
    set_df2 = set(df_column2)
    diff_left = set_df1.difference(set_df2)
    diff_right = set_df2.difference(set_df1)
    intersec = set_df1.intersection(set_df2)
    return diff_left, diff_right, intersec
    

    
### Joint operations between corpus and lexicon

def get_frequency_list(lexicon, pos, corpus):
    '''
    This function builds a lemmata frequency list of a corpus, 
    given a lexicon (for obvious reasons limited to some part-of-speech).
    
    Args:
        lexicon: a lexicon name
        pos: a part-of-speech to limit the search to
        corpus: the corpus to be searched
    Returns:
        a Pandas DataFrame with raw frequencies ('raw_freq' column) and rankings ('rank' column)
        
    >>> df_frequency_list = get_frequency_list(some_lexicon, "NOUN", corpus_to_search)
    >>> display(df_frequency_list)
    '''
    
    print('Beware: building a frequency list can take a long time')
    
    # LEXICON: get a lemmata list to work with
    lq = lexicon(lexicon_name).pos(pos)
    df_lexicon = lq.results()
    lexicon_lemmata_set = sorted( set([w.lower() for w in df_lexicon["writtenForm"]]) )
    lexicon_lemmata_arr= np.array(lexicon_lemmata_set)

    # instantiate a dataframe for storing lemmata and frequencies
    df_frequency_list = pd.DataFrame(index=lexicon_lemmata_arr, columns=['raw_freq'])
    df_frequency_list.index.name = 'lemmata'

    # CORPUS: loop through lemmata list, query the corpus with that lemma, and count the results

    # It's a good idea to work with more than one lemma at once!
    nr_of_lemmata_to_query_atonce = 100
    
    # loop over lemmata list 
    for i in range(0, len(lexicon_lemmata_set), nr_of_lemmata_to_query_atonce):
        # slice to small sets of lemmata to query at once
        small_lemmata_set = set( lexicon_lemmata_arr[i : i+nr_of_lemmata_to_query_atonce] )    

        # join set of lemmata to send them in a query all at once
        # beware: single quotes need escaping
        lemmata_list = "|".join(small_lemmata_set).replace("'", "\\\\'")
        cq = corpus(corpus_name).pattern(r'[lemma="' + lemmata_list + r'"]')
        df_corpus = cq.results()

        # store frequencies
        if (len(df_corpus)>0):
            for one_lemma in small_lemmata_set: 
                raw_freq = len(df_corpus[df_corpus['lemma 0'] == one_lemma])
                df_frequency_list.at[one_lemma, 'raw_freq'] = raw_freq 
                
    # final step: compute rank
    # this is needed to be able to compare different frequency lists 
    # with each other (which we could achieve by computing a rank diff)
    df_frequency_list['rank'] = df_frequency_list['raw_freq'].rank(ascending = False).astype(int)
    
    return df_frequency_list;


def get_missing_wordforms(lexicon, pos, corpus):    
    '''
    This function gathers all paradigms of a lexicon with a given part-of-speech
    and searches an annotated corpus for words missing in those paradigms
    
    Args:
        lexicon: a lexicon name
        pos: a part-of-speech to limit the search to
        corpus: the corpus to be searched
    Returns:
        a Pandas DataFrame associating lemmata to their paradigms ('known_wordforms' column) and
        missing wordforms found in the corpus ('unknown_wordforms' column).
        
    >>> df = get_missing_wordforms("molex", "VERB", "opensonar")
    >>> df.to_csv( "missing_wordforms.csv", index=False)
    '''
    
    print('Beware: finding missing wordforms in a lexicon can take a long time');
    
    # LEXICON: get a lemmata list to work with
    lq = lexicon(lexicon_name).pos(pos)
    df_lexicon = lq.results()
    lexicon_lemmata_set = sorted( set([w.lower() for w in df_lexicon["writtenForm"]]) )
    lexicon_lemmata_arr= np.array(lexicon_lemmata_set)
    
    # instantiate a dataframe for storing lemmata and wordforms
    df_enriched_lexicon = pd.DataFrame(index=lexicon_lemmata_arr, columns=['lemma', 'pos', 'known_wordforms', 'unknown_wordforms'])
    df_enriched_lexicon.index.name = 'lemmata'
    
    # CORPUS: loop through lemmata list, query the corpus with that lemma, 
    # and compute difference between both

    # It's a good idea to work with more than one lemma at once!
    nr_of_lemmata_to_query_atonce = 100
    
    # loop over lemmata list 
    for i in range(0, len(lexicon_lemmata_set), nr_of_lemmata_to_query_atonce):
        # slice to small sets of lemmata to query at once
        small_lemmata_set = set( lexicon_lemmata_arr[i : i+nr_of_lemmata_to_query_atonce] )    
        
        # join set of lemmata to send them in a query all at once
        # beware: single quotes need escaping
        lemmata_list = "|".join(small_lemmata_set).replace("'", "\\\\'")
        cq = corpus(corpus_name).pattern(r'[lemma="' + lemmata_list + r'"]')
        df_corpus = cq.results()
        
        # process results
        if (len(df_corpus)>0):
            for one_lemma in small_lemmata_set: 
                
                # look up the known wordforms in the lexicon
                query = lexicon_query(one_lemma, pos, lexicon)
                df_known_wordforms = search_lexicon(query, lexicon)
                
                if (len(df_known_wordforms) != 0):
                    known_wordforms = set( df_known_wordforms['wordform'].str.lower() )
                    # find the wordforms in the corpus
                    corpus_wordforms = set( (df_corpus[df_corpus['lemma 0'] == one_lemma])['word 0'].str.lower() )
                    # determine which corpus wordforms are not in lexicon wordforms
                    unknown_wordforms = corpus_wordforms.difference(known_wordforms)

                    if (len(unknown_wordforms) !=0):
                        # store the results
                        df_enriched_lexicon.at[one_lemma, 'lemma'] = one_lemma
                        df_enriched_lexicon.at[one_lemma, 'pos'] = pos
                        df_enriched_lexicon.at[one_lemma, 'known_wordforms'] = known_wordforms
                        df_enriched_lexicon.at[one_lemma, 'unknown_wordforms'] = unknown_wordforms
                
    # return non-empty results, t.i. cases in which we found some wordforms
    return df_enriched_lexicon[ df_enriched_lexicon['unknown_wordforms'].notnull() ]
        
    
def get_rank_diff(df1, df2):
    '''
    This function compares the rankings of words common to two dataframes, and compute a rank_diff, in such
    a way that one can see which words are very frequent in one set and rare in the other.
    
    Args:
        df1: a Pandas DataFrame
        df2: a Pandas DataFrame
    Returns:
        a Pandas DataFrame with lemmata (index), ranks of both input dataframes ('rank_1' and 'rank_2' columns) 
        and the rank_diff ('rank_diff' column).
        
    >>> df_frequency_list1 = get_frequency_list(base_lexicon, "NOUN", corpus_to_search1)
    >>> df_frequency_list2 = get_frequency_list(base_lexicon, "NOUN", corpus_to_search2)
    >>> df_rankdiffs = get_rank_diff(df_frequency_list1, df_frequency_list2)
    '''
    
    check_valid_df("get_rank_diff", df1)
    check_valid_df("get_rank_diff", df2)
    
    # Find lemmata shared by both dataframes: computing ranks diffs is only possible
    # when dealing with lemmata which are in both frames
    lemmata_list1 = set(df1.index.tolist())
    lemmata_list2 = set(df2.index.tolist())
    common_lemmata_list = list( lemmata_list1.intersection(lemmata_list2) )
    
    # Build dataframes limited to the common lemmata
    limited_df1 = df1.loc[ common_lemmata_list , : ]
    limited_df2 = df2.loc[ common_lemmata_list , : ]
    
    # Recompute ranks in both dataframes, because in each frame the original ranks were
    # computed with a lemmata list which might be larger than the lemmata list common
    # to both dataframes
    
    limited_df1['rank'] = limited_df1['raw_freq'].rank(ascending = False).astype(int)
    limited_df2['rank'] = limited_df2['raw_freq'].rank(ascending = False).astype(int)
    
    # Instantiate a dataframe for storing lemmata and rank diffs
    df_rankdiffs = pd.DataFrame(index=common_lemmata_list, columns=['rank_1', 'rank_2', 'rank_diff'])
    df_rankdiffs.index.name = 'lemmata'
    
    df_rankdiffs['rank_1'] = limited_df1['rank']
    df_rankdiffs['rank_2'] = limited_df2['rank']
    df_rankdiffs['rank_diff'] = pd.DataFrame.abs( df_rankdiffs['rank_1'] - df_rankdiffs['rank_2'] )
    
    return df_rankdiffs
