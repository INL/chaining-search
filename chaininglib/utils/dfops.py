import pandas as pd


# beware: just like the files in chaininglib.process, this file contains function operating on DataFrames.
# However the functions in this file are general in the sense that they don't specifically aim at manipulating
# corpus or lexicon data.  
# On the contrary, the functions in chaininglib.process do aim to manipulate corpus or lexicon data, so those
# function don't belong in this general section.


def check_valid_df(function_name, obj):
    '''
    This function is called by others to check if input is a DataFrame, when it is expected!
    If the input does not contain a DataFrame, throw an error

    Args:
        function_name: the name of the function, so as to be able to show where an error occured
        obj: the object to be checked

    Returns:
        N/A
    '''
    if not (isinstance(obj, pd.DataFrame) or isinstance(obj, pd.Series)):
        raise ValueError(function_name+"() requires a Pandas DataFrame as argument. You might have forgotten to use object.kwic().")

        
        
def property_freq(df, column_name):
    '''
    Count values for a certain property in a results DataFrame, and sort them by frequency

    Args:
        df: DataFrame with results, one row per found token
        column_name: Column name (property) to count

    Returns:
        a DataFrame of the most values for this property, sorted by frequency. 
        Column 'token count' contains the number of tokens, column 'perc' gives the percentage.
    '''
    
    # classic group by + count, just like in SQL
    df = df.groupby(column_name).size()
    
    # the new column with the counts is given the name "token count"
    # and we set a new sequential index 
    df = df.reset_index(name="token count")
    
    # sort by count, with the highest on top
    df = df.sort_values("token count", ascending=False)
    
    # set a new sequential index again
    # (the drop parameter makes sure the old index is NOT added as a column)
    df = df.reset_index(drop=True)
    
    # compute percentage for each 
    total = df.sum(numeric_only=True, axis=0)
    df["perc"] = df["token count"] / total.iloc[0]
    return df




def df_filter(df_column, pattern, method='contains'):    
    '''
    Helper function to build some condition to filter a Pandas DataFrame, 
    given a column and some value(s) to filter this column with
    
    Args:
        df_column: a Pandas DataFrame column to filter on
        pattern: string, set or interval list to filter on
        method: "contains", "match", isin" or "interval"

    Returns:
        a condition
        
    >>> words_ending_with_e = df_filter( df_lexicon["wordform"], 'e$' )
    >>> df_lexicon_final_e = df_lexicon[ words_ending_with_e ]
    '''
    
    if method=="contains":
        if not isinstance(pattern,str):
            raise ValueError("df_filter 'contains' method needs string as pattern.")
        condition = df_column.str.contains(pattern, na=False)    
    elif method=="match":
        if not isinstance(pattern,str):
            raise ValueError("df_filter 'match' method needs string as pattern.")
        condition = df_column.str.match(pattern, na=False)  
    elif method=="isin":
        if not isinstance(pattern,set):
            raise ValueError("df_filter 'isin' method needs set as pattern.")
        condition = df_column.isin(pattern)
    elif method=="interval":
        if not (isinstance(pattern, list) and len(pattern)==2):
            raise ValueError("df_filter 'interval' method needs a list consisting of a lower and upper boundary as pattern.")
        val_from = pattern[0]
        val_to = pattern[1]
        if val_from is None and val_to is None:
            raise ValueError("Lower boundary or upper boundary of interval should be given.")
        col_numeric = df_column.astype('int32')
        if val_from:
            condition_from = (col_numeric >= int(val_from))
            condition = condition_from
        if val_to:
            condition_to = (col_numeric <= int(val_to))
            condition = condition_to
        if val_from and val_to:
            condition = condition_from & condition_to
    else:
        raise ValueError("Choose one of 'contains', 'match', 'isin' or 'interval' as method for df_filter.")
        
    return condition


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
    
    set_df1 = set(df_column1)
    set_df2 = set(df_column2)
    diff_left = set_df1.difference(set_df2)
    diff_right = set_df2.difference(set_df1)
    intersec = set_df1.intersection(set_df2)
    return diff_left, diff_right, intersec
   

    
def get_rank_diff(df1, df2):    
    '''
    This function compares the rankings of words common to two dataframes, and compute a rank_diff, in such
    a way that one can see which words are very frequent in one set and rare in the other.
    
    Args:
        df1: a Pandas DataFrame provided with rankings stored in a column "rank"
        df2: a Pandas DataFrame provided with rankings stored in a column "rank"
        
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
    
    limited_df1['rank'] = limited_df1['token count'].rank(ascending = False).astype(int)
    limited_df2['rank'] = limited_df2['token count'].rank(ascending = False).astype(int)
    
    # Instantiate a dataframe for storing lemmata and rank diffs
    df_rankdiffs = pd.DataFrame(index=common_lemmata_list, columns=['rank_1', 'rank_2', 'rank_diff'])
    df_rankdiffs.index.name = 'lemmata'
    
    df_rankdiffs['rank_1'] = limited_df1['rank']
    df_rankdiffs['rank_2'] = limited_df2['rank']
    df_rankdiffs['rank_diff'] = pd.DataFrame.abs( df_rankdiffs['rank_1'] - df_rankdiffs['rank_2'] )
    
    return df_rankdiffs
