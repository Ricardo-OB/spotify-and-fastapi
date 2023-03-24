import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import json, os
from utils.credentials import cred
import time

def create_spotify_oauth(request):
    scopes = "user-follow-read,playlist-modify-private,playlist-modify-public,playlist-read-private,user-library-modify,user-library-read"
    spOAuth = SpotifyOAuth(
            client_id = cred['SPOTIPY_CLIENT_ID'],
            client_secret = cred['SPOTIPY_CLIENT_SECRET'],
            redirect_uri = request.url_for("redirectPage"),
            scope = scopes)
    return spOAuth


def get_token(request):

    if not request.cookies.get("access_token"):
        raise "Exception"

    token_info = {"access_token": request.cookies.get("access_token"),
                  "token_type": request.cookies.get("token_type"),
                  "expires_in": request.cookies.get("expires_in"),
                  "scope": request.cookies.get("scope"),
                  "expires_at": request.cookies.get("expires_at"),
                  "refresh_token": request.cookies.get("refresh_token"),}
    
    # Token is expired?
    now = int(time.time())
    is_expired = (float(token_info["expires_at"]) - now) < 60
    if is_expired:
        sp_oauth = create_spotify_oauth(request)
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    
    return token_info


def process_url_playlist(url, sp):
    # auth_manager = SpotifyClientCredentials(client_id = cred['SPOTIPY_CLIENT_ID'], client_secret= cred['SPOTIPY_CLIENT_SECRET'])
    # sp = spotipy.Spotify(auth_manager=auth_manager)

    results = sp.playlist_tracks(url)
    result = sp.user_playlist(user=None, playlist_id=url, fields="name")
    name_playlist = result['name']
    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    results_2 = tracks
    dict_songs = {str(key+1):{} for key in range(0,len(results_2))}

    for index in range(len(results_2)):
        dict_songs[str(index+1)]['url'] = results_2[index]['track']['external_urls']['spotify']
        dict_songs[str(index+1)]['uri'] = results_2[index]['track']['uri']
        dict_songs[str(index+1)]['name'] = results_2[index]['track']['name']
        list_artists = []
        for sub_item in results_2[index]['track']['artists']:
            list_artists.append(sub_item['name'])
        dict_songs[str(index+1)]['artist'] = list_artists

    return dict_songs, name_playlist


def send_songs(url_origen, url_destino, sp):
    dict_songs_origen, _ = process_url_playlist(url_origen, sp)
    dict_songs_destino, _ = process_url_playlist(url_destino, sp)

    list_songs_origen = [items['uri'] for index, items in dict_songs_origen.items()]
    list_songs_destino = [items['uri'] for index, items in dict_songs_destino.items()]
    songs_origen_final = []

    cont_songs_add = 0
    cont_songs_not_add = 0

    for song_d in list_songs_origen:
        if song_d not in list_songs_destino:
            songs_origen_final.append(song_d)
            cont_songs_add += 1
        else:
            cont_songs_not_add += 1

    quantity_songs = len(songs_origen_final)

    if (quantity_songs >= 1 and quantity_songs <=100):
        sp.playlist_add_items(url_destino, songs_origen_final)
    elif quantity_songs <=200:
        sp.playlist_add_items(url_destino, songs_origen_final[:100])
        sp.playlist_add_items(url_destino, songs_origen_final[100:])
    elif quantity_songs <=300:
        sp.playlist_add_items(url_destino, songs_origen_final[:100])
        sp.playlist_add_items(url_destino, songs_origen_final[100:200])
        sp.playlist_add_items(url_destino, songs_origen_final[200:])
    elif quantity_songs <=400:
        sp.playlist_add_items(url_destino, songs_origen_final[:100])
        sp.playlist_add_items(url_destino, songs_origen_final[100:200])
        sp.playlist_add_items(url_destino, songs_origen_final[200:300])
        sp.playlist_add_items(url_destino, songs_origen_final[300:])
    elif quantity_songs <=500:
        sp.playlist_add_items(url_destino, songs_origen_final[:100])
        sp.playlist_add_items(url_destino, songs_origen_final[100:200])
        sp.playlist_add_items(url_destino, songs_origen_final[200:300])
        sp.playlist_add_items(url_destino, songs_origen_final[300:400])
        sp.playlist_add_items(url_destino, songs_origen_final[400:])
    elif quantity_songs <=600:
        sp.playlist_add_items(url_destino, songs_origen_final[:100])
        sp.playlist_add_items(url_destino, songs_origen_final[100:200])
        sp.playlist_add_items(url_destino, songs_origen_final[200:300])
        sp.playlist_add_items(url_destino, songs_origen_final[300:400])
        sp.playlist_add_items(url_destino, songs_origen_final[400:500])
        sp.playlist_add_items(url_destino, songs_origen_final[500:])
    elif quantity_songs <=700:
        sp.playlist_add_items(url_destino, songs_origen_final[:100])
        sp.playlist_add_items(url_destino, songs_origen_final[100:200])
        sp.playlist_add_items(url_destino, songs_origen_final[200:300])
        sp.playlist_add_items(url_destino, songs_origen_final[300:400])
        sp.playlist_add_items(url_destino, songs_origen_final[400:500])
        sp.playlist_add_items(url_destino, songs_origen_final[500:600])
        sp.playlist_add_items(url_destino, songs_origen_final[600:])
    elif quantity_songs <=800:
        sp.playlist_add_items(url_destino, songs_origen_final[:100])
        sp.playlist_add_items(url_destino, songs_origen_final[100:200])
        sp.playlist_add_items(url_destino, songs_origen_final[200:300])
        sp.playlist_add_items(url_destino, songs_origen_final[300:400])
        sp.playlist_add_items(url_destino, songs_origen_final[400:500])
        sp.playlist_add_items(url_destino, songs_origen_final[500:600])
        sp.playlist_add_items(url_destino, songs_origen_final[600:700])
        sp.playlist_add_items(url_destino, songs_origen_final[700:])
    elif quantity_songs <=900:
        sp.playlist_add_items(url_destino, songs_origen_final[:100])
        sp.playlist_add_items(url_destino, songs_origen_final[100:200])
        sp.playlist_add_items(url_destino, songs_origen_final[200:300])
        sp.playlist_add_items(url_destino, songs_origen_final[300:400])
        sp.playlist_add_items(url_destino, songs_origen_final[400:500])
        sp.playlist_add_items(url_destino, songs_origen_final[500:600])
        sp.playlist_add_items(url_destino, songs_origen_final[600:700])
        sp.playlist_add_items(url_destino, songs_origen_final[700:800])
        sp.playlist_add_items(url_destino, songs_origen_final[800:])
    elif quantity_songs <=1000:
        sp.playlist_add_items(url_destino, songs_origen_final[:100])
        sp.playlist_add_items(url_destino, songs_origen_final[100:200])
        sp.playlist_add_items(url_destino, songs_origen_final[200:300])
        sp.playlist_add_items(url_destino, songs_origen_final[300:400])
        sp.playlist_add_items(url_destino, songs_origen_final[400:500])
        sp.playlist_add_items(url_destino, songs_origen_final[500:600])
        sp.playlist_add_items(url_destino, songs_origen_final[600:700])
        sp.playlist_add_items(url_destino, songs_origen_final[700:800])
        sp.playlist_add_items(url_destino, songs_origen_final[800:900])
        sp.playlist_add_items(url_destino, songs_origen_final[900:])

    return cont_songs_add, cont_songs_not_add


def count_songs(path):
    files_count = 0
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files_count += 1
    return files_count