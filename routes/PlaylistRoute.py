from flask import Blueprint
from controllers.PlaylistController import *

PlaylistRoute = Blueprint("PlaylistRoute", __name__)

PlaylistRoute.route("/api/playlists", methods=["POST"])(create_playlist)
PlaylistRoute.route("/api/playlists", methods=["GET"])(get_all_playlists)
PlaylistRoute.route("/api/playlists/<playlist_id>", methods=["GET"])(get_playlist_by_id)
PlaylistRoute.route("/api/playlists/<playlist_id>", methods=["PUT"])(update_playlist_by_id)
PlaylistRoute.route("/api/playlists/<playlist_id>", methods=["DELETE"])(delete_playlist_by_id)
