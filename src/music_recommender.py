"""
Spotify integration using spotipy with caching and backoff.
If Spotify credentials are missing, falls back to local playlists from data/local_playlists.json.
"""
import json
import os
import logging
import webbrowser
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from src import config
from src.utils import wait_exponential
import time

logger = logging.getLogger('amtrs.music')


class MusicRecommender:
    def __init__(self):
        self.sp = None
        self.cache = {}
        if config.SPOTIPY_CLIENT_ID and config.SPOTIPY_CLIENT_SECRET:
            scope = "playlist-read-private"
            self.sp = Spotify(auth_manager=SpotifyOAuth(client_id=config.SPOTIPY_CLIENT_ID,
                                                       client_secret=config.SPOTIPY_CLIENT_SECRET,
                                                       redirect_uri=config.SPOTIPY_REDIRECT_URI,
                                                       scope=scope))
        # load local playlists
        if os.path.exists(config.LOCAL_PLAYLISTS_PATH):
            with open(config.LOCAL_PLAYLISTS_PATH,'r') as f:
                self.local_playlists = json.load(f)
        else:
            self.local_playlists = {}

    def search_playlist(self, query, limit=config.SPOTIFY_SEARCH_LIMIT):
        """Search for playlists on Spotify with retry/backoff. Returns playlist URI or None"""
        if query in self.cache:
            logger.info('Cache hit for query: %s', query)
            return self.cache[query]
        if self.sp is None:
            logger.info('Spotify not configured — fallback to local')
            return self._local_for_query(query)

        # simple retry loop
        attempts = 0
        while attempts < 5:
            try:
                res = self.sp.search(q=query, type='playlist', limit=limit)
                items = res.get('playlists', {}).get('items', [])
                if items:
                    uri = items[0]['uri']
                    self.cache[query] = uri
                    logger.info('Found playlist: %s', uri)
                    return uri
                else:
                    logger.info('No playlist found for %s', query)
                    return None
            except Exception as e:
                attempts += 1
                wait = min(2**attempts, 60)
                logger.warning('Spotify search failed: %s. Retrying in %s sec', e, wait)
                time.sleep(wait)
        return None

    def _local_for_query(self, emotion):
        # try direct match
        if emotion in self.local_playlists:
            return self.local_playlists[emotion][0]
        # fallback to 'default'
        return self.local_playlists.get('default', [None])[0]

    def open_playlist_in_browser(self, uri):
        if not uri:
            logger.warning('No playlist uri to open')
            return False
        # spotify:playlist:xxxxx -> https://open.spotify.com/playlist/xxxxx
        if uri.startswith('spotify:playlist:'):
            pid = uri.split(':')[-1]
            url = f'https://open.spotify.com/playlist/{pid}'
        elif uri.startswith('https://'):
            url = uri
        else:
            url = uri
        webbrowser.open(url)
        return True
