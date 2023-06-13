from flask_sqlalchemy import SQLAlchemy

import web

db = SQLAlchemy()

def init_db(app, db_uri=""):
    try:
        app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
        db.init_app(app)
    except RuntimeError:
        pass
    return db
    
class Artist(db.Model):
    __tablename__ = "artists"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    tracks = db.relationship("Tracks", back_populates="artist")

class Tracks(db.Model):
    __tablename__ = "tracks"
    id = db.Column(db.Integer, primary_key = True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"))
    name = db.Column(db.String(200))
    lyrics = db.Column(db.Text())
    artist = db.relationship("Artist", back_populates="tracks")
    
    
def save_track_to_db(artist_name, track_name, lyrics, db=db):
    with web.app.app_context():
        artist = db.session.scalar(db.select(Artist).filter(Artist.name == artist_name))
        print (f"Query result is {artist}")
        if not artist:
            print (f"Adding {artist_name}")
            artist = Artist(name = artist_name)
        track = Tracks(name = track_name, lyrics = lyrics, artist=artist)
        db.session.add_all([artist, track])
        db.session.commit()
