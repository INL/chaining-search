from chaininglib.ui.search import create_corpus_ui
from chaininglib.ui.dfui import display_df
from chaininglib.search.CorpusQuery import *
import chaininglib.constants as constants


def add_corpus(name, config):
  constants.AVAILABLE_CORPORA[name] = config

add_corpus('ja_nl', {'blacklab_url':'http://corpora.ato.ivdnt.org/blacklab-server//JapansNederlands','default_method':'blacklab'})
add_corpus('gysseling', {'blacklab_url':'http://corpusgysseling.ivdnt.org/blacklab-server/Gysseling','default_method':'blacklab'})
corpus_name='zeebrieven'

def test_ja_nl():
  corpus_name='ja_nl'
  corpus_name='gysseling'
  query='([pos="Verb.*" & lemma != "する"]|[pos="Noun.*"][lemma="する"]) within (<sentence/> (<s/> containing [lemma="vernietigen"]))'
  # corpus_searched = create_corpus(corpus_name).pattern(query).group_by(["field:genre:i"]).max_results(1000).search()
  corpus_searched = create_corpus(corpus_name).group_by(["field:genre:i"]).max_results(100).search()
  df_corpus = corpus_searched.kwic()
  summary = corpus_searched.summary()
  print(summary)
  print(df_corpus.to_string())
  print(summary)

test_ja_nl()
#df_corpus = create_corpus(corpus_name).pattern("[lemma='kapitein']").group_by(["hit:word:i","field:datum_jaar:i"]).max_results(1000).search().kwic()
