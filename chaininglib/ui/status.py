import sys
import chaininglib.constants as constants

def show_wait_indicator(message=None):
    '''
    Shows a wait indicator, indicating that a process (such as search) is going on.
    
    Args:
        message: The message shown by the wait indicator
    '''
    if constants.ENABLE_WAIT_INDICATOR:
        print('...' + (message if message else 'Busy now') + '...', end="\r") 
        sys.stdout.write("\033[F")

def remove_wait_indicator():
    '''
    Removes a wait indicator, indicating that a process (such as search) is going on.
    '''
    if constants.ENABLE_WAIT_INDICATOR: 
        print('                                                                    ', end="\r")
        sys.stdout.write("\033[F")