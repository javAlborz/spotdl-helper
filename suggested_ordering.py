#!/usr/bin/env python3
import json
from cluster_playlist import load_playlist, detect_language_and_genre

def get_genre_energy_level(genre):
    """Assign energy levels to genres for better flow"""
    energy_map = {
        'hip hop/rap': 3,
        'electronic/dance': 4,
        'dance/party': 4,
        'pop/dance': 3,
        'disco/funk': 3,
        'reggae/caribbean': 2,
        'r&b/soul': 2,
        'jazz/blues': 1,
        'folk/acoustic': 1,
        'scandinavian': 2,  # Mix of pop and rock
        'german': 2,
        'japanese/asian pop': 2,
        'latin': 2,
        'rock/alternative': 3
    }
    return energy_map.get(genre, 2)

def create_suggested_ordering(songs):
    """Create a suggested ordering for better DJ flow"""
    # Group songs by genre
    genre_groups = {}
    for song in songs:
        genre = detect_language_and_genre(song)
        if genre not in genre_groups:
            genre_groups[genre] = []
        genre_groups[genre].append(song)
    
    # Define ideal DJ set flow order by energy and style compatibility
    genre_flow_order = [
        # Warm-up / Lower energy
        'jazz/blues',
        'folk/acoustic',
        'latin',
        'r&b/soul',
        
        # Mid energy / Groovy
        'reggae/caribbean',
        'disco/funk',
        
        # Language-specific sections (good for crowd engagement)
        'scandinavian',
        'german', 
        'japanese/asian pop',
        
        # High energy dance section
        'pop/dance',
        'electronic/dance',
        'dance/party',
        
        # Peak energy
        'hip hop/rap',
    ]
    
    # Build suggested ordering
    suggested_songs = []
    for genre in genre_flow_order:
        if genre in genre_groups:
            suggested_songs.extend(genre_groups[genre])
            # Remove processed genre
            del genre_groups[genre]
    
    # Add any remaining genres at the end
    for remaining_songs in genre_groups.values():
        suggested_songs.extend(remaining_songs)
    
    return suggested_songs

def format_suggested_playlist(songs):
    """Format the suggested playlist with genre headers"""
    output = []
    song_number = 1
    current_genre = None
    
    for song in songs:
        genre = detect_language_and_genre(song)
        
        if genre != current_genre:
            # Add genre header with better formatting
            genre_header = genre.upper().replace('/', ' / ')
            output.append(f"\n═══ {genre_header} ═══")
            output.append("")  # Empty line after header
            current_genre = genre
        
        # Add song
        artist = ', '.join(song['artists'])
        title = song['name']
        output.append(f"{song_number:2d}. {artist} - {title}")
        song_number += 1
    
    # Add final empty line
    output.append("")
    
    return '\n'.join(output)

def main():
    # Load original playlist
    songs = load_playlist('playlist.spotdl')
    
    # Create suggested ordering
    suggested_songs = create_suggested_ordering(songs)
    
    # Format output
    formatted_output = format_suggested_playlist(suggested_songs)
    
    # Print the suggested playlist
    print("SUGGESTED DJ ORDERING")
    print("=" * 50)
    print("Flow: Low energy → Mid energy → Language-specific → High energy → Peak")
    print(formatted_output)
    
    # Also save to file
    with open('suggested_playlist.txt', 'w', encoding='utf-8') as f:
        f.write("SUGGESTED DJ ORDERING\n")
        f.write("=" * 50 + "\n")
        f.write("Flow: Low energy → Mid energy → Language-specific → High energy → Peak\n")
        f.write(formatted_output)
    
    # Count genres in suggested order
    genre_counts = {}
    for song in suggested_songs:
        genre = detect_language_and_genre(song)
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    
    print(f"\nSuggested ordering groups {len(genre_counts)} genres")
    print("Output saved to suggested_playlist.txt")

if __name__ == "__main__":
    main()