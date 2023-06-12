import argparse

import crawler
import requests
import db
import utils
def parse():
    parser = argparse.ArgumentParser(
        prog = "lyrics",
        description = "Offline song lyrics browser")
    
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("listartists", help = "List of artists in the system")
    subparsers.add_parser("initdb", help = "Initialise the database")
    subparsers.add_parser("song", help = "song crawl")
    crawl_parser = subparsers.add_parser("crawl", help = "Crawl lyrics")
    song_parser = subparsers.add_parser("song", help = "Song lyrics")


    crawl_parser.add_argument("--nartists", help="Number of artists to crawl (Default : %(default)s)", 
                              type=int, 
                              default=8)

    crawl_parser.add_argument("--ntracks", help="Number of tracks to crawl per artist (Default : %(default)s)",
                              type=int,
                              default=5)
    song_parser.add_argument("--artist",help = "Name of artist to crawl (Default:%(default)s)",
                            type = str,
                            # default =
                            )
    song_parser.add_argument("--ntracks",help = "Number of tracks to crawl as per artist(Default:%(default)s)",
                            type = int,
                            default = 5
                            )

    args = parser.parse_args()
    return args

def handle_listartists(args):
    artists = crawler.get_artists()
    for idx, name in enumerate(artists, start=1):
        print (f"{idx}. {name}")

def handle_initdb(args):
    crawler.initdb()

def handle_crawl(args):
    print (args)
    crawler.crawl("https://www.songlyrics.com/top-artists-lyrics.html", 
                    args.nartists, 
                    args.ntracks)

def handle_song(args):
    artist = args.artist
    print(artist)
    url = "https://www.songlyrics.com/" + artist.lower() + "-lyrics/"
    print(url)
    song = crawler.get_song(artist)

    if song is not None:
        for i in song:
            print(i)

    else:
        print("Sorry, no songs found for artist", artist)


def main():
    commands = {"listartists" : handle_listartists,
                "initdb"  : handle_initdb ,
                "crawl" : handle_crawl,
                "song" : handle_song}

    args = parse()
    commands[args.command](args)

if __name__ == "__main__":
    main()