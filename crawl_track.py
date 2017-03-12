from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import sys
import requests

def search_artist_uri(str):
    #search artist
    artist_name = str
    endpoint = "https://api.spotify.com/v1/search?query="+artist_name+"&limit=1&type=artist"
    artist_name = artist_name.replace(' ','+')
    r = requests.get(endpoint)
    content = r.text
    json_data = json.loads(content)
    artist_uri = json_data[u'artists'][u'items'][0][u'uri']
    artist_uri = artist_uri.replace('spotify:artist:','')
    return artist_uri

def get_album(uri):
    endpoint = "https://api.spotify.com/v1/artists/"+uri+"/albums?market=ID&album_type=album"
    r = requests.get(endpoint)
    content = r.text
    json_data = json.loads(content)
    list_album = []
    i=0
    while i>=0:
        try:
            album_uri = json_data[u'items'][i][u'uri']
            album_uri = album_uri.replace('spotify:album:','')
            list_album.append(album_uri)
            i+=1
        except IndexError:
            break
    return list_album

def get_tracks(uri):
    endpoint = "https://api.spotify.com/v1/albums/"+uri+"/tracks"
    r = requests.get(endpoint)
    content = r.text
    json_data = json.loads(content)
    i=0
    list_tracks = []
    while i>=0:
        try:
            track_uri = json_data[u'items'][i][u'uri']
            track_uri = track_uri.replace('spotify:track:','')
            list_tracks.append(track_uri)
            i+=1
        except IndexError:
            break
    return list_tracks

'''
def authorize(client_id):
    client_id = ''
    redirect_uri = 'https://medium.com/@miarenauly'
    endpoint = "https://accounts.spotify.com/authorize/?client_id="+client_id+"&response_type=code&scope=playlist-modify-public playlist-modify-private&redirect_uri="+redirect_uri
    r = requests.get(endpoint)
    code = r.url


def get_token(code,client_id, client_secret):
    code = ''
    endpoint = 'https://accounts.spotify.com/api/token'
    body = {'grant_type': 'authorization_code',
            'code ': '',
            'redirect_uri ': 'https://medium.com/@miarenauly',
            'client_id': '',
            'client_secret': '',}
    body['code']='code'
    body['client_id']=client_id
    body['client_secret']=client_secret
    r = requests.post(endpoint, data=body)
    content = r.text
    json_data = json.loads(content)
    token = json_data['access_token']
    return token
'''

def get_audio_feature(uri):
    client_id = ''
    client_secret = ''
    uri = (str(uri)).replace(',','')
    client_credentials_manager = SpotifyClientCredentials(client_id,client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace=True
    features = sp.audio_features(uri)
    print(json.dumps(features, indent=4))
        
def main(str):
    artist = str
    list_album = get_album(search_artist_uri(artist))
    list_tracks = []
    for album in list_album:
        a_list = get_tracks(album)
        list_tracks = a_list + list_tracks
    for track in list_tracks:
        get_audio_feature(track)

main('coldplay')