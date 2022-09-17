import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json, os
from utils.credentials import cred

def process_url_playlist(url):
    
    auth_manager = SpotifyClientCredentials(
        client_id = cred['SPOTIPY_CLIENT_ID'],
        client_secret= cred['SPOTIPY_CLIENT_SECRET']
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)

    url_playlist = url
    results = sp.playlist(url_playlist)
    
    dict_songs = {str(key+1):{} for key in range(0,results['tracks']['total'])}
    dict_songs['Playlist Name'] = results['name']

    for index, item in enumerate(results['tracks']['items']):
        dict_songs[str(index+1)]['url'] = item['track']['external_urls']['spotify']
        dict_songs[str(index+1)]['name'] = item['track']['name']
        list_artists = []
        for sub_item in item['track']['artists']:
            list_artists.append(sub_item['name'])
        dict_songs[str(index+1)]['artist'] = list_artists
    
    return dict_songs

def count_songs(path):
    files_count = 0
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files_count += 1
    return files_count