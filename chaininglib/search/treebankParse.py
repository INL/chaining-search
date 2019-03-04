from chaininglib.search.treeobject import *
import xml.etree.ElementTree as ET


def _parse_treebank_xml (text):
    '''
    Parse the XML of a treebank
    Args:
        text: XML response from treebank
    Returns:
        List of tree representations of data
    '''
    
    # we need the XML to have a root element to be valid!
    text = '<root>' + text + '</root>'
    
    root = ET.fromstring(text)
    
    trees = []
    
    # Traverse main nodes (=highest node of each tree)
    
    for mainNode in root.findall("node"):
        
        tree = _parse_node(mainNode) # this will be called recursively, till the very last leaves are reached!
        
        trees.append( tree ) 
        
        
    # Done, return all the trees in an array
        
    return trees
        
        
        
def _parse_node (node):
    '''
    Parse one XML node of a treebank
    Args:
        node: XML of one node
    Returns:
        tree representation of data
    '''    
    
    # read list attributes
    
    list_of_attributes = list(node.attrib.keys())
    
    
    # read each attribute if present
    id = node.attrib["id"] if "id" in list_of_attributes else ""
    begin = node.attrib["begin"] if "begin" in list_of_attributes else ""
    end = node.attrib["end"] if "end" in list_of_attributes else ""

    lemma = node.attrib["lemma"] if "lemma" in list_of_attributes else ""
    postag = node.attrib["postag"] if "postag" in list_of_attributes else ""
    cat = node.attrib["cat"] if "cat" in list_of_attributes else ""
    word = node.attrib["word"]  if "word" in list_of_attributes else ""

    rel = node.attrib["rel"] if "rel" in list_of_attributes else ""
    
    
    # instantiate (sub)tree
    tree = TreeObject(id, begin, end, lemma, postag, cat, word)
    
    # parse leaves (recursively) and return results
    
    subNodes = node.findall("node")
    
    if len(subNodes) == 0:
        return tree
    else:
        for subNode in subNodes:
            part = _parse_node(subNode)  # recursive call
            tree.addPart(part)
            
        return tree