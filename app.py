from config import app, db
from routes.PlaylistRoute import PlaylistRoute
from routes.SongRoute import SongRoute
from routes.PlaylistSongRoute import PlaylistSongRoute
from flask import jsonify

app.register_blueprint(PlaylistRoute)
app.register_blueprint(SongRoute)
app.register_blueprint(PlaylistSongRoute)


@app.route("/")
def index():
    api_list = {
        "Playlist APIs": {
            "1. Method POST - Membuat Playlist": "/api/playlists",
            "2. Method GET - Mengambil semua Playlist": "/api/playlists",
            "3. Method GET - Mengambil Playlist berdasarkan ID": "/api/playlists/<id>",
            "4. Method PUT - Memperbarui Playlist berdasarkan ID": "/api/playlists/<id>",
            "5. Method DELETE - Menghapus Playlist berdasarkan ID": "/api/playlists/<id>",
        },
        "Song APIs": {
            "1. Method POST - Membuat Song": "/api/songs",
            "2. Method GET - Mengambil semua Song": "/api/songs",
            "3. Method GET - Mengambil Song berdasarkan ID": "/api/songs/<id>",
            "4. Method PUT - Memperbarui Song berdasarkan ID": "/api/songs/<id>",
            "5. Method DELETE - Menghapus Song berdasarkan ID": "/api/songs/<id>",
        },
        "PlaylistSong APIs": {
            "1. Method POST - Menambahkan Lagu ke Playlist": "/api/playlistsongs",
            "2. Method GET - Mengambil semua PlaylistSong": "/api/playlistsongs",
            "3. Method PUT - Memperbarui PlaylistSong berdasarkan ID": "/api/playlistsongs/<id>",
            "4. Method DELETE - Menghapus PlaylistSong berdasarkan ID": "/api/playlistsongs/<id>",
        },
    }
    return jsonify(api_list)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=5004, debug=True)
