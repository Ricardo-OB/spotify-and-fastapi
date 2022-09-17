from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.utilities import process_url_playlist
from utils.selenium_songs import download_songs_from_url

app = FastAPI(
    title='Spotify Music API'
)

class URL_Item(BaseModel):
    url: str

@app.post('/show', status_code=200)
async def show_songs(request: URL_Item):
    try:
        songs = process_url_playlist(request.url)
        return songs
    except Exception as e:
        print('No fue posible obtener la URL de la PLaylist.')
        print(e)

@app.post('/download', status_code=200)
async def download_songs(request: URL_Item):
    try:
        resp = download_songs_from_url(request.url)
        return resp
    except Exception as e:
        print('No fue posible descargar las canciones')
        print(e)
