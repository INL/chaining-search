import xml.etree.ElementTree as ET
import chaininglib.constants as constants
import re
import requests


def get_available_metadata(resource_name, resource_type=None):   
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
        
        
        
        
def _corpus_metadata_blacklab(corpus_name):
    '''
    Return all possible metadata fields for a BlackLab-based corpus, by sending a request to the corpus
    
    Args:
        corpus_name: Name of the corpus
    Returns:
        A dictionary of with lists of document and token metadata
    '''
    corpus_url = constants.AVAILABLE_CORPORA[corpus_name]
    response = requests.get(corpus_url)
    response_text = response.text  
    return _parse_blacklab_metadata(response_text)


# TODO: Method misses token fields which are extracted from POS tag by FCS (eg. inflection)
def _parse_blacklab_metadata(text):
    '''
    This method parses metadata fields from a Blacklab metadata response
    Args:
        text: the XML response of a lexicon/corpus search, as a string
    Returns:
        A dictionary of with lists of document and token metadata
    '''
    
    # TODO: should we secure against untrusted XML?
    root = ET.fromstring(text)
    doc_fields = [md.get("name") for md in root.iter("metadataField")]
    token_fields = [prop.get("name") for prop in root.iter("property")]
    return {"document": doc_fields, "token": token_fields}
    


def _metadata_from_lexicon_query(lex_query):
    '''
    Extract metadata fields from a lexicon query string
    
    Args:
        lex_query: A query string issued to a lexicon, can be constructed using lexicon_query()
    Returns:
        A list of metadata fields
    '''
    # Get part after select, eg: "?x ?y ?concat('',z) as ?a"
    select_match = re.search(r'select\s+(?:distinct)*\s*(.*)\s*(?:where|from)', lex_query, flags=re.IGNORECASE)
    if select_match:
        select_string = select_match.group(1)
        #Delete concat() part and following AS, because it can contain a space we do not want to split on
        string_wh_concat = re.sub(r'concat\(.*\) AS', '', select_string, flags=re.IGNORECASE)
        split_string = string_wh_concat.split()
        for i,elem in enumerate(split_string):
            if elem.lower()=="AS":
                # Remove AS and element before AS
                split_string.pop(i)
                split_string.pop(i-1)
                # Assume only one AS, so we escape loop
                break
        columns = [c.lstrip("?") for c in split_string]
    else:
        raise ValueError("No columns find in lexicon query.")
    return columns
