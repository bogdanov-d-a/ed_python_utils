import os
import webbrowser
import tempfile
import codecs

def show_and_delete_file(filename):
    try:
        if not os.path.isfile(filename):
            raise Exception(filename + ' file doesn\'t exist')
        webbrowser.open(filename)
        input()
    finally:
        os.remove(filename)

def show_data_using_file(writer):
    fd, path = tempfile.mkstemp('.txt')
    try:
        writer(path)
    finally:
        os.close(fd)
        show_and_delete_file(path)

def show_data_using_file_simple(writer):
    def cb(path):
        with codecs.open(path, 'w', 'utf-8') as out_file:
            writer(out_file)
    show_data_using_file(cb)
