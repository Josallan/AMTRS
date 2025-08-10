AMTRS — Emotion-Based Music Recommendation System

Demo project that detects facial emotion from webcam and opens a Spotify playlist matching the mood.

## Quickstart
1. Copy `.env.template` to `.env` and fill SPOTIPY_CLIENT_ID / SECRET / REDIRECT.
2. pip install -r requirements.txt
3. python src/main.py

If you don't have Spotify credentials, the app will fallback to local playlists found in `data/local_playlists.json`.


amtrs-python/
├── README.md
├── requirements.txt
├── Dockerfile
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── face_emotion.py
│   ├── music_recommender.py
│   ├── config.py
│   └── utils.py
├── models/
│   └── (optional pretrained model or instructions)
├── data/
│   └── local_playlists.json
├── scripts/
│   ├── run.sh
│   └── train_placeholder.md
└── LICENSE
