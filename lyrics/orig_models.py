from typing import List
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

class Artists(Base):
    __tablename__ = "artists"
    id: Mapped[int] = mapped_column(primary_key = True)
    name : Mapped[str] = mapped_column(String(100))

    songs: Mapped[List["Songs"]] = relationship(back_populates = "artist")

class Songs(Base):
    __tablename__ = "tracks"
    id: Mapped[int] = mapped_column(primary_key = True)
    artist_id: Mapped[int] = mapped_column(ForeignKey("artists.id"))
    name: Mapped[str] = mapped_column(String(200))
    lyrics: Mapped[str] = mapped_column(Text())

    artist:Mapped["Artists"] = relationship(back_populates="songs")
    