from chaininglib.ui.search import create_corpus_ui
from chaininglib.ui.dfui import display_df
from chaininglib.search.CorpusQuery import *
import chaininglib.constants as constants
from chaininglib.constants import add_corpus
import re
import random
from IPython.core.display import HTML

#def add_corpus(name, config):
#  constants.AVAILABLE_CORPORA[name] = config

add_corpus('ja_nl', {'blacklab_url':'http://corpora.ato.ivdnt.org/blacklab-server//JapansNederlands',
                     'default_method':'blacklab'})
add_corpus('chn_i', {'blacklab_url':'http://svotmc10.ivdnt.loc/blacklab-server/chn-intern',
                     'default_method':'blacklab'})
add_corpus('zeebrieven_i', {'blacklab_url':'http://svotmc10.ivdnt.loc/blacklab-server/zeebrieven',
                     'default_method':'blacklab'})
add_corpus('gysseling', {'blacklab_url':'http://corpusgysseling.ivdnt.org/blacklab-server/Gysseling',
                     'default_method':'blacklab'})
add_corpus('wablieft', {'blacklab_url':'http://pcob67:8080/blacklab-server/Wablieft',
                     'default_method':'blacklab'})
add_corpus('opensonar', {'blacklab_url':'http://svotmc10.ivdnt.loc/blacklab-server/opensonar',
                     'default_method':'blacklab'})



corpus_name='zeebrieven'

def opus_lemma_query(lemma):
    corpus_searched = create_corpus('wablieft')
    df_lemma = corpus_searched.pattern("<s/> containing [lemma='" + lemma + "']").search().kwic()
    df_lemma.to_csv("/tmp/" + lemma + ".csv",sep="\t")
    #display_df(df_lemma)


opus_lemma_query('krokodil')
