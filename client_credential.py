from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys

client_id = '5a84b178e67f4296823227c0d8e629fc'
client_secret = '04065cabc4d24b9eb551c19b3383e298'

client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=True


features = sp.audio_features('4ytx0PQvxNbZwaplFx2Wd1')
data = json.dumps(features)
valence = data[0][0]['valence']