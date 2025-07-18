#!/usr/bin/env python3
import json

def load_playlist(filename):
    """Load the playlist data from .spotdl file"""
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)

def detect_language_and_genre(song):
    """Detect language and genre for better clustering"""
    genres = song.get('genres', [])
    genre_text = ' '.join(genres).lower()
    
    # Language/cultural detection based on genre keywords
    if any(keyword in genre_text for keyword in ['norwegian', 'danish', 'swedish', 'nordic', 'dansktop']):
        return 'scandinavian'
    elif any(keyword in genre_text for keyword in ['german', 'neue deutsche']):
        return 'german'
    elif any(keyword in genre_text for keyword in ['japanese', 'anime', 'j-pop', 'city pop']):
        return 'japanese/asian pop'
    elif any(keyword in genre_text for keyword in ['latin', 'reggaeton', 'salsa', 'brazilian']):
        return 'latin'
    elif any(keyword in genre_text for keyword in ['french', 'chanson']):
        return 'french'
    
    # For English songs, use broader genre categories
    if not genres:
        return 'dance/party'
    
    primary_genre = genres[0].lower()
    
    # Much broader genre groupings
    if any(keyword in primary_genre for keyword in ['pop', 'dance', 'electropop', 'europop']):
        return 'pop/dance'
    elif any(keyword in primary_genre for keyword in ['hip hop', 'rap', 'trap', 'drill', 'grime']):
        return 'hip hop/rap'
    elif any(keyword in primary_genre for keyword in ['r&b', 'rnb', 'soul', 'new jack', 'contemporary r&b']):
        return 'r&b/soul'
    elif any(keyword in primary_genre for keyword in ['electronic', 'edm', 'house', 'techno', 'electro', 'trip hop', 'post-disco']):
        return 'electronic/dance'
    elif any(keyword in primary_genre for keyword in ['disco', 'funk']):
        return 'disco/funk'
    elif any(keyword in primary_genre for keyword in ['rock', 'alternative', 'indie']):
        return 'rock/alternative'
    elif any(keyword in primary_genre for keyword in ['reggae', 'dancehall', 'soca']):
        return 'reggae/caribbean'
    elif any(keyword in primary_genre for keyword in ['jazz', 'blues', 'bossa nova']):
        return 'jazz/blues'
    elif any(keyword in primary_genre for keyword in ['folk', 'acoustic', 'singer-songwriter', 'country']):
        return 'folk/acoustic'
    else:
        return 'dance/party'

def get_song_genre(song):
    """Extract and normalize the primary genre for a song"""
    return detect_language_and_genre(song)

def cluster_songs_by_genre(songs):
    """Cluster songs by genre while maintaining order"""
    if not songs:
        return []
    
    clusters = []
    current_cluster = {
        'genre': get_song_genre(songs[0]),
        'songs': [songs[0]]
    }
    
    for song in songs[1:]:
        song_genre = get_song_genre(song)
        
        if song_genre == current_cluster['genre']:
            # Same genre, add to current cluster
            current_cluster['songs'].append(song)
        else:
            # Different genre, start new cluster
            clusters.append(current_cluster)
            current_cluster = {
                'genre': song_genre,
                'songs': [song]
            }
    
    # Add the last cluster
    clusters.append(current_cluster)
    
    return clusters

def format_clustered_playlist(clusters):
    """Format the clustered playlist with genre headers"""
    output = []
    song_number = 1
    
    for cluster in clusters:
        genre = cluster['genre']
        songs = cluster['songs']
        
        # Add genre header with better formatting
        genre_header = genre.upper().replace('/', ' / ')
        output.append(f"\n═══ {genre_header} ═══")
        output.append("")  # Empty line after header
        
        # Add songs in this cluster
        for song in songs:
            artist = ', '.join(song['artists'])
            title = song['name']
            output.append(f"{song_number:2d}. {artist} - {title}")
            song_number += 1
        
        output.append("")  # Empty line after each section
    
    return '\n'.join(output)

def main():
    # Load playlist
    songs = load_playlist('playlist.spotdl')
    
    # Cluster by genre
    clusters = cluster_songs_by_genre(songs)
    
    # Format output
    formatted_output = format_clustered_playlist(clusters)
    
    # Print the clustered playlist
    print("PLAYLIST CLUSTERED BY GENRE")
    print("=" * 50)
    print(formatted_output)
    
    print(f"\n\nGenerated {len(clusters)} genre clusters from {len(songs)} songs")

if __name__ == "__main__":
    main()