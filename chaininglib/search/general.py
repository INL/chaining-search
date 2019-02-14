import xml.etree.ElementTree as ET

def get_available_metadata(resource_name, resource_type=None):
    import chaininglib.constants as constants
    from chaininglib.search.corpus import _corpus_metadata_blacklab
    from chaininglib.search.lexicon import _metadata_from_lexicon_query
    
    '''
    Return all possible metadata fields for a lexicon or corpus
    
    Args:
        resource_name: Name of the lexicon or corpus
        resource_type: (optional) One of 'lexicon' or 'corpus'. Can be used to disambiguate when resource name can be both a lexicon or corpus
    Returns:
        A list of metadata fields
    '''
    
    # Infer resource type from name
    if resource_name in constants.AVAILABLE_CORPORA and resource_name not in constants.AVAILABLE_LEXICA:
        res_type = "corpus"
    elif resource_name in constants.AVAILABLE_LEXICA and resource_name not in constants.AVAILABLE_CORPORA:
        res_type = "lexicon"
    elif resource_name in constants.AVAILABLE_LEXICA and resource_name in constants.AVAILABLE_CORPORA:
        if resource_type is not None:
            res_type = resource_type
        else:
            raise ValueError("Resource " + resource_name + " can be a corpus or lexicon. Please specify the resource_type.")
    else:
        raise ValueError("Resource " + resource_name + " not found.")
    
    
    if res_type=="lexicon":
        # Create sample query for this lexicon
        q = lexicon_query(word="", pos="", lexicon=resource_name)
        return _metadata_from_lexicon_query(q)
    elif res_type=="corpus":
        if resource_name in constants.AVAILABLE_CORPORA and resource_name != "nederlab":
            return _corpus_metadata_blacklab(resource_name)
        elif corpus_name=="nederlab":
            print("Corpus metadata not yet available for Nederlab")
            return []
    else:
        raise ValueError("resource_type should be 'corpus' or 'lexicon'.")