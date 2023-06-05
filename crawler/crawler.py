from bs4 import BeautifulSoup

def get_artists(data):
    soup = BeautifulSoup(data, features="html.parser") # Create soup
    artists = soup.find_all("td", {"class": "td-last"}) # Search for all artist td nodes
    ret = []
    for i in artists: # For each td node
        a = i.find("a") # Get the anchor inside the td
        ret.append((a.text.strip(), a["href"])) # Extract the name and target from anchor
    return ret

def get_songs(data):
    soup = BeautifulSoup(data, features="html.parser") # Create soup
    songs = soup.find_all("table", {"class": "tracklist"})
    ret = []
    for i in songs: # 
        a = i.find("a") # 
        ret.append((a.text.strip(), a["href"])) # Extract the name and target from anchor
    return ret

def get_lyrics(data):
    soup = BeautifulSoup(data, features="html.parser") # Create soup
    lyrics = soup.find("p", {"id" :"songLyricsDiv"})
    ret = []
    # for i in lyrics:
    #     a = i.find("a")
    #     ret.append((a.text, a["href"]))
    if lyrics:
        ret = lyrics.text
   
    return ret


