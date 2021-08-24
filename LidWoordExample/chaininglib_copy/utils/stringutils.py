import re

def containsRegex(word):
    '''
    This function checks whether some string contains a regular expression or not
    
    Args:
        word: a string to check for regular expressions
    Returns:
        A boolean
    '''
    return ( word.find('^')>-1 or
            word.find('$')>-1 or 
            re.match("\(.+?\)", word) or
            re.match("\[.+?\]", word) or
            re.match("[\+*]", word) )