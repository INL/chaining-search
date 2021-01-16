from chaininglib.ui.search import create_corpus_ui
from chaininglib.ui.dfui import display_df
from chaininglib.search.CorpusQuery import *
import chaininglib.constants as constants
import re
import random

def add_corpus(name, config):
  constants.AVAILABLE_CORPORA[name] = config

add_corpus('ja_nl', {'blacklab_url':'http://corpora.ato.ivdnt.org/blacklab-server//JapansNederlands',
                     'default_method':'blacklab'})
add_corpus('chn_i', {'blacklab_url':'http://svotmc10.ivdnt.loc/blacklab-server/chn',
                     'default_method':'blacklab'})

corpus_name='zeebrieven'

def test_zeebrieven():
  corpus_name='zeebrieven'
  df_corpus = create_corpus(corpus_name).pattern("[lemma='kapitein']").group_by(["hit:word:i"]).max_results(1000).search().kwic()
  display_df(df_corpus)

def test_ja_nl():
  corpus_name='ja_nl'
  query='([pos="Verb.*" & lemma != "する"]|[pos="Noun.*"][lemma="する"]) within (<sentence/> (<s/> containing [lemma="vernietigen"]))'
  df = create_corpus(corpus_name).pattern(query).group_by(["hit:lemma:i"]).max_results(1000).search().kwic()
  display_df(df)
  plot_df(df,'identityDisplay', ['hits_per_million'])

def test_openchn(query):
  corpus = create_corpus('openchn')
  #query = "[lemma='de']"
  grouping = ['field:witnessYear_from:i']
  df = corpus.pattern(query).group_by(grouping).max_results(1000000000).search().kwic()
  display_df(df)
  plot_df(df,'identityDisplay', ['hits_per_million'])
  return df

def search_and_group(corpus_name,query, field, filter=None, validity_filter="^[0-9]{4}$"):
  corpus = create_corpus(corpus_name)
  if not filter == None:
    corpus=corpus.metadata_filter(filter)
  
  grouping = ['field:' + field + ':i']
  df = corpus.pattern(query).group_by(grouping).max_results(1000000000).search().kwic()
  
  if not validity_filter == None: # remove some data noise (non-wellformed dates etc)
     df = df[df.apply(lambda x:  re.match(validity_filter, x['identityDisplay']) != None, axis=1)]
  return df

# disable caching for query by adding a random clause 
def obfuscate(query):
  return query.replace("]", " | lemma='gna_gna_" + str(random.randint(0,1000000)) +  "']")

# simulate grouping by separate querying for each value
def silly_grouping(corpus_name, query, field, values):
    result_frames = list(map(lambda value: search_and_group(corpus_name, obfuscate(query), field, filter={field: value}, validity_filter="^[0-9]{4}$"), values))
    concatenation =  pd.concat(result_frames)
    display_df(concatenation)
    plot_df(concatenation, 'identityDisplay', 'hits_per_million')

def flatten(l):
    return [item for sublist in l for item in sublist]

def merge_frames(frames, key_field, display_field):
    merged_frame = frames[0].rename(columns={display_field: display_field + '_0'})
    for i in range(1,len(frames)):
        #print('merging:' + str(i))
        renamed_frame=frames[i].rename(columns={display_field: display_field + '_' + str(i)})
        merged_frame = pd.merge(merged_frame,renamed_frame,on=key_field,how='outer')
    return merged_frame

def search_and_group_multiple(corpus_name, queries, grouping_field, filter=None, validity_filter="^[0-9]{4}$"):
  dataframes = list(map(lambda x: search_and_group(corpus_name, x, grouping_field, filter, validity_filter), queries))

  #join the frames
  field_to_show = 'hits_per_million'
  merged = merge_frames(dataframes,'identityDisplay', field_to_show)
  
  rename_columns = {}
  for i in range(0,len(queries)):
    rename_columns[field_to_show + '_' + str(i)] = queries[i]
  renamed_frame = merged.rename(columns=rename_columns)
  
  #display_df(renamed_frame)
  plot_df(renamed_frame, 'identityDisplay', y_columns=queries  )
  return zip(queries,dataframes)
    

def plot_df(df,x_column, y_columns):
    #df_values = df[y_column].apply(lambda x: int(x))
    dfsorted = df.sort_values(by=[x_column])
    dfsorted.plot.line(x_column, y_columns, figsize=[30,15])
  
