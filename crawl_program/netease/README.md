# Netease Cloud Music
## Search artists
### Search artists in ../spotify/artist.py
(Default: generateArtists)  
python3 artistsSearch.py  
python3 artistsSearch.py other  
python3 artistsSearch.py all  
python3 artistsSearch.py jacky_cheung  

### Get artists info
(Default: artistToCrawl)  
python3 artistsGetInfo.py  
python3 artistsGetInfo.py generate  
python3 artistsGetInfo.py other  
python3 artistsGetInfo.py all  
python3 artistsGetInfo.py jacky_cheung  

### Get artist all songs' comments
(Default: artistToCrawl)  
python3 getArtistComments.py  
(张学友 Most Played Songs)  
python3 getArtistComments.py jacky_cheung  



## Sync spotify most playlist songs playlists
First, define artists & artistToCrawl in artists.py.  

Then, execute these commands:  
python3 getArtistAlbums.py  
python3 getAlbumsSongs.py  
python3 processSongs.py  
python3 syncSpotifyPlaylist.py  

Or execute these commands: (***)  
(Default: artistToCrawl)  
python3 neteaseCrawlAndProcess.py  
python3 neteaseCrawlAndProcess.py all  
python3 neteaseCrawlAndProcess.py generate  
python3 neteaseCrawlAndProcess.py other  
python3 neteaseCrawlAndProcess.py jacky_cheung  

(Default: artistToCrawl)  
python3 syncSpotifyPlaylist.py  
python3 syncSpotifyPlaylist.py update  
python3 syncSpotifyPlaylist.py update faye_wong  
python3 syncSpotifyPlaylist.py update all  



## Sync spotify custom playlists
(e.g. Listening Artist, Favorite, Like, Nice, To Listen, Netease Non-playable, etc.)  
(Default: 'Favorite' 'Like' 'Nice')  
python3 ../spotify/crawlPlaylists.py  
python3 ../spotify/crawlPlaylists.py 'Listening Artist'  
python3 ../spotify/crawlPlaylists.py 'Favorite' 'Like' 'Nice'  
python3 ../spotify/crawlPlaylists.py 'Like' 'Nice'  
python3 ../spotify/crawlPlaylists.py 'Like But More' 'Nice But Classic'  
python3 ../spotify/crawlPlaylists.py 'Like But More'  
python3 ../spotify/crawlPlaylists.py 'Nice But Classic'  
python3 ../spotify/crawlPlaylists.py 'Hmm'  
python3 ../spotify/crawlPlaylists.py 'High'  
python3 ../spotify/crawlPlaylists.py '好歌拾遗'  
python3 ../spotify/crawlPlaylists.py 'Listening'  
python3 ../spotify/crawlPlaylists.py 'To Listen'  
python3 ../spotify/crawlPlaylists.py 'Netease Non-playable'  
python3 ../spotify/crawlPlaylists.py 'One Hit'  
python3 ../spotify/crawlPlaylists.py 'More Hits - 民谣'  
python3 ../spotify/crawlPlaylists.py 'More Hits - 流行'  
python3 ../spotify/crawlPlaylists.py 'Collection 1'  

python3 syncCustomPlaylist.py 'parameter'  
python3 syncCustomPlaylist.py 'Listening Artist'  
python3 syncCustomPlaylist.py 'Favorite'  
python3 syncCustomPlaylist.py 'Like'  
python3 syncCustomPlaylist.py 'Nice'  
python3 syncCustomPlaylist.py 'Like But More'  
python3 syncCustomPlaylist.py 'Nice But Classic'  
python3 syncCustomPlaylist.py 'Hmm'  
python3 syncCustomPlaylist.py 'High'  
python3 syncCustomPlaylist.py '好歌拾遗'  
python3 syncCustomPlaylist.py '张学友'  
python3 syncCustomPlaylist.py '周杰伦'  
python3 syncCustomPlaylist.py 'Listening'  
python3 syncCustomPlaylist.py 'To Listen'  
python3 syncCustomPlaylist.py 'Netease Non-playable'  
python3 syncCustomPlaylist.py 'One Hit'  
python3 syncCustomPlaylist.py 'More Hits - 民谣'  
python3 syncCustomPlaylist.py 'More Hits - 流行'  
python3 syncCustomPlaylist.py 'Collection 1'  

### Sync spotify liked songs
python3 songsDiff.py  
python3 syncLikedSongs.py  

python3 getPlaylistSongs.py 'Favorite' 'Like' 'Nice'  
~~python3 getPlaylistDetails.py huahua~~  
python3 diffSongs.py  
python3 diffSongs.py huahua  



## Other
### Get playlist songs
(Default: 我喜欢的音乐)  
python3 getPlaylistSongs.py  
python3 getPlaylistSongs.py 'Favorite' 'Like' 'Nice' 'Listening Artist'  
python3 getPlaylistSongs.py 'Favorite' 'Like' 'Nice'  
python3 getPlaylistSongs.py 'Listening Artist'  
python3 getPlaylistSongs.py '好歌拾遗'  
python3 getPlaylistSongs.py 'Collection 1'  
python3 getPlaylistSongs.py 张学友  
(张学友 Most Played Songs)  
python3 getPlaylistSongs.py jacky_cheung  

### Get playlist song details
(Default: artistToCrawl)  
python3 getPlaylistDetails.py  
(张学友 Most Played Songs)  
python3 getPlaylistDetails.py jacky_cheung  
python3 getPlaylistDetails.py 'Collection 1'  
python3 getPlaylistDetails.py 张学友  
python3 getPlaylistDetails.py 'Listening Artist'  
