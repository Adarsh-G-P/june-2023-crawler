import logging
import os
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
    

def setup_logger(debug):
    l = logging.getLogger("lyrics")
    l.setLevel(logging.DEBUG)
    h = logging.StreamHandler()
    if debug:
        h.setLevel(logging.DEBUG)
    else:
        h.setLevel(logging.INFO)
    h.setFormatter(logging.Formatter("[%(levelname)s] %(filename)s:%(lineno)d : %(message)s"))
    l.addHandler(h)
    
def get_logger():
    return logging.getLogger("lyrics")