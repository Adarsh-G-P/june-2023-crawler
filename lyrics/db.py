import psycopg2

db = psycopg2.connect("dbname=students")

# DB functions
def initdb():
    cur = db.cursor()
    with open("data/init.sql") as f:
        cur.execute(f.read())
    db.commit()
    cur.close()
    
def get_artists():
    cur = db.cursor()
    cur.execute("SELECT name from artists ORDER BY name")
    artists = cur.fetchall()
    ret = []
    for i in artists:
        ret.append(i[0])
    cur.close()
    return ret

def save_track_to_db(artist, track, lyrics, db=db):
    cur = db.cursor()
    cur.execute("SELECT id from artists where name = %s", (artist,))
    artist_id = cur.fetchone()
    if artist_id:
        artist_id = artist_id[0]
    else:
        cur.execute("INSERT INTO artists (name) VALUES(%s)", (artist,));
        cur.execute("SELECT id from artists where name = %s", (artist,))
        artist_id = cur.fetchone()[0]
    cur.execute("INSERT INTO tracks (artist_id, name, lyrics) VALUES (%s, %s, %s)", (artist_id, track, lyrics));
    db.commit()
    cur.close()