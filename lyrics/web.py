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
