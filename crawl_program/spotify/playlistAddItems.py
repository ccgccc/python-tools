import json

artist = 'jacky_cheung'

allTracks = []
with open('./files/' + artist + '_alltracks.json') as f:
    allTracks = json.load(f)
print(allTracks)
