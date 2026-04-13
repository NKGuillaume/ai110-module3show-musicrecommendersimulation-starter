from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # Build user preference dict for scoring
        user_pref = {
            'energy': getattr(user, 'target_energy', 0.5),
            'valence': 0.5,
            'danceability': 0.5,
            'acousticness': 1.0 if getattr(user, 'likes_acoustic', False) else 0.0,
            'tempo_norm': 0.5,
            'genre': getattr(user, 'favorite_genre', None),
            'mood': getattr(user, 'favorite_mood', None),
            'favorite_artist': None,
        }

        # infer tempo range from available songs
        tempos = [s.tempo_bpm for s in self.songs if getattr(s, 'tempo_bpm', None) is not None]
        if tempos:
            tmin, tmax = min(tempos), max(tempos)
        else:
            tmin, tmax = 40.0, 200.0

        scored: List[Tuple[Song, float]] = []
        for s in self.songs:
            track = {
                'energy': s.energy,
                'valence': s.valence,
                'danceability': s.danceability,
                'acousticness': s.acousticness,
                'tempo_norm': (s.tempo_bpm - tmin) / (tmax - tmin) if tmax > tmin else 0.5,
                'genre': s.genre,
                'mood': s.mood,
                'artist': s.artist,
            }
            score = compute_score(track, user_pref, pop_norm=0.0)
            scored.append((s, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # Build similar user_pref map as in recommend()
        user_pref = {
            'energy': getattr(user, 'target_energy', 0.5),
            'valence': 0.5,
            'danceability': 0.5,
            'acousticness': 1.0 if getattr(user, 'likes_acoustic', False) else 0.0,
            'tempo_norm': 0.5,
            'genre': getattr(user, 'favorite_genre', None),
            'mood': getattr(user, 'favorite_mood', None),
            'favorite_artist': None,
        }
        track = {
            'energy': song.energy,
            'valence': song.valence,
            'danceability': song.danceability,
            'acousticness': song.acousticness,
            'tempo_norm': 0.5,
            'genre': song.genre,
            'mood': song.mood,
            'artist': song.artist,
        }
        score = compute_score(track, user_pref, pop_norm=0.0)
        parts = [f"Overall score: {score:.1f}/100"]
        if song.genre == user_pref.get('genre'):
            parts.append(f"matches genre: {song.genre}")
        if song.mood == user_pref.get('mood'):
            parts.append(f"matches mood: {song.mood}")
        return '; '.join(parts)

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}
    rows: List[Dict] = []
    with open(csv_path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for r in reader:
            try:
                for field in int_fields:
                    if field in r and r[field] != '':
                        r[field] = int(r[field])
                for field in float_fields:
                    if field in r and r[field] != '':
                        r[field] = float(r[field])
            except Exception:
                # skip malformed row
                continue
            rows.append(r)

    # normalize tempo to 0..1 using observed min/max
    tempos = [r['tempo_bpm'] for r in rows if 'tempo_bpm' in r]
    if tempos:
        tmin, tmax = min(tempos), max(tempos)
        denom = tmax - tmin if tmax > tmin else 1.0
        for r in rows:
            if 'tempo_bpm' in r:
                r['tempo_norm'] = max(0.0, min(1.0, (r['tempo_bpm'] - tmin) / denom))
            else:
                r['tempo_norm'] = 0.5
    else:
        for r in rows:
            r['tempo_norm'] = 0.5

    return rows

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # Build a user_prefs mapping compatible with compute_score's expectations
    # Accept both short and explicit keys; prefer explicit (favorite_genre etc.)
    prefs = {
        'favorite_genre': user_prefs.get('favorite_genre') or user_prefs.get('genre'),
        'favorite_mood': user_prefs.get('favorite_mood') or user_prefs.get('mood'),
        'target_energy': user_prefs.get('target_energy') or user_prefs.get('energy') or 0.5,
        'target_valence': user_prefs.get('target_valence', 0.5),
        'target_danceability': user_prefs.get('target_danceability', 0.5),
        'likes_acoustic': user_prefs.get('likes_acoustic', False),
        'target_acousticness': user_prefs.get('target_acousticness', None),
        'target_tempo': user_prefs.get('target_tempo') or user_prefs.get('target_tempo_bpm'),
    }
    score = compute_score(song, prefs, pop_norm=song.get('pop_norm', 0.0))
    reasons: List[str] = []

    if song.get('genre') == prefs.get('favorite_genre'):
        reasons.append('genre match (+2.0)')
    if song.get('mood') == prefs.get('favorite_mood'):
        reasons.append('mood match (+2.0)')

    target_energy = prefs.get('target_energy', 0.5)
    e_pts = round(max(0.0, 1.0 - abs(song.get('energy', 0.5) - target_energy)) * 1.5, 2)
    reasons.append(f'energy fit (+{e_pts})')

    target_valence = prefs.get('target_valence', 0.5)
    v_pts = round(max(0.0, 1.0 - abs(song.get('valence', 0.5) - target_valence)) * 0.75, 2)
    reasons.append(f'valence fit (+{v_pts})')

    target_danceability = prefs.get('target_danceability', 0.5)
    d_pts = round(max(0.0, 1.0 - abs(song.get('danceability', 0.5) - target_danceability)) * 0.75, 2)
    reasons.append(f'danceability fit (+{d_pts})')

    target_acousticness = prefs.get('target_acousticness')
    if target_acousticness is None:
        target_acousticness = 1.0 if prefs.get('likes_acoustic', False) else 0.0
    a_pts = round(max(0.0, 1.0 - abs(song.get('acousticness', 0.0) - target_acousticness)) * 0.75, 2)
    reasons.append(f'acousticness fit (+{a_pts})')

    target_tempo = prefs.get('target_tempo') or prefs.get('target_tempo_bpm')
    if 'tempo_bpm' in song and target_tempo is not None:
        t_pts = round(max(0.0, 1.0 - abs(song['tempo_bpm'] - target_tempo) / 100.0) * 0.5, 2)
        reasons.append(f'tempo fit (+{t_pts})')

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored: List[Tuple[Dict, float, str]] = []
    for s in songs:
        score, reasons = score_song(user_prefs, s)
        explanation = ', '.join(reasons) if reasons else 'no match'
        scored.append((s, score, explanation))
    scored.sort(key=lambda t: t[1], reverse=True)
    return scored[:k]


import math
def gaussian_similarity(v, p, sigma=0.15):
    return math.exp(-((v-p)**2) / (2*sigma*sigma))

def compute_score(track, user_pref, pop_norm=0.0):
    """Compute a 0–100 weighted score for a track against a user preference dict."""
    # Linear scoring recipe matching the user's example.
    # Categorical bonuses
    raw = 0.0
    if track.get('genre') == user_pref.get('favorite_genre'):
        raw += 2.0
    if track.get('mood') == user_pref.get('favorite_mood'):
        raw += 2.0

    # Energy fit (weight 1.5)
    target_energy = user_pref.get('target_energy', 0.5)
    e_points = max(0.0, 1.0 - abs(track.get('energy', 0.5) - target_energy)) * 1.5
    raw += e_points

    # Valence fit (weight 0.75)
    target_valence = user_pref.get('target_valence', 0.5)
    v_points = max(0.0, 1.0 - abs(track.get('valence', 0.5) - target_valence)) * 0.75
    raw += v_points

    # Danceability fit (weight 0.75)
    target_danceability = user_pref.get('target_danceability', 0.5)
    d_points = max(0.0, 1.0 - abs(track.get('danceability', 0.5) - target_danceability)) * 0.75
    raw += d_points

    # Acousticness (weight 0.75) - use target_acousticness float if provided, else likes_acoustic bool
    target_acousticness = user_pref.get('target_acousticness')
    if target_acousticness is None:
        likes_acoustic = user_pref.get('likes_acoustic', False)
        target_acousticness = 1.0 if likes_acoustic else 0.0
    a_points = max(0.0, 1.0 - abs(track.get('acousticness', 0.0) - target_acousticness)) * 0.75
    raw += a_points

    # Tempo fit (weight 0.5) - normalized over 100 BPM window using tempo_bpm
    target_tempo = user_pref.get('target_tempo') or user_pref.get('target_tempo_bpm')
    tempo_points = 0.0
    if 'tempo_bpm' in track and target_tempo is not None:
        tempo_sim = max(0.0, 1.0 - abs(track['tempo_bpm'] - target_tempo) / 100.0)
        tempo_points = tempo_sim * 0.5
        raw += tempo_points

    # Maximum raw possible: 8.25 (2+2+1.5+0.75+0.75+0.75+0.5)
    max_raw = 8.25
    score_0_100 = (raw / max_raw) * 100.0
    return round(score_0_100, 4)