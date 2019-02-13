from chaininglib.search import CorpusQuery
from chaininglib.search import LexiconQuery

def check_valid_df(function_name, obj):
    if type(obj) is CorpusQuery or type(obj) is LexiconQuery:
        raise ValueError(function_name+"() was called with a " + str(type(obj))+ " object. Hint: call " + str(type(obj))+ ".results().")