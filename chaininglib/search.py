
import requests
import pandas as pd
import xml.etree.ElementTree as ET
import json

def parse_xml(text):
    # TODO: should we secure against untrusted XML?
    root = ET.fromstring(text)
    records = []
    computed_nwih = False
    for entry in root.iter("{http://clarin.eu/fcs/resource}ResourceFragment"):
        for dataView in entry.findall("{http://clarin.eu/fcs/resource}DataView"):
            # We only take into account hits, ignore metadata and segmenting dataViews
            if (dataView.get("type")=="application/x-clarin-fcs-hits+xml"):
                result = dataView.find("{http://clarin.eu/fcs/dataview/hits}Result")
                left_context = result.text if result.text is not None else ''
                hits = list(result)
                last_hit = hits[-1]
                right_context = last_hit.tail if last_hit.tail is not None else ''
                hit_words = [hit.text for hit in hits]
                
                if not computed_nwih:
                    n_words_in_hit = len(hits)
                    computed_nwih=True
                kwic = [left_context] + hit_words + [right_context]
                records.append(kwic)
    columns = ["left context"] + ["word " + str(n) for n in range(n_words_in_hit)] + ["right context"]
    return pd.DataFrame(records, columns = columns)

def search_corpus(query, corpus):
    # Do request to federated content search corpora, so we get same output format for every corpus
    url = "http://portal.clarin.inl.nl/fcscorpora/clariah-fcs-endpoints/sru?operation=searchRetrieve&queryType=fcs&x-fcs-context=" + corpus + "&maximumRecords=20&query=" + query
    response = requests.get(url)
    response_text = response.text
    df = parse_xml(response_text)
    return df
   
def search_lexicon(query,corpus):
    endpoint = "http://svprre02:8080/fuseki/tdb/sparql"
    url = endpoint #+ "?query=" + query
    response = requests.post(url,data={"query":query})
    response_json = json.loads(response.text)
    records_json = response_json["results"]["bindings"]
    records_string = json.dumps(records_json)
    df = pd.read_json(records_string, orient="records")
    df = df.applymap(lambda x: x["value"])
    return df