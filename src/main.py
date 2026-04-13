"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


# ── Standard profiles ────────────────────────────────────────────────────────

HIGH_ENERGY_POP = {
    "label": "High-Energy Pop",
    "favorite_genre": "pop",
    "favorite_mood": "happy",
    "target_energy": 0.90,
    "target_valence": 0.85,
    "target_danceability": 0.85,
    "target_tempo_bpm": 128,
    "likes_acoustic": False,
    "target_acousticness": 0.10,
}

CHILL_LOFI = {
    "label": "Chill Lofi",
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "target_valence": 0.60,
    "target_danceability": 0.60,
    "target_tempo_bpm": 78,
    "likes_acoustic": True,
    "target_acousticness": 0.75,
}

DEEP_INTENSE_ROCK = {
    "label": "Deep Intense Rock",
    "favorite_genre": "rock",
    "favorite_mood": "intense",
    "target_energy": 0.92,
    "target_valence": 0.30,
    "target_danceability": 0.65,
    "target_tempo_bpm": 150,
    "likes_acoustic": False,
    "target_acousticness": 0.08,
}

# ── Adversarial / edge-case profiles ─────────────────────────────────────────

CONFLICTING_VIBES = {
    "label": "Adversarial: Conflicting Vibes (high energy + chill mood)",
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.92,       # lofi songs are typically low energy
    "target_valence": 0.50,
    "target_danceability": 0.50,
    "target_tempo_bpm": 78,
    "likes_acoustic": True,
    "target_acousticness": 0.75,
}

GHOST_GENRE = {
    "label": "Adversarial: Ghost Genre (genre not in catalog)",
    "favorite_genre": "k-pop",   # no k-pop songs in data/songs.csv
    "favorite_mood": "happy",
    "target_energy": 0.80,
    "target_valence": 0.80,
    "target_danceability": 0.80,
    "target_tempo_bpm": 120,
    "likes_acoustic": False,
    "target_acousticness": 0.10,
}

ALL_NEUTRAL = {
    "label": "Adversarial: All Neutral (no genre/mood, all features at 0.5)",
    "favorite_genre": None,
    "favorite_mood": None,
    "target_energy": 0.50,
    "target_valence": 0.50,
    "target_danceability": 0.50,
    "target_tempo_bpm": None,
    "likes_acoustic": False,
    "target_acousticness": 0.50,
}

ALL_PROFILES = [
    HIGH_ENERGY_POP,
    CHILL_LOFI,
    DEEP_INTENSE_ROCK,
    CONFLICTING_VIBES,
    GHOST_GENRE,
    ALL_NEUTRAL,
]


def run_profile(label: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print top-k recommendations for a single user profile."""
    print(f"\n{'='*50}")
    print(f"  Profile: {label}")
    print(f"{'='*50}")
    recommendations = recommend_songs(user_prefs, songs, k=k)
    for i, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{i}. {song['title']} by {song.get('artist', '?')}  [{score:.1f}/100]")
        print(f"   Why: {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for profile in ALL_PROFILES:
        label = profile.pop("label")
        run_profile(label, profile, songs)
        profile["label"] = label   # restore so the dict stays intact


if __name__ == "__main__":
    main()
