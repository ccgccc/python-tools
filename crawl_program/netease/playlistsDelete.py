import os
from os import listdir
from os.path import isfile, join
from artists import *
from common import *

playlistIds = ['', '']

headers['cookie'] = readFileContent('cookie.txt')

deletePlaylist(','.join(playlistIds))
