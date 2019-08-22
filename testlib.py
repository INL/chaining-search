from chaininglib.search.CorpusQuery import *
from chaininglib.process.corpus import *
from chaininglib.ui.dfui import *

# do some corpus search
print('This can take a few seconds... please wait!')
for one_corpus in get_available_corpora():
    print(one_corpus)
    #c = create_corpus(one_corpus).lemma("woordenboek").detailed_context(True).search()
    #df_corpus = c.kwic()

corpus_to_search="chn-extern"
#corpus_to_search="zeebrieven"
df_corpus = create_corpus(corpus_to_search).detailed_context(True).pos("NOU.*").search().kwic()
print('done here')
# compute and display a table of the frequencies of the lemmata

freq_df = get_frequency_list(df_corpus)
display_df(freq_df)