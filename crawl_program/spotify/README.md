# Spotify
## Get artists info
(Default: generateArtists)  
python3 artistsGetInfo.py  
python3 artistsGetInfo.py other  
python3 artistsGetInfo.py all  



## Generate spotify most playlist songs playlists
First, define artists & artistToCrawl in artists.py.  

Then, execute these commands:  
python3 crawlAlbums.py  
python3 crawlProcessTracks.py  
python3 generatePlaylistAndTracks.py  

Or execute these commands: (***)   
(Default: artistToCrawl)  
python3 spotifyCrawlAndProcess.py 
python3 spotifyCrawlAndProcess.py all  
python3 spotifyCrawlAndProcess.py generate  
python3 spotifyCrawlAndProcess.py other  
python3 spotifyCrawlAndProcess.py jacky_cheung  

(Default: artistToCrawl)  
python3 generatePlaylistAndTracks.py  
python3 generatePlaylistAndTracks.py update  
python3 generatePlaylistAndTracks.py update all  

### Add tracks to Listening Artist playlist
(Default: artistToCrawl, Listening Artist)  
python3 playlistAddItemsByNumber.py  
or  
(Default: artistToCrawl, Listening Artist)  
python3 playlistAddItemsByPlaycount.py  



## Sync netease playlists (& filter netease non-playable songs)
(e.g. Favorite, Like, Nice, To Listen, Netease Non-playable)  
(Default: 'Favorite' 'Like' 'Nice')  
python3 ../netease/getPlaylistSongs.py  
python3 ../netease/getPlaylistSongs.py 'Favorite' 'Like' 'Nice'  
python3 ../netease/getPlaylistSongs.py 'Hmm'  
python3 ../netease/getPlaylistSongs.py 'One Hit'  
python3 ../netease/getPlaylistSongs.py 'To Listen'  
python3 ../netease/getPlaylistSongs.py 'Netease Non-playable'  

python3 syncNeteaseSongs.py 'parameter'  
python3 syncNeteaseSongs.py 'Favorite'  
python3 syncNeteaseSongs.py 'Like'  
python3 syncNeteaseSongs.py 'Nice'  
python3 syncNeteaseSongs.py 'Hmm'  
python3 syncNeteaseSongs.py 'One Hit'  
python3 syncNeteaseSongs.py 'To Listen'  
python3 syncNeteaseSongs.py 'Netease Non-playable'  

## Like songs
python3 tracksDiff.py  
python3 saveUserTracks.py  
