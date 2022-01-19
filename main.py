import json
from flask import Flask, request, redirect, g, render_template
import requests
from urllib.parse import quote
from Song import Song

# Authentication Steps, paramaters, and responses are defined at https://developer.spotify.com/web-api/authorization-guide/
# Visit this url to see all the steps, parameters, and expected response.
#this is a test

app = Flask(__name__)

#  Client Keys
CLIENT_ID = "95c267e06f9a427ab4378fd3dba8d6cb"
CLIENT_SECRET = "a535b18e2c9f44aa82eee80ab5d59cca"

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# Server-side Parameters
#CLIENT_SIDE_URL = "http://172.30.202.10"
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 8080
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private user-read-recently-played user-read-playback-state user-modify-playback-state"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}



@app.route("/")
def index():
    # Auth Step 1: Authorization
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)


@app.route("/callback/q")
def callback():
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),

        "redirect_uri": REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    }
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]



    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    song = Song("The Steps HAIM", authorization_header)
    print(song.request["tracks"]["items"][0]["external_urls"]["spotify"])

    songList = ["Swimming in the Moonlight Bad Suns", "Outright Wild Party", "Hyperfine G Flip", "dfjksdlfhjkanv", "Harvard Laundry Day"]
    
    display_arr = []
    initIndex = 0
    indexList = []

    queuedLink = []
    queuedSongs = []
    queuedArtists = []
    queuedImage = []






    for track in songList:
        song = Song(track,authorization_header)
        if song.found == True:
            artist = song.request["tracks"]["items"][0]["artists"][0]["name"]
            trackTitle = song.request["tracks"]["items"][0]["name"]
            image = song.request["tracks"]["items"][0]["album"]["images"][1]["url"]
            link = song.request["tracks"]["items"][0]["external_urls"]["spotify"]

            songMeta = f"Queued {trackTitle} by {artist}"
            indexList.append(initIndex)
            initIndex += 1
            queuedSongs.append(trackTitle)
            queuedArtists.append(artist)
            queuedImage.append(image)
            queuedLink.append(link)
            print("The tempo is " + str(song.getAudioFeature("tempo")))
            #song.add_queue()

        else:
            failedQuery = song.request["Not Found"]
            msg = f"Song not found. Could not queue: {failedQuery}"
            display_arr.append(msg)



    return render_template("index.html", queuedLink = queuedLink, indexList = indexList, queuedSongs = queuedSongs, queuedArtists = queuedArtists, queuedImage = queuedImage)


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
