import os
import sys
import inspect
# Enable import parent directory modules
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from spotify.artists import *
from common import *

# Define artist here
searchArtists = generateArtists
if len(sys.argv) >= 2:
    if sys.argv[1] == 'other':
        searchArtists = otherArtists
    elif sys.argv[1] == 'all':
        searchArtists = artists
    else:
        if artists.get(sys.argv[1]) != None:
            searchArtists = {artist: artists.get(artist) for artist in sys.argv[1:]}
        else:
            print('Can\'t find \'' +
                  sys.argv[1] + '\' in \'../spotify/artists.py\'.')
            sys.exit()


allArtists = {}
for identifier in list(searchArtists.keys())[:12]:
    artist = searchArtists[identifier]
    result = searchArtist(artist['name'])
    if result.get('result') != None and result.get('result').get('artists') != None\
            and len(result['result']['artists']) > 0:
        artistResults = result['result']['artists']
        curArtist = {
            'name': artistResults[0]['name'],
            'artistId': artistResults[0]['id']
        }
        allArtists[identifier] = curArtist
        print(identifier + ':', curArtist)
    else:
        print(artist['name'], 'not found.')
print(json.dumps(allArtists, ensure_ascii=False, indent=4).replace('"', '\''))
