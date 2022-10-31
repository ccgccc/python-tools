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


### Sync spotify custom playlists
(e.g. Listening Artist, Favorite, Like, Nice, To Listen, Netease Liked, etc.)
python3 crawlPlaylists.py  (in ../spotify)
python3 syncCustomPlaylist.py