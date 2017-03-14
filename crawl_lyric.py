import requests
import json
from bs4 import BeautifulSoup
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


def find_lyric_url(song_title,artist_name):
    base_url = "http://api.genius.com"
    headers = {'Authorization': 'Bearer TOKEN'}
    song_title = song_title.replace(' ','%20')
    search_url = base_url + "/search?q=" + song_title
    response = requests.get(search_url, headers=headers)
    content = response.text
    #print content.encode('ascii', 'ignore')
    json_data = json.loads(content)
    #print json_data

    song_info = None
    for hit in json_data["response"]["hits"]:
    	if hit["result"]["primary_artist"]["name"] == artist_name:
    		song_info = hit
    		#print json.dumps(song_info, indent=4)
    		song_url=song_info['result']['url']
    		#print song_url
    		return song_url
    		break
    	if song_info:
    		pass

def scrap_lyric(page_url):
    page_url = str(page_url)
    page = requests.get(page_url)
    html = BeautifulSoup(page.text, "html.parser")
    #remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html('script')]
    #at least Genius is nice and has a tag called 'lyrics'!
    lyrics = html.find("lyrics").get_text()
    lyrics = lyrics.encode('ascii','ignore')
    return lyrics

def alter_table():
    try:
        query = "alter table crawl_track add column lyrics text"
        cur.execute(query)
        conn.commit()
    except:
        pass

def insert_data(track_id,lyrics):
    try:
    	query = "update crawl_track set lyrics = '%s' where track_id = '%s'" %(lyrics, track_id)
        cur.execute(query)
        conn.commit()
    except Error,e:
        conn.rollback() 

def fetch():
    query = "select track_id, track_name, track_artist from crawl_track"
    cur.execute(query)
    table = cur.fetchall()
    return table

def main():
    table = fetch()
    for row in table:
        track_id = row[0]
        track_name = row[1]
        track_artist = row[2]
        url = find_lyric_url(track_name,track_artist)
        print url
#       try:
        lyrics = scrap_lyric(url)
        insert_data(track_id,lyrics)
#        except requests.exceptions.MissingSchema:
#            pass
main()