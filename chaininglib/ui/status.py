import sys
import chaininglib.constants as constants

def show_wait_indicator(message=None):
    if constants.ENABLE_WAIT_INDICATOR:
        print('...' + (message if message else 'Busy now') + '...', end="\r") 
        sys.stdout.write("\033[F")

def remove_wait_indicator():   
    if constants.ENABLE_WAIT_INDICATOR: 
        print('                                                                    ', end="\r")
        sys.stdout.write("\033[F")