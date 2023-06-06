from bs4 import BeautifulSoup
import os
import requests
def get_datafile_content(fname):
    data_file = os.path.join(os.path.dirname(__file__),"tests", "data", fname)
    with open(data_file) as f:
        data = f.read()
        return data
def get_artists(data):
    soup = BeautifulSoup(data, features="html.parser") # Create soup
    artists = soup.find_all("td", {"class": "td-last"}) # Search for all artist td nodes
    ret = []
    for i in artists: # For each td node
        a = i.find("a") # Get the anchor inside the td
        ret.append((a.text.strip(), a["href"])) # Extract the name and target from anchor
    return ret
def get_lyrics(data):
    soup = BeautifulSoup(data, features="html.parser") # Create soup
    artists = soup.find_all("table", {"class": "tracklist"}) # Search for all artist td nodes
    ret = []
    for i in artists: # For each td node
        a = i.find_all("a") [:5]# Get the anchor inside the td
        for b in a:
            ret.append((b.text.strip(), b["href"])) # Extract the name and target from anchor
    return ret
def get_artist_track_lyrics(data) :
    soup = BeautifulSoup(data, features="html.parser")
    lyrics = soup.find("p",{"id": "songLyricsDiv"})
    ret = ""
    if lyrics :
        ret = lyrics.text.strip()
    return ret
def create_artist_songlyrics_file(data):
    for artists in data :
        artist_name = artists[0]
        song_link = artists[1]
        song_response = requests.get(song_link)
        song_html_content = song_response.text
        artist_folder = os.path.join("artists", artist_name)
        os.makedirs(artist_folder, exist_ok=True)
        songs = get_lyrics(song_html_content)
        for song in songs :
            song_name = song[0].replace('/',"_")
            lyrics_link = song[1]
          
            lyrics_link = song[1]
            if lyrics_link:
                lyrics_response = requests.get(lyrics_link)
                lyrics_html_content = lyrics_response.text
                lyrics = get_artist_track_lyrics(lyrics_html_content)
                # song_folder = os.path.join(artist_folder, song_name)
                # os.makedirs(song_folder, exist_ok=True)
                song_filename = os.path.join(artist_folder, f"{song_name}.txt")
                with open(song_filename, "w") as fsong:
                    fsong.write(lyrics)
def main() :
    data = get_datafile_content("top-artists-lyrics.html")
    song_data = get_artists(data)[:5]
    create_artist_songlyrics_file(song_data)
if __name__ == "__main__":
    main()