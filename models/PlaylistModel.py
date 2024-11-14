from config import db
from datetime import datetime


class Playlist(db.Model):
    __tablename__ = "playlists"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    playlist_songs = db.relationship("PlaylistSong", backref="playlist", lazy=True)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "created_at": self.created_at}