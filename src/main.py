"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    user_prefs = {
        "favorite_genre": "lofi",
        "favorite_mood": "chill",
        "target_energy": 0.40,
        "target_valence": 0.60,
        "target_danceability": 0.60,
        "target_tempo_bpm": 78,
        "likes_acoustic": True,
        "target_acousticness": 0.75,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop 5 Recommendations\n" + "-" * 40)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{i}. {song['title']} by {song.get('artist', '?')}  [{score:.1f}/100]")
        print(f"   Why: {explanation}")
        print()


if __name__ == "__main__":
    main()
