from chaininglib.search.CorpusQuery import *
from chaininglib.search.metadata import *
#m={}
#c = create_corpus("zeebrieven").pattern(r'[lemma="dat"]').method("fcs").extra_fields_doc(["author","witnessYear_from"]).detailed_context(False).metadata_filter(m).search().xml()
#print(c)

print(get_available_metadata("zeebrieven"))