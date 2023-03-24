from typing import Optional
from fastapi import FastAPI, HTTPException, Request, Response, Cookie, Form, status
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

import json
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from utils.utilities import process_url_playlist, create_spotify_oauth, get_token, send_songs
from utils.selenium_songs import download_songs_from_url
import spotipy

app = FastAPI(
    title='Spotify Music API'
)

# app.add_middleware(
#   CORSMiddleware,
#   allow_origins=['http://localhost:8000'],
#   allow_credentials=True,
#   allow_methods=["GET", "POST", "OPTIONS", "HEAD",], # include additional methods as per the application demand
#   allow_headers=["Content-Type","Set-Cookie"], # include additional headers as per the application demand
# )

# app.add_middleware(SessionMiddleware, secret_key="adsgfAFafdfs!22")

app.mount("/static", StaticFiles(directory="src/static"), name="static")

templates = Jinja2Templates(directory="src/templates")


class URL_Item(BaseModel):
    url: str


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("login.html", context={"request": request})


@app.get("/authSpotify")
async def preRedirectPage(request: Request):
    print("Entrando a preRedirectPage")
    sp_oauth = create_spotify_oauth(request)
    auth_url = sp_oauth.get_authorize_url()
    return RedirectResponse(auth_url)


@app.get("/redirect")
async def redirectPage(request: Request):
    print("Entrando a redirectPage")
    sp_oauth = create_spotify_oauth(request)
    code = request.query_params['code']
    code = sp_oauth.parse_response_code(code)
    token_info = sp_oauth.get_access_token(code)
    # print("------------token_info----------", token_info)
    response = RedirectResponse(request.url_for("homeMain"))
    response.set_cookie(key="access_token", value=token_info["access_token"], httponly=True)
    response.set_cookie(key="token_type", value=token_info["token_type"], httponly=True)
    response.set_cookie(key="expires_in", value=token_info["expires_in"], httponly=True)
    response.set_cookie(key="scope", value=token_info["scope"], httponly=True)
    response.set_cookie(key="expires_at", value=token_info["expires_at"], httponly=True)
    response.set_cookie(key="refresh_token", value=token_info["refresh_token"], httponly=True)
    return response


@app.get("/main-home")
async def homeMain(request: Request):
    try:
        token_info = get_token(request)
    except Exception as e:
        print("Not logged in")
        return RedirectResponse(request.url_for("home"))
    
    sp = spotipy.Spotify(auth=token_info["access_token"])
    user = sp.current_user()["display_name"]

    contexts = {"request": request, "user": user, "sp": sp}
    return templates.TemplateResponse("features.html", context=contexts)


@app.get("/manage-playlists")
async def managePlaylists(request: Request):
    try:
        token_info = get_token(request)
    except Exception as e:
        print("Not logged in")
        return RedirectResponse(request.url_for("home"))
    
    sp = spotipy.Spotify(auth=token_info["access_token"])
    id_urls = []
    playlists = sp.current_user_playlists()

    while playlists:
        for i, playlist in enumerate(playlists['items']):
            # print(f"{i + 1}. URL id: {playlist['id']}. Name: {playlist['name']}")
            id_urls.append(playlist["id"])
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None

    contexts = {"request": request, "id_urls": id_urls}
    return templates.TemplateResponse("manage_playlist.html", context=contexts)

@app.get("/main-transfer")
async def homeTransfer(request: Request):
    try:
        token_info = get_token(request)
    except Exception as e:
        print("Not logged in")
        return RedirectResponse(request.url_for("home"))
    
    sp = spotipy.Spotify(auth=token_info["access_token"])

    contexts = {"request": request, "sp": sp}
    return templates.TemplateResponse("home_transfer.html", context=contexts)


@app.post("/main-transfer")
async def homeTransfer(request: Request, exampleURL1: Optional[str] = Form(...), exampleURL2: Optional[str] = Form(...)):
    contexts = {"exampleURL1": exampleURL1, "exampleURL2": exampleURL2}
    html_frames = f"""
    <div>
    <p>Playlists seleccionadas:</p>
    <iframe style="margin-right: 1em; margin-left: 1em;"
            src="https://open.spotify.com/embed/playlist/{exampleURL1[34:56]}?utm_source=generator&theme=0"
            width="46%"
            height="352"
            frameBorder="0"
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
    </iframe>
    <iframe style="margin-right: 1em; margin-left: 1em;"
            src="https://open.spotify.com/embed/playlist/{exampleURL2[34:56]}?utm_source=generator&theme=0"
            width="46%"
            height="352"
            frameBorder="0"
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
    </iframe>
    <hr>
    <br>
    </div>
    """
    return HTMLResponse(content=html_frames, status_code=200)


@app.post("/transfer-songs")
async def transferSongs(request: Request, exampleURL1: Optional[str] = Form(...), exampleURL2: Optional[str] = Form(...)):
    try:
        token_info = get_token(request)
    except Exception as e:
        print("Not logged in")
        return RedirectResponse(request.url_for("home"))
    
    sp = spotipy.Spotify(auth=token_info["access_token"])
    songs_1, name_playlist_1 = process_url_playlist(exampleURL1, sp)
    songs_2, name_playlist_2 = process_url_playlist(exampleURL2, sp)

    contexts = {"request": request, "songs_1": songs_1, "songs_2": songs_2,
                "name_playlist_1": name_playlist_1, "name_playlist_2": name_playlist_2,
                "url_1": exampleURL1, "url_2": exampleURL2}

    return templates.TemplateResponse("transfer_song.html", context=contexts)


@app.post("/transfering-songs")
async def finalTransferSongs(request: Request, url_1: str = Form(...), url_2: str = Form(...)):

    try:
        token_info = get_token(request)
    except Exception as e:
        print("Not logged in")
        return RedirectResponse(request.url_for("home"))
    
    sp = spotipy.Spotify(auth=token_info["access_token"])
    cont_songs_add, cont_songs_not_add = send_songs(url_1, url_2, sp)

    contexts = {"request": request, "add": cont_songs_add, "not_add": cont_songs_not_add}
    return templates.TemplateResponse("transfer_done.html", context=contexts)


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
