from nltk.tag.perceptron import PerceptronTagger


def get_tagger(df_corpus, word_key="word", pos_key="universal_dependency"):
    '''
    This function instantiates a tagger trained with some corpus annotations 
    Args:
        df_corpus: Pandas DataFrame with annotated corpus data
    Returns:
        a PerceptronTagger instance 
    
    >>> tagger = get_tagger(df_corpus)  # df_corpus containes a Pandas DataFrame with lots of corpus data
    >>> sentence = 'Here is some beautiful sentence'
    >>> tagged_sentence = tagger.tag( sentence.split() )
    >>> print(tagged_sentence) 
    
    '''
    
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
    sentences = []
    nr_of_words_per_sentence = int( df_corpus.shape[1] / number_of_layers )  

    # Build training data for the tagger in the right format
    # The input must be like: [ [('today','NN'),('is','VBZ'),('good','JJ'),('day','NN')], [...] ]
    for index, row in df_corpus.iterrows():
        one_sentence =  []
        wrong = False
        for i in range(0, nr_of_words_per_sentence, 1):
            word_idx = word_key+' '+str(i)
            pos_idx = pos_key+' '+str(i)
            tuple = ( row[word_idx], row[pos_idx] )
            one_sentence.append( tuple )
            if (row[word_idx] is None or row[pos_idx] is None):
                wrong = True
        if wrong is False:
            sentences.append(one_sentence)

    # Instantiate and train the tagger now
    tagger = PerceptronTagger(load=False)
    tagger.train(sentences)
    
    return tagger