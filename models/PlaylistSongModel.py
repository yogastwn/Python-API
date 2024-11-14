from config import db

class PlaylistSong(db.Model):
    __tablename__ = "playlist_songs"
    id = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey("songs.id"), nullable=False)
    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"), nullable=False)

    def to_dict(self):
        return {"id": self.id, "song_id": self.song_id, "playlist_id": self.playlist_id}