import pandas as pd


# Test url extern: http://brievenalsbuit.ato.ivdnt.org/blacklab-server/zeebrieven
AVAILABLE_CORPORA = {'chn':'http://svprmc05.inl.nl/blacklab-server/chn',
                     'opensonar':'http://172.16.10.93:8080/blacklab-server/opensonar',
                     'zeebrieven':'http://svprmc20.ivdnt.org/blacklab-server/zeebrieven',
                     'gysseling':'http://svprmc20.ivdnt.org/blacklab-server/gysseling',
                     'nederlab':''}
AVAILABLE_LEXICA = {'anw':'http://172.16.4.56:8890/sparql', 
                    'celex':'http://172.16.4.56:8890/sparql', 
                    'diamant':'http://svprre02:8080/fuseki/tdb/sparql', 
                    'duelme':'http://172.16.4.56:8890/sparql', 
                    'molex':'http://172.16.4.56:8890/sparql'}

RECORDS_PER_PAGE = 1000

# Fields parsed by default from corpus xml by _parse_xml
# Extra fields can be given to _parse_xml by users
DEFAULT_FIELDS_TOKEN = ["word", "lemma", "universal_dependency"]
DEFAULT_FIELDS_DOC = []

# For UI
DEFAULT_QUERY = r'[lemma="boek"]'
DEFAULT_CORPUS = "chn"
DEFAULT_SEARCHWORD = 'boek'
DEFAULT_LEXICON = "diamant"

# Get rid of ellipsis in display (otherwise relevant data might not be shown)
pd.set_option('display.max_colwidth',1000)