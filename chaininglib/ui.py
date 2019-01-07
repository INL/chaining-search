
import ipywidgets as widgets
from IPython.display import display
DEFAULT_QUERY = r'[lemma="boek"]'
DEFAULT_CORPUS = "chn"

def create_corpus_ui():
    # Create UI elements
    corpusQueryField = widgets.Text(description="<b>CQL query:</b>", value=DEFAULT_QUERY)
    corpusField = widgets.Dropdown(
        options=['chn', 'opensonar', 'zeebrieven', 'gysseling', 'nederlab'],
        value=DEFAULT_CORPUS,
        description='<b>Corpus:</b>',
    )
    '''corpusSearchButton = widgets.Button(
        description='Search',
        button_style='info', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Search',
    )
    # Handle events
    corpusSearchButton.on_click(corpus_search)'''

    # Stack UI elements in vertical box and display
    corpusUiBox = widgets.VBox([corpusQueryField,corpusField])
    display(corpusUiBox)
    
    # Return fields, so their contents are accessible from the global namespace of the Notebook
    return corpusQueryField, corpusField

def create_lexicon_ui():
    DEFAULT_SEARCHWORD = 'boek'
    DEFAULT_LEXICON = "diamant"

    # Create UI elements
    searchWordField = widgets.Text(description="<b>Word:</b>", value=DEFAULT_SEARCHWORD)
    lexiconField = widgets.Dropdown(
        options=['diamant'],
        value=DEFAULT_LEXICON,
        description='<b>Lexicon:</b>',
    )
    '''lexSearchButton = widgets.Button(
        description='Search',
        button_style='info', # 'success', 'info', 'warning', 'danger' or ''
        tooltip='Search',
    )
    # Handle events
    lexSearchButton.on_click(lexicon_search)'''
    # Stack UI elements in vertical box and display
    lexUiBox = widgets.VBox([searchWordField,lexiconField])
    display(lexUiBox)
    return searchWordField, lexiconField