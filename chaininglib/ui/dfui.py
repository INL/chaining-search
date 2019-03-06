import ipywidgets as widgets
from pathlib import Path
from IPython.display import Javascript
from IPython.core.display import display, HTML   # print HTML
import matplotlib.pyplot as plt  # display_df
import re
import chaininglib.utils.dfops as dfops


def create_save_dataframe_ui(df, filename=None):    
    '''
    This function builds a GUI for saving the results of some lexicon or corpus query to a .csv file.
    One can use load_dataframe(filepath) to reload the results later on.
    
    Args:
        df: a Pandas DataFrame
        filename (Optional): a filename
    Returns:
        N/A
    '''
    
    dfops.check_valid_df("create_save_dataframe_ui", df)
    
    # build ui for saving results
    default_filename = 'mijn_resultaten.csv' if filename is None else re.sub('[\W_]+', '_', filename)+".csv"
    saveResultsCaption = widgets.Label(value='Sla uw resultaten op:')
    fileNameField = widgets.Text(value=default_filename)
    savebutton = widgets.Button(
        description='Bestand opslaan',
        disabled=False,
        button_style='warning', 
        tooltip=default_filename,  # trick to pass filename to button widget
        icon=''
    )
    # inject dataframe into button object
    savebutton.df = df
    # when the user types a new filename, it will be passed to the button tooltip property straight away
    fileNameLink = widgets.jslink((fileNameField, 'value'), (savebutton, 'tooltip'))
    # click event with callback
    savebutton.on_click( _save_dataframe )    
    saveResultsBox = widgets.HBox([saveResultsCaption, fileNameField, savebutton])
    display(saveResultsBox)
    
    
def _save_dataframe(button):
    fileName = button.tooltip
    # The result files can be saved locally or on the server:
    # If result files are to be offered as downloads, set to True; otherwise set to False    
    fileDownloadable = False
    # specify paths here, if needed:
    filePath_onServer = ''  # could be /path/to
    filePath_default = ''
    # compute full path given chosen mode
    fullFileName = (filePath_onServer if fileDownloadable else filePath_default ) + fileName
        
    try:
        button.df.to_csv( fullFileName, index=False)
        # confirm it all went well
        print(fileName + " saved")    
        button.button_style = 'success'
        button.icon = 'check'
        # trick: https://stackoverflow.com/questions/31893930/download-csv-from-an-ipython-notebook
        if (fileDownloadable):
            downloadableFiles = FileLinks(filePath_onServer)
            display(downloadableFiles)
    except Exception as e:
        button.button_style = 'danger'
        raise ValueError("An error occured when saving " + fileName + ": "+ str(e))    

    
    
def load_dataframe(filepath):
    '''
    This functions (re)loads some previously saved Pandas DataFrame
    
    Args:
        filepath: path to the saved Pandas DataFrame (.csv)
    Returns: 
        a Pandas DataFrame representing the content of the file
    
    >>> df_corpus = load_dataframe('mijn_resultaten.csv')
    >>> display_df(df_corpus, labels="Results:")
    '''
    try:
        df = pd.read_csv(filepath)
        print(filepath + " loaded successfully")            
    except Exception as e:
        raise ValueError("An error occured when loading " + filepath + ": "+ str(e))
    finally:
        return df
    
    
    
def display_df(dfs, labels=None, mode='table'):
    '''
    This function shows the content of one or more Pandas DataFrames.
    When dealing with more DataFrames, those should be part of a dictionary associating
    labels (eg. corpus or lexicon names) to DataFrames (values). 
    
    Args:
        results: a Pandas DataFrames, or a dictionary of Pandas DataFrames
        labels: a label, of a list of labels corresponding to the Pandas DataFrames in the first parameter
        mode (Optional): Way of displaying, one of 'table' (default) or 'chart' 
    Returns:
        N/A
    
    >>> # call with a single pattern
    >>> df_corpus = create_corpus(corpus_to_search).pattern(some_query).search().kwic()
    >>> display_df(df_corpus)
    
    >>> # call with a list of pattern
    >>> list_of_queries = [ corpus_query(lemma=syn) for syn in syn_list ]
    >>> result_dict = create_corpus(corpus).pattern(list_of_queries).search().kwic()
    >>> display_df(result_dict, labels=list(syn_list))
    '''
    
    if type(dfs) is dict:
    
        assert len(labels)==len(dfs)
        for n,query in enumerate(dfs):
            df = dfs[query]
            if not df.empty:
                _display_single_df(df, labels[n], mode)
    else:
        dfops.check_valid_df("display_df", dfs)
        _display_single_df(dfs, labels, mode)


def _display_single_df(df_column, label, mode):
    
    # chart mode
    if mode == 'chart':
        plt.figure()
        df_column.plot.barh().set_title(label)
    
    # table mode (default)
    else:    
        if label is not None:
            display(HTML("<b>%s</b>" % label))        

        display(df_column)
    
    # eventually, give UI to save data
    create_save_dataframe_ui(df_column, label)
    