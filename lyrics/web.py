from flask import Flask

import models

app = Flask("lyrics")


@app.route("/")
def index():
    db = models.init_db(app)
    artists_count = db.session.scalar(db.select(db.func.count(models.Artist.id)))
    tracks_count = db.session.scalar(db.select(db.func.count(models.Tracks.id)))
    return f"<h1>Welcome to the lyrics server. We have {artists_count} artists and {tracks_count} tracks.</h1>"

@app.route("/user/<id>")
def users(id):
    return f"You asked for user {id}"

@app.route("/artists")
def list_artist():
    db = models.init_db(app)
    print(db)
    artists = db.session.execute(db.select(models.Artist.name))
    print(artists)
    artist_name = [artist.name for artist in artists]
    print(artist_name)
    ret = "<h1>Artists</h1>"
    for idx,name in enumerate(artist_name, start=1):
        ret += f"{idx}.{name}<br>"
        # return f"<ul><li>{idx}.{name}</li></ul>"

    return f'{ret}'
    

@app.route("/artists/tracks")
def tracks():
    db = models.init_db(app)
    artists = db.session.execute(db.select(models.Artist)).scalars()
    output = []
    for artist in artists:
        artist_tracks = db.session.execute(db.select(models.Tracks).where(models.Tracks.artist_id == artist.id)).scalars()
        artist_track_names = set([track.name for track in artist_tracks]) 
        output.append(f"{artist.name}: {', '.join(artist_track_names)}")
    return "<br><br>".join(output)    