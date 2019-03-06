

import pandas as pd
import requests
from collections import defaultdict
import xml.etree.ElementTree as ET
import urllib
import chaininglib.constants as constants
import chaininglib.utils.dfops as dfops


def _create_lucene_metadata_filter(filter_dict):
    '''
    Create a Lucene metadata filter, based on a dictionary of conditions.
    
    Args:
        filter_dict: Dictionary of conditions. The key represents the column to be filtered. If the value is a string, the value will be matched exactly. If the value is a list, it will be interpreted as a numerical interval.
    
    Returns:
        Lucene metadata filter, which can be included in query to Blacklab server
    
    >>> _create_lucene_metadata_filter(df, {"author":"P.C. Hooft", "witnessYear_from":[1700,1800]})

    '''
    filter_string = ""
    for i, feature_name in enumerate(filter_dict):
        filter_string += feature_name + ":"
        feature_value = filter_dict[feature_name]
        # If value is string: add exact match condition of form 'feature_name:feature_value'
        if isinstance(feature_value, str):
            filter_string += ('"%s"' % feature_value)
        elif isinstance(feature_value, list) and len(feature_value)==2:
            # Numerical interval, eg. years
            # Replace None by *
            feature_value = [f if f is not None else "*" for f in feature_value]
            interval = '[%s TO %s]' % (str(feature_value[0]), str(feature_value[1]))
            filter_string += interval
        else:
            print("Unrecognized value type, skipping: " + str(feature_value))
            continue
        if i < len(filter_dict) -1:
            filter_string += " AND "
    return filter_string

def _create_pandas_metadata_filter(df, filter_dict):
    '''
    Create a Pandas DataFrame filter, based on a dictionary of conditions.
    
    Args:
        df: Pandas DataFrame on which the resulting filter of this method will be applied. The DataFrame is used to construct the Pandas filter: the filter will be DataFrame-specific.
        filter_dict: Dictionary of conditions. The key represents the column to be filtered. If the value is a string, the value will be matched exactly. If the value is a list, it will be interpreted as a numerical interval.
    
    Returns:
        Pandas DataFrame filter, which can be applied to df
    
    >>> _create_pandas_metadata_filter(df, {"author":"P.C. Hooft", "witnessYear_from":[1700,1800]})

    '''
    i = 0
    for feature_name in filter_dict:
        feature_value = filter_dict[feature_name]
        if isinstance(feature_value, str):
            # If value is string: add exact match condition
            condition = dfops.df_filter(df[feature_name], feature_value, method="match")
            i += 1
        elif isinstance(feature_value, list) and len(feature_value)==2:
            # Numerical interval, eg. years
            # User can give both years, or only one: [1600,1700], [1600,None], [None,1700]
            condition = dfops.df_filter(df[feature_name], feature_value, method="interval")   
            i +=1  
        else:
            print("Unrecognized value type, skipping: " + str(feature_value))
            continue
        if i==1:
            total_condition = condition
        else:
            total_condition = total_condition & condition
    return total_condition


def _parse_xml_blacklab (text, detailed_context=False, extra_fields_doc=[], extra_fields_token=[]):
    '''
    This function converts the Blacklab XML output of a lexicon or corpus search into a Pandas DataFrame for further processing
    
    Args:
        text: the XML response of a corpus search, as a string
        detailed_context: (optional) True to parse the layers of all tokens, False to limit detailed parsing to hits
        extra_fields_doc: extra document metadata fields to add to the results, if needed
        extra_fields_token: extra token layers to add to the results, if needed
    
    Returns:
        df: a Pandas DataFrame representing the parse results
        next_pos: the next result to be parsed (since the results might be spread among several XML response pages), 
        or 0 if there is no page left to be parsed
    
    >>> md = get_available_metadata("zeebrieven")
    >>> df, next_pos = _parse_xml_blacklab(response_text_from_server, detailed_context=False, extra_fields_doc=["author","witnessYear_from"], extra_fields_token=md["token"])
    
    '''
    # TODO: should we secure against untrusted XML?
    root = ET.fromstring(text)
    records = []
    records_len = []
    n_tokens = 0
    max_len = 0
    cols= []
    
    fields_token = constants.DEFAULT_FIELDS_TOKEN_BL + extra_fields_token
    fields_doc = constants.DEFAULT_FIELDS_DOC_BL + extra_fields_doc
    doc_metadata_all = defaultdict(dict)

    # collect metadata for all documents
    docInfos = root.find("docInfos")
    if docInfos is None:
        raise ValueError("Returned response has unexpected structure: " + text)
    for docInfo in docInfos.findall("docInfo"):
        pid = docInfo.get("pid")
        for field in docInfo:
            # If we want this field, save it
            field_name = field.tag
            if field_name in fields_doc:
                field_value = field.text
                doc_metadata_all[pid][field_name] = field_value

    # Determine max_len of hits
    for entry in root.iter("hit"):
        left = entry.find('left').findall('w')
        match = entry.find('match').findall('w')
        right = entry.find('right').findall('w')
        
        # If detailed_context on, return all layers for match+context
        if detailed_context:
            tokens = left+match+right
        # If detailed_context off, return all layers only for match
        else:
            tokens = match
        
        n_tokens = len(tokens)
        if n_tokens > max_len:
            max_len = n_tokens

    # Traverse hits
    for entry in root.iter("hit"):
        left = entry.find('left').findall('w')
        match = entry.find('match').findall('w')
        right = entry.find('right').findall('w')
        
        # If detailed_context on, return all layers for match+context
        if detailed_context:
            tokens = left+match+right
        # If detailed_context off, return all layers only for match
        else:
            tokens = match
        

        layer = defaultdict(list)
        for token in tokens:
            # Go through all extra attributes: such as lemma pos
            for att in token.attrib:
                # Check if attribute is in fields we want
                if att in fields_token:
                    layer[att].append(token.get(att))
                
            # Check word, which is saved as text instead of attribute
            if "word" in fields_token:
                layer["word"].append(token.text)
        
        # Get document metadata for this hit from storage
        pid = entry.find("docPid").text
        doc_metadata = doc_metadata_all[pid]

        if detailed_context is False:
            left_context = " ".join([w.text if w.text is not None else "" for w in left])
            right_context = " ".join([w.text if w.text is not None else "" for w in right])
        else:
            left_context = None
            right_context = None

        data, cols = _combine_layers(layer, max_len, fields_doc, doc_metadata, detailed_context, left_context, right_context)
        records.append(data)
        records_len.append(n_tokens)

    
    next_pos = 0
    summary = root.find("summary")
    has_next = summary.find("windowHasNext").text
    # If there is a next page, compute new start position
    if (has_next == "true"):
        first = summary.find("windowFirstResult").text
        number = summary.find("requestedWindowSize").text
        next_pos = int(first) + int(number)
        
        
    # do some clean up now!
    for i in range( len(records_len), 0, 1): 
        if (records_len[i]<max_len):
            del records[i]
        
    return pd.DataFrame(records, columns = cols), next_pos


def _parse_xml_fcs(text, detailed_context=False, extra_fields_doc=[], extra_fields_token=[]):
    '''
    This function converts the Federated Content Search XML output of a lexicon or corpus search into a Pandas DataFrame for further processing
    
    Args:
        text: the XML response of a lexicon/corpus search, as a string
        detailed_context: (optional) True to parse the layers of all tokens, False to limit detailed parsing to hits
        extra_fields_doc: extra document metadata fields to add to the results, if needed
        extra_fields_token: extra token layers to add to the results, if needed
    Returns:
        df: a Pandas DataFrame representing the parse results
        next_pos: the next result to be parsed (since the results might be spread among several XML response pages), 
        or 0 if there is no page left to be parsed
    
    >>> md = get_available_metadata("zeebrieven")
    >>> df, next_pos = _parse_xml_fcs(response_text_from_server, detailed_context=False, extra_fields_doc=["author","witnessYear_from"], extra_fields_token=md["token"])
    
    '''
    
    # TODO: should we secure against untrusted XML?
    root = ET.fromstring(text)
    records = []
    records_len = []
    n_tokens = 0
    cols= []
    left_context = None
    right_context = None
    
    fields_token = constants.DEFAULT_FIELDS_TOKEN_FCS + extra_fields_token
    fields_doc = constants.DEFAULT_FIELDS_DOC_FCS + extra_fields_doc
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
                # We assume that application/x-clarin-fcs-hits+xml (where left and right context are initialized) precedes x-clarin-fcs-adv+xml,
                # otherwise code won't work properly because left and right context are not initialized
                data, cols = _combine_layers(hit_layer, n_tokens, fields_doc, doc_metadata, detailed_context, left_context, right_context)
                # Reset left and right context. So if left and right context are not initialized (see above), our program can throw an error,
                # instead of using old contexts
                left_context = None
                right_context = None
                records.append(data)
                records_len.append(n_tokens)
    
    next_pos = 0
    next_record_position = root.find("{http://docs.oasis-open.org/ns/search-ws/sruResponse}nextRecordPosition")
    if (next_record_position is not None):
        next_pos = int(next_record_position.text)
        
        
    # do some clean up now!
    for i in range( len(records_len), 0, 1): 
        if (records_len[i]<max_len):
            del records[i]
        
    return pd.DataFrame(records, columns = cols), next_pos

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

        
def _combine_layers(hit_layer, n_tokens, doc_metadata_req, doc_metadata_recv, detailed_context=False, left_context=None, right_context=None):
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
        detailed_context (optional): True to parse the layers of all tokens, False to limit detailed parsing to hits
        left_context (optional): left context string, needed when detailed_context=False
        right_context (optional): right context string, needed when detailed_context=False
    Returns:
        data: flat list with combined token layers, sorted alphabetically, and document metadata
    '''
    # Sort layer keys to ensure same order of data in every row and column titles
    layers_keys = sorted(hit_layer.keys())
    # Original structure is list of tokens per layer id
    # Arrange items first on token, then on layer_id
    layers_token_flat = [hit_layer[layer_id][n] if n < len(hit_layer[layer_id]) else "" for n in range(n_tokens) for layer_id in layers_keys]
    # Flatten list of document metadata fields
    # Use all requested fields, some of which may not be available in this hit
    doc_flat = [doc_metadata_recv[field] if field in doc_metadata_recv else "" for field in doc_metadata_req]
    
    
    # Create list of columns, in same order
    tokens_columns = [layer_id+ " "+str(n) for n in range(n_tokens) for layer_id in layers_keys]
    if detailed_context is False:
        if left_context is None or right_context is None:
            raise ValueError("left_context or right_context is None: not allowed when detailed_context==False!")
        tokens_columns = ["left context"] + tokens_columns + ["right context"]
        layers_token_flat = [left_context] + layers_token_flat + [right_context]

    # Combine token and document data
    data = layers_token_flat + doc_flat
    # Add all requested document metadata fields as columns
    columns = tokens_columns + doc_metadata_req


    return data, columns
