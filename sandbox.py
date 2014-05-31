import os.path

def dir(path=''):
    my_directory = os.path.dirname(__file__)
    if my_directory == '' :
        my_directory = '.'
    return my_directory + '/sandbox/' + path
