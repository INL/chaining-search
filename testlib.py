from chaininglib.search.CorpusQuery import *

c = create_corpus("zeebrieven").pattern(r'[lemma="dat"]').method("blacklab").extra_fields_doc(["author", "title"]).results()
print(c)