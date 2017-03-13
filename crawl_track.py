from __future__ import print_function    # (at top of module)
from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import sys
import requests
from mysql.connector import connect, Error


dbhost = ''
dbuser = ''
dbpass = ''
dbname = ''
dbport = 3139

conn = connect(host = dbhost,
        user = dbuser,
        password = dbpass,
        database = dbname,
        port = dbport)

cur = conn.cursor()


def making_table():
    try:
        cur.execute('''CREATE TABLE crawl_track
        (album_uri varchar (255) DEFAULT NULL,
        album_name varchar (255) DEFAULT NULL,
        track_uri varchar (255) DEFAULT NULL,
        track_artist varchar (255) DEFAULT NULL,
        track_name varchar (255) DEFAULT NULL,
        track_href varchar (255) DEFAULT NULL,
        analysis_url varchar(255) DEFAULT NULL,
        energy varchar(255) DEFAULT NULL,
        liveness varchar(255) DEFAULT NULL,
        tempo varchar(255) DEFAULT NULL,
        speechiness varchar(255) DEFAULT NULL,
        uri varchar(255) DEFAULT NULL,
        acousticness varchar(255) DEFAULT NULL,
        instrumentalness varchar(255) DEFAULT NULL,
        time_signature varchar(255) DEFAULT NULL,
        danceability varchar(255) DEFAULT NULL,
        track_key varchar(255) DEFAULT NULL,
        duration_ms varchar(255) DEFAULT NULL,
        loudness varchar(255) DEFAULT NULL,
        valence varchar(255) DEFAULT NULL,
        track_type varchar(255) DEFAULT NULL,
        track_id varchar(255) DEFAULT NULL,
        mode varchar(255) DEFAULT NULL
        );''')
        print ("Table created successfully")
        conn.commit()
    except:
        pass

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
            album_name = json_data[u'items'][i][u'name']
            album_data = [album_uri,album_name]
            list_album.append(album_data)
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
            track_artist = json_data[u'items'][i][u'artists'][0][u'name']
            track_name = json_data[u'items'][i][u'name']
            track_data = [track_uri, track_artist, track_name]
            list_tracks.append(track_data)
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
    data = json.dumps(features)
    json_data = json.loads(data)
    track_href = json_data[0]['track_href']
    analysis_url = json_data[0]['analysis_url']
    energy = json_data[0]['energy']
    liveness = json_data[0]['liveness']
    tempo = json_data[0]['tempo']
    speechiness = json_data[0]['speechiness']
    uri = json_data[0]['uri']
    acousticness = json_data[0]['acousticness']
    instrumentalness = json_data[0]['instrumentalness']
    time_signature = json_data[0]['time_signature']
    danceability = json_data[0]['danceability']
    key = json_data[0]['key']
    duration_ms = json_data[0]['duration_ms']
    loudness = json_data[0]['loudness']
    valence = json_data[0]['valence']
    type_track = json_data[0]['type']
    id_track = json_data[0]['id']
    mode = json_data[0]['mode']
    return track_href, analysis_url, energy, liveness, tempo, speechiness, uri, acousticness, instrumentalness, time_signature, danceability, key,\
    duration_ms, loudness, valence, type_track, id_track, mode

def insert_data(data, album_uri, album_name, track_uri, track_artist, track_name):
    try:
        print (data)
        query = "insert into crawl_track values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
            % (album_uri,album_name,track_uri,track_artist,track_name, data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],\
            data[11],data[12],data[13], data[14],data[15],data[16],data[17])
        print (query)
        cur.execute(query)
        conn.commit()
    except Error,e:
        conn.rollback()

def main(str):
    making_table()
    artist = str
    list_album = get_album(search_artist_uri(artist))
    for album in list_album:
        list_tracks = []
        album_uri = album[0]
        album_name = album[1]
        a_list = get_tracks(album[0])
        list_tracks = a_list + list_tracks
        for track in list_tracks:
            track_uri = track[0]
            track_artist = track[1]
            track_name = track[2]
            data = get_audio_feature(track_uri)
            insert_data(data,album_uri,album_name,track_uri,track_artist,track_name)

main('coldplay')