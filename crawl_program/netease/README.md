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
python3 ../spotify/crawlPlaylists.py 'Hmm'  
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
python3 syncCustomPlaylist.py 'Hmm'  
python3 syncCustomPlaylist.py 'To Listen'  
python3 syncCustomPlaylist.py 'Netease Non-playable'  
python3 syncCustomPlaylist.py 'One Hit'  
python3 syncCustomPlaylist.py 'More Hits - 民谣'  
python3 syncCustomPlaylist.py 'More Hits - 流行'  
python3 syncCustomPlaylist.py 'Collection 1'  

### Sync spotify liked songs
python3 songsDiff.py  
python3 syncLikedSongs.py  
