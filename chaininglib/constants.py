import pandas as pd

# AVAILABLE_CORPORA = {'chn':{'blacklab_url':'https://svprmc05.inl.nl/blacklab-server/chn', 'default_method':'blacklab'},
#                      'opensonar':{'blacklab_url':'https://172.16.10.93:8080/blacklab-server/opensonar', 'default_method':'blacklab'},
#                      'zeebrieven':{'blacklab_url':'https://brievenalsbuit.ato.ivdnt.org/blacklab-server/zeebrieven','default_method':'blacklab'}, # 'https://svprmc20.ivdnt.org/blacklab-server/zeebrieven',
#                      'gysseling':{'blacklab_url':'https://svprmc20.ivdnt.org/blacklab-server/gysseling', 'default_method':'blacklab'},
#                      'nederlab':{'default_method':'fcs'}}

AVAILABLE_CORPORA = {'zeebrieven':{'blacklab_url':'https://corpora.ato.ivdnt.org/blacklab-server/zeebrieven','default_method':'blacklab'},
                     'gysseling':{'blacklab_url':'https://corpora.ato.ivdnt.org/blacklab-server/gysseling', 'default_method':'blacklab'},
                     'openchn': {'blacklab_url':'https://corpora.ato.ivdnt.org/blacklab-server/openchn/', 'default_method': 'blacklab'},
                    'opus': {'blacklab_url':'https://corpora.ato.ivdnt.org/blacklab-server/OPUS','default_method':'blacklab'}}


AVAILABLE_LEXICA = {'anw':{"sparql_url":'https://rdf.ivdnt.org/sparql', "method":"sparql"}, 
                    'celex':{"sparql_url":'https://rdf.ivdnt.org/sparql', "method":"sparql"}, 
                    #'diamant':{"sparql_url":'https://172.16.4.56:8890/sparql', "method":"sparql"}, 
                    'diamant':{"sparql_url":'https://svprre02:8080/fuseki/tdb/sparql', "method":"sparql"}, 
                    #'diamant':{"sparql_url":'https://rdf.ivdnt.org/sparql', "method":"sparql"}, 
                    'duelme':{"sparql_url":'https://rdf.ivdnt.org/sparql', "method":"sparql"}, 
                    'molex':{"sparql_url":'https://rdf.ivdnt.org/sparql', "method":"sparql"},
                    'mnwlex': {"method":"lexicon_service"},
                    'nameslex': {"method":"lexicon_service"},
                    'lexicon_service_db': {"method":"lexicon_service"}}
                    #'lexiconservice_mnw_wnt': {"method":"lexicon_service"}}

    
AVAILABLE_TREEBANKS = {'treebanks_xml':{"treebanks_url":'svowgr01.ivdnt.loc', "method":'basex', "user":"admin", "pass":"admin", "port":1984},
                      'cgn':{"treebanks_url":'https://gretel.ivdnt.org/api/src/router.php', "method":'gretel'},
                      'lassy':{"treebanks_url":'https://gretel.ivdnt.org/api/src/router.php', "method":'gretel'}}

RECORDS_PER_PAGE = 1000
FCS_URL = "https://portal.clarin.inl.nl/fcscorpora/clariah-fcs-endpoints/sru?operation=searchRetrieve&queryType=fcs"
LEXICON_SERVICE_URL = "https://sk.taalbanknederlands.inl.nl/LexiconService/lexicon/_QUERY_TYPE_?case_sensitive=false&tweaked_queries=true"

# Fields parsed by default from corpus xml by _parse_xml
# Extra fields can be given to _parse_xml by users
DEFAULT_FIELDS_TOKEN_FCS = ["word", "lemma", "universal_dependency"]
DEFAULT_FIELDS_DOC_FCS = []

DEFAULT_FIELDS_TOKEN_BL = ["word", "lemma", "pos"]
DEFAULT_FIELDS_DOC_BL = []

# For UI
DEFAULT_QUERY = r'[lemma="boek"]'
DEFAULT_CORPUS = "zeebrieven"
DEFAULT_SEARCHWORD = 'boek'
DEFAULT_LEXICON = "anw"

ENABLE_WAIT_INDICATOR = True

# Get rid of ellipsis in display (otherwise relevant data might not be shown)
pd.set_option('display.max_colwidth',1000)
