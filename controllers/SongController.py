from flask import jsonify, request
from config import db
from models.SongModel import Song


# Method POST - create song /api/songs
def create_song():
    new_song_data = request.get_json()
    new_song = Song(
        title=new_song_data["title"],
        artist=new_song_data["artist"],
        album=new_song_data["album"],
        duration=new_song_data["duration"],
    )
    db.session.add(new_song)
    db.session.commit()
    return (
        jsonify(
            {
                "status": "success",
                "message": "Song created successfully",
                "data": new_song.to_dict(),
            }
        ),
        201,
    )


# Method GET - all songs /api/songs
def get_all_songs():
    songs = Song.query.all()
    song_list = [song.to_dict() for song in songs]
    return jsonify({"songs": song_list})


# Method GET - song by id /api/songs/{song_id}
def get_song_by_id(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({"status": "error", "message": "Song not found"}), 404

    return jsonify({"song": song.to_dict()})


# Method PUT - update song by id /api/songs/{song_id}
def update_song_by_id(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({"status": "error", "message": "Song not found"}), 404

    song_data = request.get_json()
    song.title = song_data["title"]
    song.artist = song_data["artist"]
    song.album = song_data["album"]
    song.duration = song_data["duration"]
    db.session.commit()
    return (
        jsonify(
            {
                "status": "success",
                "message": "Song updated successfully",
                "data": song.to_dict(),
            }
        ),
        200,
    )


# Method DELETE - delete song by id /api/songs/{song_id}
def delete_song_by_id(song_id):
    song = Song.query.get(song_id)
    if not song:
        return jsonify({"status": "error", "message": "Song not found"}), 404

    db.session.delete(song)
    db.session.commit()
    return jsonify(
        {
            "status": "success",
            "message": "Song ID " + str(song_id) + " deleted successfully",
        }
    )
