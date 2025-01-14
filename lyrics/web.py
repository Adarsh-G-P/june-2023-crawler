from flask import Flask, Response, render_template, request, jsonify

import models

app = Flask("lyrics")


@app.route("/")
def index():
    db = models.init_db(app)
    artists = db.session.execute(db.select(models.Artist)).scalars()
    return render_template("index.html", artists = artists)

@app.route("/artist/<artist_id>")
def artist(artist_id):
    db = models.init_db(app)
    artists = db.session.execute(db.select(models.Artist)).scalars()
    artist = db.session.execute(db.select(models.Artist).filter(models.Artist.id == artist_id)).scalar()
    track = db.session.execute(db.select(models.Tracks).filter(models.Tracks.id == artist_id)).scalar()

    return render_template("artists.html", artists = artists, current = artist,track=track)


# @app.route("/song/<song_id>",methods = ['POST','GET'])
# def update_lyrics(song_id):
#     db = models.init_db(app)
#     artists = db.session.execute(db.select(models.Artist)).scalars()
#     track = db.session.execute(db.select(models.Tracks).filter(models.Tracks.id == song_id)).scalar()

#     # Check if the "Accept" header contains "application/json"
#     if "application/json" in request.headers.get("Accept", ""):
#         # Return JSON if the header is set to "application/json" or contains "application/json"
#         return jsonify({"name":track.name, "lyrics":track.lyrics,})
#     else:
#         # Render the HTML template for other requests
#         return render_template("lyrics.html", artists=artists, current=track.artist, track=track)


@app.route("/song/<song_id>")
def song(song_id):
    print (request.headers)
    db = models.init_db(app)
    artists = db.session.execute(db.select(models.Artist)).scalars()
    track = db.session.execute(db.select(models.Tracks).filter(models.Tracks.id == song_id)).scalar()
    print (f"|{request.headers['Accept']}|");
    if request.headers['Accept'] == "application/json":
        return jsonify({"name":track.name,
                        "lyrics":track.lyrics})
    else:
        return render_template("track.html", artists = artists, current = track.artist, track = track)


@app.route("/songs/<artist_id>")
def songs(artist_id):
    db = models.init_db(app)
    artist = db.session.execute(db.select(models.Artist).filter(models.Artist.id == artist_id)).scalar()
    tracks = []
    for i in artist.tracks:
        t = {"id" : i.id,
             "name" : i.name,
             "lyrics" : i.lyrics}
        tracks.append(t)

    ret = { "current" : 0,
            "tracks": tracks}
    return jsonify(ret)

@app.route("/user/<id>")
def users(id):
    return f"You asked for user {id}"




# from flask import Flask, Response, render_template

# import models

# app = Flask("lyrics")


# @app.route("/")
# def index():
#     db = models.init_db(app)
#     artists = db.session.execute(db.select(models.Artist)).scalars()
#     return render_template("index.html", artists = artists)

# @app.route("/artist/<artist_id>")
# def artist(artist_id):
#     db = models.init_db(app)
#     artists = db.session.execute(db.select(models.Artist)).scalars()
#     artist = db.session.execute(db.select(models.Artist).filter(models.Artist.id == artist_id)).scalar()
#     return render_template("artists.html", artists = artists, current = artist)


# @app.route("/song/<song_id>")
# def song(song_id):
#     db = models.init_db(app)
#     artists = db.session.execute(db.select(models.Artist)).scalars()
#     track = db.session.execute(db.select(models.Tracks).filter(models.Tracks.id == song_id)).scalar()
#     lyrics_list =track.lyrics.split('\n\n')
#     ret = []
#     for line in lyrics_list:
#         ret.append(line)
#     return render_template("lyrics.html", artists = artists, current = track.artist, track = track,lyrics=ret)




# @app.route("/user/<id>")
# def users(id):
#     return f"You asked for user {id}"
