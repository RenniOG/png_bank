import readline
import glob
import os


# For keyboard path autocomplete
def complete(text, state):
    # line = readline.get_line_buffer().split()
    if '~' in text:
        text = os.path.expanduser('~')

    if os.path.isdir(text):
        text += '/'

    return [x for x in glob.glob(text + '*')][state]


# Will run on import
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
