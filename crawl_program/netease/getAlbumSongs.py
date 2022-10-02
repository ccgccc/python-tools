from artists import *
from common import *


album = getAlbum(146313860)

printAlbums([album['album']])

printSongs(album['songs'])
