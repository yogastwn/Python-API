from flask import Blueprint
from controllers.PlaylistSongController import *


PlaylistSongRoute = Blueprint("PlaylistSongRoute", __name__)

PlaylistSongRoute.route("/api/playlistsongs", methods=["POST"])(create_playlist_song)
PlaylistSongRoute.route("/api/playlistsongs", methods=["GET"])(get_all_playlist_songs)
# PlaylistSongRoute.route("/api/playlistsongs/<playlist_song_id>", methods=["GET"])(get_playlist_song_by_id)
PlaylistSongRoute.route("/api/playlistsongs/<playlist_song_id>", methods=["PUT"])(update_playlist_song_by_id)
PlaylistSongRoute.route("/api/playlistsongs/<playlist_song_id>", methods=["DELETE"])(delete_playlist_song_by_id)