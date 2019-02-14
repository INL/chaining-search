import requests
from collections import defaultdict
import xml.etree.ElementTree as ET
import urllib


def _parse_xml(text, detailed_context=False, extra_fields_doc=[], extra_fields_token=[]):    
    import pandas as pd
    import chaininglib.constants as constants
    
    '''
    This function converts the XML output of a lexicon or corpus search into a Pandas DataFrame for further processing
    
    Args:
        text: the XML response of a lexicon/corpus search, as a string
        detailed_context: (optional) True to parse the layers of all tokens, False to limit detailed parsing to hits
        extra_fields_doc: 
        extra_fields_token: 
    Returns:
        df: a Pandas DataFrame representing the parse results
        next_pos: the next result page to be parsed (since the results might be spread among several XML response pages), 
        or 0 if there is no page left to be parsed
    '''
    
    # TODO: should we secure against untrusted XML?
    root = ET.fromstring(text)
    records = []
    records_len = []
    n_tokens = 0
    computed_nt = False
    cols= []
    
    fields_token = constants.DEFAULT_FIELDS_TOKEN + extra_fields_token
    fields_doc = constants.DEFAULT_FIELDS_DOC + extra_fields_doc
    for entry in root.iter("{http://clarin.eu/fcs/resource}ResourceFragment"):
        doc_metadata = {}
        for dataView in entry.findall("{http://clarin.eu/fcs/resource}DataView"):
            # Parse document metadata
            if(dataView.get("type")=="application/x-clariah-fcs-simple-metadata+xml"):
                for keyval in dataView.findall("keyval"):
                    key = keyval.get("key")
                    if key in fields_doc:
                        value = keyval.get("value")
                        doc_metadata[key] = value
            
            # ----- [part 1] ----- 
            # in 'hits only' mode, we'll gather the hits, otherwise we'll gather all the words of the sentences
            
            # We only take hits into account, ignore metadata and segmenting dataViews
            if (detailed_context is False and dataView.get("type")=="application/x-clarin-fcs-hits+xml"):
                result = dataView.find("{http://clarin.eu/fcs/dataview/hits}Result")
                left_context = result.text if result.text is not None else ''
                hits = list(result)
                if len(hits)==0:
                    print([w for w in result.itertext()])
                    print("no hit in kwic, skip")
                    continue
                last_hit = hits[-1]
                right_context = last_hit.tail if last_hit.tail is not None else ''
                #hit_words = [hit.text for hit in hits]
            
            # ----- [part 2] ----- 
            # gather info about each hit (=hits only mode) or about each word (=NOT hits only mode)
            
            # Get lemma of each hit
            cols= []
            max_len = 0
            if (dataView.get("type")=="application/x-clarin-fcs-adv+xml"):
                hit_layer = defaultdict(list) 
                for layer in dataView.findall(".//{http://clarin.eu/fcs/dataview/advanced}Layer"):
                    layer_id = layer.get("id").split("/")[-1]
                    # Only capture this layer, if it is in the list of designated fields (default+extra by user)
                    if layer_id in fields_token:
                        path = ".//{http://clarin.eu/fcs/dataview/advanced}Span"
                        if (detailed_context is False):
                            path = path+"[@highlight='h1']" 
                        for one_span in layer.findall(path):
                            span_text = one_span.text            
                            hit_layer[layer_id].append(span_text)
                        # Compute number of columns
                        n_tokens = len(hit_layer[layer_id])
                        if max_len<n_tokens:
                            max_len = n_tokens
                data, cols = _combine_layers(hit_layer, n_tokens, doc_metadata_req=fields_doc, doc_metadata_recv=doc_metadata)
                if detailed_context is False:
                    kwic = [left_context] + data + [right_context]
                else:
                    kwic = data
                records.append(kwic)
                records_len.append(n_tokens)
                
    if detailed_context is False:
        columns = ["left context"] + cols + ["right context"]
    else:
        columns = cols
    
    next_pos = 0
    next_record_position = root.find("{http://docs.oasis-open.org/ns/search-ws/sruResponse}nextRecordPosition")
    if (next_record_position is not None):
        next_pos = int(next_record_position.text)
        
        
    # do some clean up now!
    for i in range( len(records_len), 0, 1): 
        if (records_len[i]<max_len):
            del records[i]
        
    return pd.DataFrame(records, columns = columns), next_pos

def _show_error_if_any(text):
    '''
    This function reads error messages in the XML output of a lexicon or corpus search 
    and it finds any, it is printed on screen
    
    Args:
        text: the XML response of a lexicon/corpus search, as a string
    Returns:
        N/A
    '''
    root = ET.fromstring(text)
    msgs = []
    for diagnostic in root.iter("{http://docs.oasis-open.org/ns/search-ws/diagnostic}diagnostic"):
        for msg in diagnostic.findall("{http://docs.oasis-open.org/ns/search-ws/diagnostic}message"):
            msg_text = msg.text if msg.text is not None else ''
            msgs.append(msg_text)
    if len(msgs) > 0:
        print("; ".join(msgs))

def _corpus_metadata_blacklab(corpus_name):
    import chaininglib.constants as constants
    
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

# Search methods

def search_corpus_all(corpus, pos=None):
    '''
    This function gets all words of a corpus. If needed, the output can be restricted to words with a given part-of-speech
    Args:
        corpus: corpus name
        pos: part-of-speech (optional)
    Returns:
        a Pandas DataFrame containing corpus data
        
    >>> df_corpus = search_corpus_all("gysseling")
    >>> display_df(df_corpus)
    '''
    
    query = r'[]'
    if pos is not None:
        query = r'[pos="'+pos+r'"]'
    return search_query, corpus



# Deprecated, no longer needed in new CorpusQuery API
def corpus_options(detailed_context=False, extra_fields_doc=[], extra_fields_token=[], start_position=1):
    '''
    Helper function to declare options to be applied in a corpus search.
    This function is to be called as a parameter of search_corpus()
    
    >>> corpus_query = r'[lemma="someword"]'
    >>> corpus_opts = corpus_options( extra_fields_doc=fields["document"] )
    >>> df_corpus = search_corpus( corpus_query, corpus_to_search, corpus_opts )
    '''
    return {
        "detailed_context": detailed_context, 
        "extra_fields_doc": extra_fields_doc,
        "extra_fields_token": extra_fields_token,
        "start_position": start_position
    }

# Deprecated, replaced by CorpusQuery
def search_corpus(query, corpus, corpus_options=None):
    from chaininglib.wait import show_wait_indicator, remove_wait_indicator
    import chaininglib.constants as constants
    
    '''
    This function searches a corpus given a query and a corpus name
    Args:
        query: a corpus query, eg. previously generated by corpus_query_lemma() or such
        corpus: a corpus name
        detailed_context: (optional) {True, False (default)} 
        extra_fields_doc: 
        extra_fields_token: 
    Returns:
        a Pandas DataFrame containing corpus data
        
    >>> df_corpus = search_corpus(r'[pos="ADJ"][word="huis"]', "chn")
    >>> display_df(df_corpus)
    '''
    
    
    # read options
    if corpus_options is None:
        corpus_options = {
        "detailed_context" :False,
        "extra_fields_doc" : [],
        "extra_fields_token" : [],
        "start_position" : 1
        }
    
    # show wait indicator
    show_wait_indicator('Searching '+corpus+ ' at page '+str(corpus_options["start_position"]))    
    
    if corpus not in constants.AVAILABLE_CORPORA:
        raise ValueError("Unknown corpus: " + corpus)
    try:
        # Do request to federated content search corpora, so we get same output format for every corpus
        url = "http://portal.clarin.inl.nl/fcscorpora/clariah-fcs-endpoints/sru?operation=searchRetrieve&queryType=fcs&maximumRecords=1000&startRecord=" + str(corpus_options["start_position"]) + "&x-fcs-context=" + corpus + "&query=" + urllib.parse.quote(query)
        #print(url)
        response = requests.get(url)
        response_text = response.text    
        df, next_page = _parse_xml(response_text, corpus_options["detailed_context"], corpus_options["extra_fields_doc"], corpus_options["extra_fields_token"])
        # If there are next pages, call search_corpus recursively
        #print(next_page)
        remove_wait_indicator()
        if next_page > 0:
            # Update start position
            corpus_options["start_position"] = next_page
            df_more = search_corpus(query, corpus, corpus_options)
            df = df.append(df_more, ignore_index=True)
            
        
        # show message out of xml, if some error has occured (prevents empty output)
        _show_error_if_any(response_text)
        
        return df
    except Exception as e:
        remove_wait_indicator()
        raise ValueError("An error occured when searching corpus " + corpus + ": "+ str(e))
     

    
# Deprecated, replaced by CorpusQuery
def search_corpus_multiple(queries, corpus):
    '''
    This function sends multiples queries at once to the search_corpus function
    Args:
        queries: array of corpus queries, eg. previously generated by corpus_query_lemma() or such
        corpus: a corpus name 
    Returns:
        a dictionary of Pandas DataFrames, associating each query (key) to the resulting corpus data (value)
    '''
    result_dict = {}
    for query in queries:
        result_dict[query] = search_corpus(query,corpus)
    return result_dict
   
    

     
        

# Processing methods




def _combine_layers(hit_layer, n_tokens, doc_metadata_req, doc_metadata_recv):
    '''
    Combine the layers, in alphabetical order of the layer names, to a flat list, with separate column per layer per word in hit, and document metadata added as last columns
    
    Args:
        hit_layer: dictionary with list of items per layer
        n_tokens: number of tokens for which token-level annotations exist.
                    Is equal to total number of tokens in sentence if _parse_xml is called with detailed_context=True.
                    Is equal to number of tokens in hit if _parse_xml is called with detailed_context=False.
        doc_metadata_req: list of document metadata fields which have been requested
        doc_metadata_recv: dictionary with document metadata that is actually present in hits:
                        can contain less fields than doc_fields_requested
    Returns:
        data: flat list with combined token layers, sorted alphabetically, and document metadata
    '''
    # Sort layer keys to ensure same order of data in every row and column titles
    layers_keys = sorted(hit_layer.keys())
    # Original structure is list of tokens per layer id
    # Arrange items first on token, then on layer_id
    layers_token_flat = [hit_layer[layer_id][n] for n in range(n_tokens) for layer_id in layers_keys]
    # Flatten list of document metadata fields
    # Use all requested fields, some of which may not be available in this hit
    doc_flat = [doc_metadata_recv[field] if field in doc_metadata_recv else "" for field in doc_metadata_req]
    # Combine token and document data
    data = layers_token_flat + doc_flat
    
    ### Columns
    # Create list of columns, in same order
    tokens_columns = [layer_id+ " "+str(n) for n in range(n_tokens) for layer_id in layers_keys]
    # Add all requested document metadata fields as columns
    columns = tokens_columns + doc_metadata_req
    return data, columns

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
    
