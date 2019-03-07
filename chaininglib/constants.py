import pandas as pd

# AVAILABLE_CORPORA = {'chn':{'blacklab_url':'http://svprmc05.inl.nl/blacklab-server/chn', 'default_method':'blacklab'},
#                      'opensonar':{'blacklab_url':'http://172.16.10.93:8080/blacklab-server/opensonar', 'default_method':'blacklab'},
#                      'zeebrieven':{'blacklab_url':'http://brievenalsbuit.ato.ivdnt.org/blacklab-server/zeebrieven','default_method':'blacklab'}, # 'http://svprmc20.ivdnt.org/blacklab-server/zeebrieven',
#                      'gysseling':{'blacklab_url':'http://svprmc20.ivdnt.org/blacklab-server/gysseling', 'default_method':'blacklab'},
#                      'nederlab':{'default_method':'fcs'}}

AVAILABLE_CORPORA = {'zeebrieven':{'blacklab_url':'http://brievenalsbuit.ato.ivdnt.org/blacklab-server/zeebrieven','default_method':'blacklab'},
                     'gysseling':{'blacklab_url':'http://brievenalsbuit.ato.ivdnt.org/blacklab-server/gysseling', 'default_method':'blacklab'}}


AVAILABLE_LEXICA = {'anw':{"sparql_url":'http://172.16.4.56:8890/sparql', "method":"sparql"}, 
                    'celex':{"sparql_url":'http://172.16.4.56:8890/sparql', "method":"sparql"}, 
                    'diamant':{"sparql_url":'http://svprre02:8080/fuseki/tdb/sparql', "method":"sparql"}, 
                    'duelme':{"sparql_url":'http://172.16.4.56:8890/sparql', "method":"sparql"}, 
                    'molex':{"sparql_url":'http://172.16.4.56:8890/sparql', "method":"sparql"},
                    'mnwlex': {"method":"lexicon_service"},
                    'lexicon_service_db': {"method":"lexicon_service"}}
                    #'lexiconservice_mnw_wnt': {"method":"lexicon_service"}}

RECORDS_PER_PAGE = 1000
FCS_URL = "http://portal.clarin.inl.nl/fcscorpora/clariah-fcs-endpoints/sru?operation=searchRetrieve&queryType=fcs"
LEXICON_SERVICE_URL = "http://sk.taalbanknederlands.inl.nl/LexiconService/lexicon/get_wordforms?case_sensitive=false&tweaked_queries=true"

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
DEFAULT_LEXICON = "diamant"

ENABLE_WAIT_INDICATOR = True

# Get rid of ellipsis in display (otherwise relevant data might not be shown)
pd.set_option('display.max_colwidth',1000)