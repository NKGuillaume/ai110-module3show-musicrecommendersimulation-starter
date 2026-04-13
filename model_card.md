# 🎧 Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeMatch 1.0**

A simple music recommender that matches songs to what a user says they like.

---

## 2. Intended Use

This tool suggests songs from a small catalog based on a user's taste profile.

It is meant for a classroom project — not for real users.

It works best when the user knows what genre and mood they want.

It should not be used if the genre they want is not in the catalog, because it will just return the wrong songs without saying anything.

---

## 3. How the Model Works

Every song gets a score out of 100.

If the song's genre matches what the user wants, it gets bonus points. Same for mood.

Then it checks how close the song's energy is to what the user wants. Energy matters the most out of all the audio features.

After that it looks at valence (happy vs. sad feel), danceability, acousticness, and tempo.

All the points are added up and the top 5 songs win.

Each result also shows why the song was picked — like "genre match (+1.0)" or "energy fit (+2.8)" — so it is easy to understand.

---

## 4. Data

There are 18 songs in the catalog.

Each song has: genre, mood, energy, tempo, valence, danceability, and acousticness.

There are 15 genres and 13 moods represented.

But 13 of those 15 genres only have one song each. So most genre searches always return the same #1 song.

The catalog also has more high-energy songs than low-energy ones.

There are no lyrics, no popularity scores, and no release dates.

---

## 5. Strengths

It works really well when the user wants lofi, pop, or rock — those genres have more than one song.

Every result comes with a reason, so you can see exactly why a song ranked where it did.

It never crashes. Even if you give it a genre that doesn't exist, it still returns something.

It is easy to tune — changing one weight number changes the whole ranking.

---

## 6. Limitations and Bias

Most genres only have one song. That one song always wins for anyone who picks that genre, no matter what.

For example, rock has one song — Storm Runner. A rock user will always get Storm Runner at #1, every time, forever. That is a filter bubble.

The genre and mood labels are also very powerful. In one test, a user asked for high-energy music but had "lofi" as their genre. The system still gave them quiet lofi songs because the genre label was worth so many points it drowned out everything else.

The system also has no way to tell the user "sorry, we don't have that genre." It just quietly returns whatever is closest, which can be confusing.

---

## 7. Evaluation

Six profiles were tested against the 18-song catalog.

Three were normal: High-Energy Pop, Chill Lofi, and Deep Intense Rock.

Three were designed to break things: one had a genre not in the catalog (k-pop), one had totally contradictory preferences (lofi + high energy), and one had no preferences at all.

The normal profiles worked great. The right songs came back at the top.

The biggest surprise was the contradictory profile. Even though the user asked for energy=0.92, the system returned quiet lofi songs because the genre label was too powerful to overcome.

The blank profile was also interesting. With nothing to go on, all five results were basically tied — the system had no idea what to do.

A weight experiment was also run. Halving the genre bonus and doubling the energy weight changed a few rankings in ways that felt more accurate.

---

## 8. Future Work

Add more songs. Most genres only have one, which means there is no real competition. More songs would make the scores actually mean something.

Add a diversity rule. Something like "no more than 2 songs from the same genre in the top 5" would help users discover more of the catalog.

Tell the user when their genre is missing. Right now it just silently returns wrong results. A simple warning would make it way more honest.

---

## 9. Personal Reflection

I thought recommenders had to learn from your history to work. This project showed me that even a totally static formula can give decent results if the user tells you what they want.

The weirdest thing I learned is how much the labels matter. Two songs can sound similar, but if one is tagged "lofi" and one is tagged "ambient" they get treated completely differently.

The contradictory profile test stuck with me. The system wasn't broken — it was doing exactly what the math said. But it gave the wrong result. That made me think real apps probably do this too, and users just never know.
