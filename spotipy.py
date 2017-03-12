import requests
import json
import spotipy

def search_artist_uri(str):
	#search artist
    endpoint = "https://api.spotify.com/v1/search?query="+artist_name+"&limit=1&type=artist"
    artist_name = str
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
    print list_album

def get_tracks(uri,list_tracks):
    endpoint = "https://api.spotify.com/v1/albums/"+uri+"/tracks"
    r = requests.get(endpoint)
    content = r.text
    json_data = json.loads(content)
    i=0
    while i>=0:
        try:
            track_uri = json_data[u'items'][i][u'uri']
            track_uri = track_uri.replace('spotify:track:','')
            list_tracks.append(track_uri)
            i+=1
        except IndexError:
            break
    print list_tracks

'''
def authorize(client_id):
    client_id = ''
    redirect_uri = 'https://medium.com/@miarenauly'
    endpoint = "https://accounts.spotify.com/authorize/?client_id="+client_id+"&response_type=code&scope=playlist-modify-public playlist-modify-private&redirect_uri="+redirect_uri
    r = requests.get(endpoint)
    code = r.url
'''

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

def get_audio_feature(uri,token):
    endpoint = "https://api.spotify.com/v1/audio-features/"+uri
    headers = {'Authorization': 'Bearer '+ token}
    r = requests.get(endpoint, headers=headers)
    content = r.text
    json_data = json.loads(content)
    i=0
    while i>=0:
    	#baru sampe sini
        
def main(str):
    client_id = ''
    client_secret = ''
    artist = str
    list_album = get_album(search_artist_uri(artist))
    list_tracks = []
    for album in list_album:
        get_tracks(album,list_tracks)
    code = ''
    token = get_token(code,client_id,client_secret)
    for track in list_tracks:
        get_audio_feature(track,token)

main()