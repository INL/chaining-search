from chaininglib.search.LexiconQuery import *
from chaininglib.search.CorpusQuery import *
import numpy as np

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
    lq = create_lexicon(lexicon).pos(pos)
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
        cq = create_corpus(corpus).pattern(r'[lemma="' + lemmata_list + r'"]')
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
    lq = create_lexicon(lexicon).pos(pos)
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
        cq = create_corpus(corpus).pattern(r'[lemma="' + lemmata_list + r'"]')
        df_corpus = cq.results()
        
        # process results
        if (len(df_corpus)>0):
            for one_lemma in small_lemmata_set: 
                
                # look up the known wordforms in the lexicon
                ql = create_lexicon(lexicon).lemma(one_lemma).pos(pos)
                df_known_wordforms = ql.results()
                
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
        
    
