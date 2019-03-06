from chaininglib.search.CorpusQuery import *
from chaininglib.search.LexiconQuery import *
from chaininglib.search.metadata import *
#c = create_corpus("zeebrieven").pattern(r'[lemma="dat"]').extra_fields_doc(["author","witnessYear_from"]).detailed_context(True).search().kwic()
#print(c)
l = create_lexicon("mnwlex").lemma("boek,boef").search().search().search().kwic()
print(l)
#print(get_available_metadata("zeebrieven"))