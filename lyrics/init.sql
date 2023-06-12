DROP TABLE if exists artist_tags CASCADE;
DROP TABLE if exists tracks CASCADE;
DROP TABLE if exists artists CASCADE;
DROP TABLE if exists tags CASCADE;


CREATE TABLE artists (
       id SERIAL,
       name VARCHAR(100),
       PRIMARY KEY (id)
);

CREATE TABLE tracks (
       id SERIAL,
       artist_id INTEGER REFERENCES artists(id),
       name VARCHAR(200),
       lyrics TEXT,
       PRIMARY KEY (id)
       );

CREATE TABLE tags (
       id SERIAL,
       name VARCHAR(20),
       PRIMARY KEY(id)
       );

CREATE TABLE artist_tags (
       artist INTEGER REFERENCES artists(id),
       tag INTEGER REFERENCES tags(id)
       );