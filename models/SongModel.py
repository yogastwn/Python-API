from config import db


class Song(db.Model):
    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    artist = db.Column(db.String(80), nullable=False)
    album = db.Column(db.String(80), nullable=False)
    duration = db.Column(db.Integer, nullable=False)

    playlist_songs = db.relationship("PlaylistSong", backref="song", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        # Convert seconds to minutes:seconds format
        minutes = self.duration // 60
        seconds = self.duration % 60
        formatted_duration = f"{minutes}:{seconds:02d}"
        
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "duration": formatted_duration,
        }
