from flask import jsonify, request
from config import db
from models.PlaylistSongModel import PlaylistSong
from models.SongModel import Song
from models.PlaylistModel import Playlist
from sqlalchemy import func
from datetime import timedelta


# Method POST - create playlist song /api/playlistsongs
def create_playlist_song():
    new_playlist_song_data = request.get_json()
    song_id = new_playlist_song_data.get("song_id")
    playlist_id = new_playlist_song_data.get("playlist_id")

    song = Song.query.get(song_id)
    playlist = Playlist.query.get(playlist_id)

    if not song and not playlist:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "ID Lagu dan ID Playlist tidak ditemukan",
                }
            ),
            404,
        )
    if not song:
        return jsonify({"status": "error", "message": "ID Lagu tidak ditemukan"}), 404
    if not playlist:
        return (
            jsonify({"status": "error", "message": "ID Playlist tidak ditemukan"}),
            404,
        )

    existing_entry = PlaylistSong.query.filter_by(
        song_id=song_id, playlist_id=playlist_id
    ).first()
    if existing_entry:
        return (
            jsonify(
                {"status": "error", "message": "Lagu ini sudah ada di dalam playlist"}
            ),
            409,
        )

    # Create new playlist song entry
    new_playlist_song = PlaylistSong(song_id=song_id, playlist_id=playlist_id)
    db.session.add(new_playlist_song)
    db.session.commit()

    return (
        jsonify(
            {
                "status": "success",
                "message": "Lagu berhasil ditambahkan ke playlist",
                "data": [
                    {
                        "id": new_playlist_song.id,
                        "song_id": new_playlist_song.song_id,
                        "playlist_id": new_playlist_song.playlist_id,
                        "playlist_name": playlist.name,
                        "song_name": song.title,
                    }
                ],
            }
        ),
        201,
    )


# Method GET - playlist songs /api/playlistsongs
def get_all_playlist_songs():
    playlist_songs = PlaylistSong.query.all()
    playlist_song_list = []
    
    for playlist_song in playlist_songs:
        playlist = Playlist.query.get(playlist_song.playlist_id)
        song = Song.query.get(playlist_song.song_id)
        
        playlist_song_list.append(
            {
                "id": playlist_song.id,
                "song_id": playlist_song.song_id,
                "playlist_id": playlist_song.playlist_id,
                "playlist_name": playlist.name if playlist else "Tidak ada playlist",
                "song_name": song.title if song else "Tidak ada lagu",
            }
        )
    
    return jsonify({"playlist_songs": playlist_song_list})



# Method PUT - update playlist song by id /api/playlistsongs/{playlist_song_id}
def update_playlist_song_by_id(playlist_song_id):
    playlist_song = PlaylistSong.query.get(playlist_song_id)

    if not playlist_song:
        return (
            jsonify({"status": "error", "message": "Playlist song tidak ditemukan"}),
            404,
        )

    playlist_song_data = request.get_json()
    song_id = playlist_song_data.get("song_id")
    playlist_id = playlist_song_data.get("playlist_id")

    song = Song.query.get(song_id)
    playlist = Playlist.query.get(playlist_id)

    if not song and not playlist:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "ID Lagu dan ID Playlist tidak ditemukan",
                }
            ),
            404,
        )
    if not song:
        return jsonify({"status": "error", "message": "ID Lagu tidak ditemukan"}), 404
    if not playlist:
        return (
            jsonify({"status": "error", "message": "ID Playlist tidak ditemukan"}),
            404,
        )

    existing_entry = PlaylistSong.query.filter_by(
        song_id=song_id, playlist_id=playlist_id
    ).first()
    if existing_entry and existing_entry.id != playlist_song_id:
        return (
            jsonify(
                {"status": "error", "message": "Lagu sudah ada di dalam playlist ini"}
            ),
            400,
        )

    playlist_song.song_id = song_id
    playlist_song.playlist_id = playlist_id
    db.session.commit()

    return (
        jsonify(
            {
                "status": "success",
                "message": f"Playlist song ID {playlist_song_id} berhasil diperbarui",
                "data": playlist_song.to_dict(),
            }
        ),
        200,
    )


# Method DELETE - delete playlist song by id /api/playlistsongs/{playlist_song_id}
def delete_playlist_song_by_id(playlist_song_id):
    playlist_song = PlaylistSong.query.get(playlist_song_id)
    if not playlist_song:
        return jsonify({"status": "error", "message": "Playlist song tidak ditemukan"}), 404
    db.session.delete(playlist_song)
    db.session.commit()
    return (
        jsonify(
            {
                "status": "success",
                "message": "Playlist song ID "
                + str(playlist_song_id)
                + " deleted successfully",
            }
        ),
        200,
    )
