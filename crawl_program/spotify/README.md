### Generate spotify most playlist songs playlists
First, define artists & artistToCrawl in artists.py.

Then, execute these commands:
python3 crawlAlbums.py
python3 crawlProcessTracks.py
python3 generatePlaylistAndTracks.py

Or execute these commands:
python3 spotifyCrawlAndProcess.py
python3 generatePlaylistAndTracks.py

#### Add tracks to Listening Artist playlist
python3 playlistAddItemsByNumber.py
or
python3 playlistAddItemsByPlaycount.py



### Sync netease playlists (& filter netease non-playable songs)
(e.g. Favorite, Like, Nice, Netease Non-playable)
python3 getPlaylistSongs.py  (in ../netease)
python3 syncNeteaseSongs.py

### Like songs
python3 tracksDiff.py
python3 saveUserTracks.py
