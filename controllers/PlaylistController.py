from flask import jsonify, request
from config import db
from models.PlaylistModel import Playlist
from models.SongModel import Song
from models.PlaylistSongModel import PlaylistSong
from sqlalchemy import func
from datetime import timedelta

# Method POST - create playlist /api/playlists
def create_playlist():
    new_playlist_data = request.get_json()
    new_playlist = Playlist(name=new_playlist_data["name"])
    db.session.add(new_playlist)
    db.session.commit()
    return (
        jsonify(
            {
                "status": "success",
                "message": "Playlist created successfully",
                "data": new_playlist.to_dict(),
            }
        ),
        201,
    )


# Method GET - all playlists /api/playlists
def get_all_playlists():
    playlists = Playlist.query.all()
    playlist_with_songs = []

    for playlist in playlists:
        playlist_songs = PlaylistSong.query.filter_by(playlist_id=playlist.id).all()
        songs = [Song.query.get(playlist_song.song_id) for playlist_song in playlist_songs]
        
        total_songs = len(songs)
        total_duration_seconds = sum(song.duration for song in songs if song)
        total_duration = str(timedelta(seconds=total_duration_seconds))

        playlist_with_song = {
            "id": playlist.id,
            "name": playlist.name,
            "created_at": playlist.created_at,
            "total_songs": total_songs if total_songs else "Tidak ada lagu di playlist ini",
            "total_duration": total_duration,
            # "songs": [song.to_dict() for song in songs if song is not None],  # Add song only if it's found
        }

        playlist_with_songs.append(playlist_with_song)

    return jsonify({"playlists": playlist_with_songs})


# Method GET - playlist by id /api/playlists/{playlist_id}
def get_playlist_by_id(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({"status": "error", "message": "Playlist not found"}), 404

    playlist_songs = PlaylistSong.query.filter_by(playlist_id=playlist_id).all()
    songs = [Song.query.get(playlist_song.song_id) for playlist_song in playlist_songs]

    total_songs = len(songs)
    total_duration_seconds = sum(song.duration for song in songs if song)
    total_duration = str(timedelta(seconds=total_duration_seconds))

    playlist_with_song = {
        "id": playlist.id,
        "name": playlist.name,
        "created_at": playlist.created_at,
        "total_songs": total_songs if total_songs else "Tidak ada lagu di playlist ini",
        "total_duration": total_duration,
        "songs": [song.to_dict() for song in songs if song is not None],
    }

    return jsonify({"playlist": playlist_with_song})


# Method PUT - update playlist by id /api/playlists/{playlist_id}
def update_playlist_by_id(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({"status": "error", "message": "Playlist not found"}), 404

    playlist_data = request.get_json()
    playlist.name = playlist_data["name"]
    db.session.commit()
    return (
        jsonify(
            {
                "status": "success",
                "message": "Playlist updated successfully",
                "data": playlist.to_dict(),
            }
        ),
        200,
    )


# Method DELETE - delete playlist by id /api/playlists/{playlist_id}
def delete_playlist_by_id(playlist_id):
    playlist = Playlist.query.get(playlist_id)
    if not playlist:
        return jsonify({"status": "error", "message": "Playlist tidak ditemukan"}), 404

    # Check if there are songs associated with this playlist
    if PlaylistSong.query.filter_by(playlist_id=playlist_id).first():
        return jsonify(
            {
                "status": "error",
                "message": "Playlist tidak dapat dihapus karena masih memiliki lagu.",
            }
        ), 409

    # Delete the playlist if no songs are associated
    db.session.delete(playlist)
    db.session.commit()
    return jsonify(
        {
            "status": "success",
            "message": f"Playlist ID {playlist_id} berhasil dihapus.",
        }
    )
