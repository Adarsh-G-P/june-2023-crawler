import os

import crawler

def test_get_popular_artists():
    data_file = os.path.join(os.path.dirname(__file__), "data", "top-artists-lyrics.html")
    with open(data_file) as f:
        data = f.read()
    artists = crawler.get_artists(data)
    name0, link0 = artists[0]
    name1, link1 = artists[1]
    name99, link99 = artists[98]
    name100, link100 = artists[99]

    assert len(artists) == 100

    assert name0 == "Hillsong"
    assert link0 == "https://www.songlyrics.com/hillsong-lyrics/"
    assert name1 == "Eminem"
    assert link1 == "https://www.songlyrics.com/eminem-lyrics/"

    assert name99 == "Skrillex"
    assert link99 == "https://www.songlyrics.com/skrillex-lyrics/"

    assert name100 == "Shakira"
    assert link100 == "https://www.songlyrics.com/shakira-lyrics/"

def test_get_list_songs():
    data_file = os.path.join(os.path.dirname(__file__), "data", "list_songs.html")
    with open(data_file) as f:
        data = f.read()
    songs = crawler.get_songs(data)
    song1, link1 = songs[0] 
    # song2, link2 = songs[1]
    # songs482, link482 = songs[481]
    # songs483, link483 = songs[482]

    # assert len(songs) == 483      
    
    assert song1 == "Oceans (Where Feet May Fail)"
    assert link1 == "https://www.songlyrics.com/hillsong/oceans-where-feet-may-fail-lyrics/"

    # assert song2 == "This Is Our God"
    # assert link2 == "https://www.songlyrics.com/hillsong/this-is-our-god-lyrics/"
     
    # assert songs482 == "In Your Hands"
    # assert link482 == "https://www.songlyrics.com/hillsong/in-your-hands-lyrics/"
    
    # assert songs483 == "God Is In The House(Live)"
    # assert link483 == "https://www.songlyrics.com/hillsong/god-is-in-the-house-live-lyrics/"
    


def test_get_lyrics():
    data_file = os.path.join(os.path.dirname(__file__), "data", "lyrics.html")
    with open(data_file) as f:
        data = f.read()
    lyrics = crawler.get_lyrics(data)
    assert lyrics.startswith("You call me out upon the waters")
    print(lyrics)


    # lyrics_start_with, lyrics_end_with = songs[0]
    # assert lyrics_start_with.startwith() == "You call me out upon the waters"
    # assert lyrics_end_with == "You call me out upon the waters"