### Generate spotify most playlist songs playlists
First, define artists & artistToCrawl in artists.py.

Then, execute these commands:
python3 crawlAlbums.py
python3 crawlProcessTracks.py
python3 generatePlaylistAndTracks.py

Or execute these commands:
python3 spotifyCrawlAndProcess.py
python3 generatePlaylistAndTracks.py
python3 generatePlaylistAndTracks.py update

#### Add tracks to Listening Artist playlist
python3 playlistAddItemsByNumber.py
or
python3 playlistAddItemsByPlaycount.py



### Sync netease playlists (& filter netease non-playable songs)
(e.g. Favorite, Like, Nice, To Listen, Netease Non-playable)
python3 ../netease/getPlaylistSongs.py
python3 ../netease/getPlaylistSongs.py 'Favorite' 'Like' 'Nice'
python3 ../netease/getPlaylistSongs.py 'Hmm'
python3 ../netease/getPlaylistSongs.py 'To Listen'
python3 ../netease/getPlaylistSongs.py 'Netease Non-playable'

python3 syncNeteaseSongs.py
python3 syncNeteaseSongs.py 'Favorite'
python3 syncNeteaseSongs.py 'Like'
python3 syncNeteaseSongs.py 'Nice'
python3 syncNeteaseSongs.py 'Hmm'
python3 syncNeteaseSongs.py 'To Listen'
python3 syncNeteaseSongs.py 'Netease Non-playable'

### Like songs
python3 tracksDiff.py
python3 saveUserTracks.py
