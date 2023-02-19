# Spotify
## Get artists info
(Default: artistToCrawl)  
python3 artistsGetInfo.py  
python3 artistsGetInfo.py jacky_cheung  
python3 artistsGetInfo.py generate  
python3 artistsGetInfo.py other  
python3 artistsGetInfo.py all  
python3 artistsGetInfo.py merge  
python3 artistsFollows.py  



## Generate spotify most playlist songs playlists
First, define artists & artistToCrawl in artists.py.  

Then, execute these commands:  
python3 crawlAlbums.py  
python3 crawlProcessTracks.py  
python3 generatePlaylistAndTracks.py  

Or execute these commands: (***)   
(Default: artistToCrawl)  
(overwriteTrackSheets = False)  
python3 spotifyCrawlAndProcess.py  
python3 spotifyCrawlAndProcess.py all  
python3 spotifyCrawlAndProcess.py generate  
python3 spotifyCrawlAndProcess.py generate false (overwriteTrackSheets = False)  
python3 spotifyCrawlAndProcess.py other  
python3 spotifyCrawlAndProcess.py jacky_cheung  
python3 spotifyCrawlAndProcess.py jacky_cheung false (overwriteTrackSheets = False)  
python3 spotifyCrawlAndProcess.py dicky_cheung-2 dicky_cheung    

(Default: artistToCrawl)  
python3 generatePlaylistAndTracks.py  
python3 generatePlaylistAndTracks.py jacky_cheung  
python3 generatePlaylistAndTracks.py update  
python3 generatePlaylistAndTracks.py update faye_wong  
python3 generatePlaylistAndTracks.py update all  

### Delete generated playlist
python3 playlistDelete.py artist  

### Add tracks to Listening Artist playlist
(Default: artistToCrawl, Listening Artist)  
python3 playlistAddItemsByPlaycount.py  
or   
(Default: artistToCrawl, generated playlist)  
python3 playlistAddItemsByNumber.py  
(Default: artistToCrawl)  
python3 playlistAddItemsByNumber.py 'Listening Artist'  
python3 playlistAddItemsByNumber.py 'Listening Artist' pushu xuwei lijian zhengjun  
python3 playlistAddItemsByNumber.py 'Collection 1' pushu xuwei lijian zhengjun  
python3 playlistAddItemsByNumber.py 'Collection 2' sam_hui alan_tam george_lam  
python3 playlistAddItemsByNumber.py 'Collection 3' sally_yeh sandy_lam priscilla_chan vivian_chow  
python3 playlistAddItemsByNumber.py 'Collection 4' cally_kwong shirley_kwan cass_phang  
python3 playlistAddItemsByNumber.py 'Collection 5' andy_hui william_so edmond_leung dicky_cheung big_four  



## Sync netease playlists (& filter netease non-playable songs)
(e.g. Favorite, Like, Nice, To Listen, Netease Non-playable)  
(Default: 我喜欢的音乐)  
python3 ../netease/getPlaylistSongs.py  
python3 ../netease/getPlaylistSongs.py 'Listening Artist'  
python3 ../netease/getPlaylistSongs.py 'Favorite' 'Like' 'Nice'  
python3 ../netease/getPlaylistSongs.py 'Like' 'Nice'  
python3 ../netease/getPlaylistSongs.py 'Hmm'  
python3 ../netease/getPlaylistSongs.py 'High'  
python3 ../netease/getPlaylistSongs.py 'To Listen'  
python3 ../netease/getPlaylistSongs.py 'Netease Non-playable'  
python3 ../netease/getPlaylistSongs.py 'One Hit'  
python3 ../netease/getPlaylistSongs.py 'More Hits - 民谣'  
python3 ../netease/getPlaylistSongs.py 'Collection 1'  

python3 syncNeteaseSongs.py 'parameter'  
(Must be incremental!)  
python3 syncNeteaseSongs.py 'Favorite'  
python3 syncNeteaseSongs.py 'Like'  
python3 syncNeteaseSongs.py 'Nice'  
python3 syncNeteaseSongs.py 'Hmm'  
python3 syncNeteaseSongs.py 'High'  
python3 syncNeteaseSongs.py 'To Listen'  
python3 syncNeteaseSongs.py 'Netease Non-playable'  
(To update description)  
python3 syncNeteaseSongs.py 'One Hit'  
python3 syncNeteaseSongs.py 'More Hits - 民谣'  
python3 syncNeteaseSongs.py 'More Hits - 流行'  
python3 syncNeteaseSongs.py 'Collection 1'  

python3 ../netease/getPlaylistSongs.py 'Listening Artist'  
python3 syncNeteaseSongs.py 'Listening'  

python3 ../netease/getPlaylistSongs.py '好歌拾遗'  
python3 syncArtistSongs.py  

### Like songs
python3 tracksDiff.py  
python3 saveUserTracks.py  



## Other
### Get playlist songs
(Default: 'Favorite' 'Like' 'Nice')  
python3 crawlPlaylists.py  
python3 crawlPlaylists.py 'Listening Artist'  
python3 crawlPlaylists.py 'Favorite' 'Like' 'Nice'  
python3 crawlPlaylists.py 'Favorite' 'Like'  
python3 crawlPlaylists.py 'Like' 'Nice'  
python3 crawlPlaylists.py '好歌拾遗'  
