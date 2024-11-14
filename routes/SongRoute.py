from flask import Blueprint
from controllers.SongController import *


SongRoute = Blueprint("SongRoute", __name__)

SongRoute.route("/api/songs", methods=["POST"])(create_song)
SongRoute.route("/api/songs", methods=["GET"])(get_all_songs)
SongRoute.route("/api/songs/<song_id>", methods=["GET"])(get_song_by_id)
SongRoute.route("/api/songs/<song_id>", methods=["PUT"])(update_song_by_id)
SongRoute.route("/api/songs/<song_id>", methods=["DELETE"])(delete_song_by_id)
