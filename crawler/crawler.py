import os

import psycopg2
import requests
from bs4 import BeautifulSoup

db = psycopg2.connect("dbname=students")

# DB functions
def initdb():
    cur = db.cursor()
    with open("init.sql") as f:
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

# def get_song():
#     cur = db.cursor()
#     cur.execute

# Crawler functions
def crawl_artists(data, count=10):
    
    soup = BeautifulSoup(data, features="html.parser") # Create soup
    artists = soup.find_all("td", {"class": "td-last"}) # Search for all artist td nodes
    ret = []
    for i in artists: # For each td node
        a = i.find("a") # Get the anchor inside the td
        ret.append((a.text.strip(), a["href"])) # Extract the name and target from anchor
        if count is not None:
            if count.isnumeric():
                count = int(count) - 1

                if count == 0:
                    break

    return ret

def crawl_tracks_of_artist(data, count=5):
   
    soup = BeautifulSoup(data, features="html.parser")
    tracks = soup.find("table", {"class" : "tracklist"})
    ret = []
    for track in list(tracks.find_all("a")):
        lyrics_page = requests.get(track['href']).text
        lyrics = extract_lyrics(lyrics_page)
        ret.append([track.text.strip(), lyrics])
        if count is not None:
            count -=1
            if count == 0:
                break

    return ret
    
def extract_lyrics(data):
    soup = BeautifulSoup(data, features="html.parser")    
    lyrics = soup.find("p", {"id" : "songLyricsDiv"})
    if lyrics:
        lyrics = lyrics.text
    else:
        lyrics = ""
    return lyrics


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


def save_track(artist, track, lyrics, base="lyrics_crawl"):
   

    artist = artist.replace("/","_").replace(" ","_").lower()
    track = track.replace("/","_").replace(" ","_").lower()
    artist_dir = os.path.join(base, artist)

    if not os.path.exists(artist_dir):
        os.makedirs(artist_dir)
    
    track_path = os.path.join(artist_dir, track) + ".txt"
    
    with open(track_path, "w") as f:
        f.write(lyrics)
    

def crawl(start_url, nartists, ntracks):
    data = requests.get(start_url).text
    artists = crawl_artists(data, nartists)
    for artist_name, artist_link in artists:
        print (f"{artist_name} : ", end="", flush = True)
        tracks_page = requests.get(artist_link).text
        tracks = crawl_tracks_of_artist(tracks_page, ntracks)
        for track_name, lyrics in tracks:
            save_track(artist_name, track_name, lyrics)
            save_track_to_db(artist_name, track_name, lyrics)
            print (".", end="", flush=True)
        print()

def get_song(artist_name):
    cur = db.cursor()
    cur.execute("SELECT tracks.name FROM tracks JOIN artists ON tracks.artist_id = artists.id WHERE artists.name = %s", (artist_name,))
    tracks = cur.fetchall()
    result = []
    cur.close()   
    for track in tracks:
        result.append(track[0])   

    return result