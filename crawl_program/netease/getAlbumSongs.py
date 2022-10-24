from artists import *
from common import *

# ******************************
#   Get netease album by id
# ******************************


album = getAlbum(146313860)

printAlbums([album['album']])

printSongs(album['songs'])
