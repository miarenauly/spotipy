from mysql.connector import connect, Error
import nltk
from nltk.tag import pos_tag_sents

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

def fetch():
    try:
        cur.execute("select track_id, lyric from crawl_track")
        table = cur.fetchall()
        return table
    except:
    	pass

def tokenize(table):
	for data in table:
		lyric = data[1]
		if lyric == None:
			pass
		else:
			lyric = lyric.replace('\n','.')
			token = nltk.word_tokenize(lyric)
			pos_tag = nltk.pos_tag(token)
			return pos_tag

def sentiment(pos_tag):
	i=0
    while i>=0:
        try:
        	jj_count = 0
        	jj_neg = 0
        	jj_pos = 0
            tag = pos_tag[i][1]
            word = pos_tag[i][0]
            if tag == 'JJ':
            	jj_count += 1
            	#analyze the neg or pos of the word
            else:
            	pass
            i+=1
        except IndexError:
            break
    



