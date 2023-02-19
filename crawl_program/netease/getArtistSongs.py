from artists import *
from common import *

# ****************************************
#    Get netease artist songs directly
# ****************************************


allSongs = getArtistSongs(artistToCrawl)

writeJsonToFile(allSongs, artistToCrawl + '_songs')

printSongs(allSongs['songs'])
