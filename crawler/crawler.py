import os

import psycopg2
import requests
from bs4 import BeautifulSoup

db = psycopg2.connect("dbname=students")

def get_artists(data, count=10):
    """
    Inputs :
      1. HTML string which contains a list of artists. 
      2. Count is the maximum number of artists that will be returned.

    Outputs:
      1. A list each element of which is of the form
         ("artist name", link to tracks of artist)

    Description of what this does:
      Parses the input HTML, find the list of artists. Creates a list as mentioned in outputs and returns the list
    
    """

    soup = BeautifulSoup(data, features="html.parser") # Create soup
    artists = soup.find_all("td", {"class": "td-last"}) # Search for all artist td nodes
    ret = []
    for i in artists: # For each td node
        a = i.find("a") # Get the anchor inside the td
        ret.append((a.text.strip(), a["href"])) # Extract the name and target from anchor
        if count == 0:
            break
        count -= 1
    return ret

def get_tracks_of_artist(data, count=5):
    """
    Inputs : 
      HTML string which contains all tracks of a single artist

    Outputs :
      A list each element of which is of the form
      ("track name", "lyrics of the song")

    Description : 
      Parses the input HTML to find all the tracks of the artist. Creates a list like mentioned in the output
    
    """
    soup = BeautifulSoup(data, features="html.parser")
    tracks = soup.find("table", {"class" : "tracklist"})
    ret = []
    for track in list(tracks.find_all("a")):
        lyrics_page = requests.get(track['href']).text
        lyrics = extract_lyrics(lyrics_page)
        ret.append([track.text.strip(), lyrics])
        if count == 0:
            break
        count -=1
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
    print("Id is ", artist_id)

    cur.execute("INSERT INTO tracks (artists_id,name,lyrics) values (%s,%s,%s)",(artist_id,track,lyrics,))
    # cur.execute ("select id from tracks where artists_id=%s",(artist_id,track))
    db.commit()
    cur.close()


def save_track(artist, track, lyrics, base="lyrics_crawl"):
    """
    Inputs : 
       1. artist - String containing the name of the artist
       2. track - String containing name of the track of the artist
       3. Lyrics - String containing lyrics of the above track
       4. base - Base directory to store the artist lyrics

    Outputs: 
       None

    Description: 
       Creates files of the forms
    {artist_name}/{track_name}.txt and stores the lyrics inside them.

    """

    artist = artist.replace("/","_").replace(" ","_").lower()
    track = track.replace("/","_").replace(" ","_").lower()
    artist_dir = os.path.join(base, artist)

    if not os.path.exists(artist_dir):
        os.makedirs(artist_dir)
    
    track_path = os.path.join(artist_dir, track) + ".txt"
    
    with open(track_path, "w") as f:
        f.write(lyrics)
    

def crawl(start_url):
    data = requests.get(start_url).text
    artists = get_artists(data)
    for artist_name, artist_link in artists:
        print (f"{artist_name} : ", end="", flush = True)
        tracks_page = requests.get(artist_link).text
        tracks = get_tracks_of_artist(tracks_page)
        for track_name, lyrics in tracks:
            save_track(artist_name, track_name, lyrics)
            save_track_to_db(artist_name, track_name, lyrics)
            print (".", end="", flush=True)
        print()

if __name__ == "__main__":
    crawl("https://www.songlyrics.com/top-artists-lyrics.html")