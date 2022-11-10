### Sync spotify most playlist songs playlists
First, define artists & artistToCrawl in artists.py.

Then, execute these commands:
python3 getArtistAlbums.py
python3 getAlbumsSongs.py
python3 processSongs.py
python3 syncSpotifyPlaylist.py

Or execute these commands:
python3 neteaseCrawlAndProcess.py
python3 syncSpotifyPlaylist.py
python3 syncSpotifyPlaylist.py update



### Sync spotify custom playlists
(e.g. Listening Artist, Favorite, Like, Nice, To Listen, Netease Non-playable, etc.)
python3 ../spotify/crawlPlaylists.py
python3 ../spotify/crawlPlaylists.py 'Listening Artist'
python3 ../spotify/crawlPlaylists.py 'Favorite' 'Like' 'Nice'
python3 ../spotify/crawlPlaylists.py 'Hmm'
python3 ../spotify/crawlPlaylists.py 'To Listen'
python3 ../spotify/crawlPlaylists.py 'Netease Non-playable'

python3 syncCustomPlaylist.py
python3 syncCustomPlaylist.py 'Listening Artist'
python3 syncCustomPlaylist.py 'Favorite'
python3 syncCustomPlaylist.py 'Like'
python3 syncCustomPlaylist.py 'Nice'
python3 syncCustomPlaylist.py 'Hmm'
python3 syncCustomPlaylist.py 'To Listen'
python3 syncCustomPlaylist.py 'Netease Non-playable'

#### Sync spotify liked songs
python3 syncLikedSongs.py