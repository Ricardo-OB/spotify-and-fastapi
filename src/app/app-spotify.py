from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.utilities import process_url_playlist

app = FastAPI(
    title='Spotify Music API'
)

class URL_Item(BaseModel):
    url: str

@app.post('/', status_code=200)
async def download(request: URL_Item):
    songs = process_url_playlist(request.url)
    return songs