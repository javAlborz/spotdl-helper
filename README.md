# spotdl-helper

Extract complete Spotify playlist data using spotDL, bypassing web interface limitations.

## Quick Start

1. Setup environment:
```bash
python3 -m venv spotify_env
source spotify_env/bin/activate
pip install spotdl
spotdl --download-ffmpeg
```

2. Extract playlist:
```bash
spotdl save "SPOTIFY_PLAYLIST_URL" --save-file playlist.spotdl
```

3. View all songs:
```bash
python3 -c "
import json
with open('playlist.spotdl', 'r') as f:
    data = json.load(f)
    
for i, song in enumerate(data, 1):
    artist = ', '.join(song['artists'])
    title = song['name']
    print(f'{i}. {artist} - {title}')
"
```

## Why?

Spotify's web interface only shows ~14 songs initially due to lazy loading. This tool extracts all songs from any playlist without authentication.