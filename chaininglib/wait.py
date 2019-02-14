import sys

def show_wait_indicator(message=None):
    
    print('...' + (message if message else 'Busy now') + '...', end="\r") 
    sys.stdout.write("\033[F")

def remove_wait_indicator():    
    print('                                                                    ', end="\r")
    sys.stdout.write("\033[F")