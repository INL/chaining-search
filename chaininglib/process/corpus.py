from nltk.tag.perceptron import PerceptronTagger
from chaininglib.utils.dfops import property_freq, df_filter
import pandas as pd
import chaininglib.ui.status as status
import re

# beware: just like chaininglib.utils.dfops, this file contains function operating on DataFrames.
# However the functions in this file aim to manipulate DataFrames with corpus data, 
# whereas the functions in dfops are more general

def get_frequency_list(df_corpus, column_name="lemma"):
    '''
    This function computes the raw frequency of lemmata in a DataFrame containing corpus data

    Args:
        df_corpus: a Pandas DataFrame with corpus data (it must contain at least one 'lemma' column)
    
    Returns:
        a Pandas DataFrame with 'lemmata' as index, 'token count' a number of occurences per lemma, 
        and 'rank' as ordinal position in the list of lemmata, based on the 'token count'.
    
    >>> df_corpus = create_corpus("gysseling").lemma("boef").search().kwic()
    >>> df_freq_list = get_frequency_list(df_corpus)

    '''
    status.show_wait_indicator('Building frequency list')
    
    # get a list of the columns named 'lemma...' 
    all_col_names = list(df_corpus.columns.values)
    lemma_col_names = [x for x in set(all_col_names) if str(x).startswith(column_name)]
    
    if len(lemma_col_names) == 0:
        raise ValueError("function get_frequency_list() was called with a DataFrame which doesn't contain any '%s' column. If needed, rename the relevant column of your DataFrame into '%s'." % (column_name, column_name))
    
    # instantiate a DataFrame with one single column 'lemmata',
    # in which we will gather all single lemmata occurences
    df_lemmata_list = pd.DataFrame()
    
    # loop through the list of lemma-column:
    # For each of them, gather all unique lemmata and add those to the df_lemmata_list DataFrame
    for col_name in lemma_col_names:
        # rename the column in question to 'lemmata', so as to be able to merge this DataFrame with the full list of lemmata
        sub_df_corpus = df_corpus[col_name]
        df_lemmata_list = pd.concat( [df_lemmata_list, sub_df_corpus] )
        
    column_name_plural = column_name + "s"
    df_lemmata_list.columns=[column_name_plural]
        
    # Use the property_freq to compute a frequency list
    df_frequency_list = property_freq(df_lemmata_list, column_name_plural)    
    # set the lemmata column to be the index
    df_frequency_list.set_index(column_name_plural)
    
    # final step: compute ranks
    # this is needed to be able to compare different frequency lists 
    # with each other (which we could achieve by computing a rank diff)
    df_frequency_list['rank'] = df_frequency_list['token count'].rank(ascending = False).astype(int)
    
    status.remove_wait_indicator()
    
    return df_frequency_list



def extract_lexicon(dfs_corpus, lemmaColumnName='lemma', posColumnName='pos', wordformColumnName='word'):
    '''
    This method creates a lexicon from a list of corpus search results. Lemma, POS and word column names from the corpus results are also used for the resulting lexicon
    
    Args:
        dfs_corpus: list of Pandas DataFrames with search results from different corpora
        lemmaColumnName: (default 'lemma') column name for lemma in dfs_corpus
        posColumnName: (default 'pos') column name for part-of-speech in dfs_corpus
        wordformColumnName: (default 'word') column name for word form in dfs_corpus

    Returns:
        a Pandas DataFrame representing a lexicon, with lemmaColumnName, posColumnName and wordformColumnName as columns

    >>> dfs_corpus = [df_results_corpus1, df_results_corpus2]
    >>> lexicon = extract_lexicon(dfs_corpus, lemmaColumnName='lemma', posColumnName='pos', wordformColumnName='word')

    '''
    print("extracting lexicon...")
    
    # Instantiate a DataFrame 
    # in which we will gather the paradigms
    df_lexicon = pd.DataFrame()
    
    # The algorithm expects a list of DataFrames by default, so make sure we have just that
    if isinstance(dfs_corpus, pd.DataFrame):
        dfs_corpus = [dfs_corpus]
        
    for df_corpus in dfs_corpus:
        # Exract the basic layers (lemma, pos, wordform) contained in df_corpus
        column_names = list(df_corpus.columns.values)
        
        for n, val in enumerate(column_names):
            # remove the numbers at the end of the layers names (lemma 1, lemma 2, ..., pos 1, pos 2, ...)
            # so we end up with clean layers name only
            column_names[n] = val.split(' ')[0] 


        # To be able to extract a lexicon, we need at least: lemma, pos, wordform
        # (only lemma and wordform is dangerous, since there can be homonyms with different grammatical categories,
        #  so when grouping them, we would end up with mixed up paradigms)
        if (lemmaColumnName not in set(column_names) or posColumnName not in set(column_names) or wordformColumnName not in set(column_names)):
            print("Skipping corpus. extract_lexicon() expects the Pandas DataFrame input to contain at least these columns: "+lemmaColumnName+", "+posColumnName+" and "+wordformColumnName)
            continue


        # loop through the layers, extract those as temporary DataFrame, 
        # and concat each temporary DataFrame with the main DataFrame to get a full list
        for i in range(0, len(set(column_names)), 1):
            current_lemma = lemmaColumnName+' '+str(i)
            current_pos = posColumnName+' '+str(i)
            current_wordform = wordformColumnName+' '+str(i)
            sub_df_corpus = df_corpus.loc[ : , [current_lemma, current_pos, current_wordform] ]
            sub_df_corpus.columns = [lemmaColumnName, posColumnName, wordformColumnName]

            df_lexicon = pd.concat( [df_lexicon, sub_df_corpus] )

    # set column names
    df_lexicon.columns = [lemmaColumnName, posColumnName, wordformColumnName]
    
    # get rid on illformed lemmata and set it all lowercase
    
    df_lexicon = df_lexicon[ df_lexicon[lemmaColumnName].apply(lambda x: type(x)==str) ]    
    df_lexicon[lemmaColumnName] = df_lexicon[lemmaColumnName].apply(lambda x: x.lower())
    
    df_lexicon = df_lexicon[ df_lexicon[wordformColumnName].apply(lambda x: type(x)==str) ]
    df_lexicon[wordformColumnName] = df_lexicon[wordformColumnName].apply(lambda x: x.lower()) 
    
    df_lexicon = df_lexicon[ df_lexicon[lemmaColumnName].str.contains("^[a-z]+$" ) ]
    
    # make sure each lemma-pos-wordform combination is unique
    df_lexicon = df_lexicon.drop_duplicates()
    df_lexicon = df_lexicon.sort_values(by=[lemmaColumnName, posColumnName])
    df_lexicon = df_lexicon.reset_index(drop=True)
    return df_lexicon



def get_tagger(dfs_corpus, word_key="word", pos_key="universal_dependency"):
    '''
    This function instantiates a tagger trained with some corpus annotations (out of a DataFrame)

    Args:
        dfs_corpus: one (or a list of) Pandas DataFrame(s) with annotated corpus data
        word_key: (default 'word') column name for wordforms in dfs_corpus
        pos_key: (default 'universal_dependency') column name for parts-of-speech in dfs_corpus
    
    Returns:
        a PerceptronTagger instance 
    
    >>> # get a tagger, trained with df_corpus: a Pandas DataFrame with lots of corpus data
    >>> tagger = get_tagger(df_corpus)  
    >>> # tag a sentence now
    >>> sentence = 'Here is some beautiful sentence'
    >>> tagged_sentence = tagger.tag( sentence.split() )
    >>> print(tagged_sentence) 
    
    '''
    
    sentences = []
    
    # The algorithm expects a list of DataFrames by default, so make sure we have just that
    if isinstance(dfs_corpus, pd.DataFrame):
        dfs_corpus = [dfs_corpus]
        
    for df_corpus in dfs_corpus:
    
        # The corpus DataFrame consists of a number of sentences (rows) with a fixed number of tokens.
        # Each token has a fixed number of layers holding info like: lemma, wordform or part-of-speech. 
        # As a result, the number of columns of each row = [number of tokens] x [number of layers]

        # To be able to feed the tagger correctly, we need to compute the number of layers,
        # so we can infer the number of tokens the sentences hold. This is because
        # the tagger expects us to feed it with arrays with length = [number of tokens], as elements of
        # one single array holding all sentences arrays (see below).

        # So, determine how many layers (lemma, pos, wordform) we have 
        column_names = list(df_corpus.columns.values)
        for n, val in enumerate(column_names):
            # remove the numbers at the end of the layers names (lemma 1, lemma 2, ..., pos 1, pos 2, ...)
            # so we end up with clean layers name only
            column_names[n] = val.split(' ')[0] 
        number_of_layers = len(set(column_names))

        # Now we can determine the standard length of our corpus sentences: that can be computed 
        # by dividing the number of columns of the corpus DataFrame by the number of layers
        # we just computed.

        nr_of_words_per_sentence = int( df_corpus.shape[1] / number_of_layers )  

        # Build training data for the tagger in the right format
        # The input must be like: [ [('today','NN'),('is','VBZ'),('good','JJ'),('day','NN')], [...] ]
        for index, row in df_corpus.iterrows():
            one_sentence =  []
            wrong = False
            for i in range(0, nr_of_words_per_sentence, 1):
                word_idx = word_key+' '+str(i)
                pos_idx = pos_key+' '+str(i)
                try:
                    tuple = ( row[word_idx], _cut_off_features(row[pos_idx]) )
                    one_sentence.append( tuple )
                    if (row[word_idx] is None or row[pos_idx] is None):
                        wrong = True
                except:
                    raise ValueError("function get_tagger() expects corpus data with columns '%s' and '%s', but those columns could not be found. Please call the function with these extra paramters to declare which column your corpus data has instead: get_tagger(word_key='...', pos_key='...')." % (word_key, pos_key))
            if wrong is False:
                sentences.append(one_sentence)
                
    # Instantiate and train the tagger now
    tagger = PerceptronTagger(load=False)
    tagger.train(sentences)
    
    return tagger


def _cut_off_features(pos_with_features):
    '''
    This function cuts off features from tags with features attached
    '''
    return re.sub('^([A-Z-]+)(|\\(.+\\))$', r'\1', pos_with_features) 