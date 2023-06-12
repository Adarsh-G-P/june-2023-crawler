import os

import psycopg2
import requests
from bs4 import BeautifulSoup
import lyrics as lyricsdb
import lyrics.utils as utils


db = psycopg2.connect("dbname=students")

logger = utils.get_logger()


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

