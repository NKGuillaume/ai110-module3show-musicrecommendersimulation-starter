# Reflection: Comparing Profile Outputs

---

## Pair 1 — High-Energy Pop vs. Chill Lofi

The High-Energy Pop profile wanted upbeat, danceable pop music, and it got exactly that: Sunrise City at the top with a 95/100 score. The Chill Lofi profile wanted quiet, acoustic, slow music and also got exactly what it asked for: Midnight Coding at 98/100.

These two profiles produced completely different top-5 lists with no overlap at all. That makes sense, because they are basically opposite listeners. One wants high energy and no acoustic instruments; the other wants low energy and lots of acoustic texture. The scoring treated them as completely different people and recommended completely different music.

**What this tells us about the system:** It works well when the user's preferences are clear and the catalog actually has songs in that genre. Both lofi and pop had at least two songs available, so both users got a strong #1 and a reasonable #2.

---

## Pair 2 — High-Energy Pop vs. Deep Intense Rock

Both profiles wanted high-energy, fast, intense music. The difference is genre and mood: Pop wants "happy," Rock wants "intense."

The High-Energy Pop results included Sunrise City, Rooftop Lights, and Gym Hero — all light, fun, radio-friendly songs. The Deep Intense Rock results included Storm Runner (the only rock song in the catalog) at #1, then Gym Hero at #2, then Thunderforge.

**Why does Gym Hero keep showing up?** Gym Hero (genre=pop, mood=intense, energy=0.93) is the song in the catalog with the highest energy. It appears in both lists because the system sees "this song has almost exactly the energy the user wants" and gives it points for that. For the Happy Pop user it gets a genre bonus (it is pop). For the Intense Rock user it gets a mood bonus (it is intense). It is the catalog's version of a jack-of-all-trades — it fits multiple profiles because its attributes are extreme enough to score well on energy no matter who is asking.

This is a good example of how a small catalog creates repetition. With only 18 songs, the high-energy ones appear for every high-energy user regardless of genre.

---

## Pair 3 — Chill Lofi vs. Conflicting Vibes

This is the most interesting comparison. Both profiles asked for genre=lofi and mood=chill. The only difference was energy: Chill Lofi wanted energy=0.40 (low and relaxed), while Conflicting Vibes wanted energy=0.92 (intense).

You might expect very different results. Instead, both profiles returned almost identical top-5 lists — the same two lofi/chill songs at #1 and #2.

**Why does this happen?** The genre and mood labels together are worth more points than all the audio features combined. So even though the Conflicting Vibes user explicitly said they want something with high energy, the system looked at the label "lofi/chill" and gave those songs such a large head start that no high-energy song could catch up. Midnight Coding has an energy of 0.42 — nowhere near the 0.92 the user wanted — but it still won because it had the right genre tag.

**What this means in plain language:** If you told a friend "I want something chill and lofi but really energetic," and your friend just kept handing you the same sleepy study music because it had the word "lofi" on the label, you would be frustrated. That is exactly what the system did. It heard "lofi" and stopped listening to the rest of what you said. This is the filter bubble problem in action.

---

## Pair 4 — Deep Intense Rock vs. Ghost Genre (k-pop)

Both profiles wanted high-energy, high-valence music at fast tempos. The difference is that Deep Intense Rock asked for a genre that exists in the catalog (rock) and Ghost Genre asked for k-pop, which has no songs in the catalog at all.

Deep Intense Rock: Storm Runner scored 97.7 at #1. The system found a perfect match.
Ghost Genre: The best result was Sunrise City at 86.7, which is a pop/happy song — not k-pop at all.

The system did not crash. It did not say "I have no k-pop." It just silently fell back to matching on mood and audio features, surfacing songs that felt energetic and happy even though they were nothing like what the user wanted.

**What this tells us:** The system degrades quietly, which sounds polite but is actually misleading. A real app should tell the user "we do not have k-pop in our catalog" rather than recommending pop songs and pretending they are a good match. Silence about missing genres is a form of bias — it hides the gap instead of acknowledging it.

---

## Pair 5 — Ghost Genre vs. All Neutral

Both profiles produced results without any genre bonus. Ghost Genre had no matching genre in the catalog; All Neutral had no genre set at all.

Ghost Genre still got a mood bonus (the user wanted mood=happy, and two songs matched). Its top score was 86.7. All Neutral got no categorical bonus at all and maxed out around 55.

**The difference:** The Ghost Genre user, despite being underserved, at least got recommendations driven by a mood preference. The All Neutral user got essentially a random list — five songs within 5 points of each other, ranked by tiny differences in energy and danceability proximity to 0.5.

**What this tells us:** Mood is a surprisingly powerful rescue signal. Even when genre fails completely, knowing "this person wants happy music" is enough to meaningfully filter the catalog. A system that collects even one piece of preference data is dramatically better than one that knows nothing. This is why real apps push you to pick a few genres or artists immediately after you sign up — a totally blank profile produces useless recommendations.

---

## Summary

| Profile pair | Key difference | What it reveals |
|---|---|---|
| Pop vs. Lofi | Opposite tastes, zero overlap in results | System works well when preferences are clear |
| Pop vs. Rock | Both high-energy, different genre/mood | High-energy songs (Gym Hero) appear for both — small catalog creates repetition |
| Lofi vs. Conflicting Vibes | Same labels, opposite energy target | Genre+mood labels overpower audio features — filter bubble |
| Rock vs. Ghost Genre | One genre exists, one does not | System fails silently for missing genres |
| Ghost Genre vs. All Neutral | One has a mood signal, one has nothing | Even a single preference dramatically improves results |
