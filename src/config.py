
import os
from dotenv import load_dotenv
load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI', 'http://localhost:8888/callback')

# Fallback playlists map emotion -> list of playlist URIs or local file paths
LOCAL_PLAYLISTS_PATH = 'data/local_playlists.json'

# Model / detector settings
DETECTOR_CONFIDENCE = float(os.getenv('DETECTOR_CONFIDENCE', 0.35))

# App settings
MAX_DETECTIONS = int(os.getenv('MAX_DETECTIONS', 5))

# Spotify search settings
SPOTIFY_SEARCH_LIMIT = int(os.getenv('SPOTIFY_SEARCH_LIMIT', 1))
