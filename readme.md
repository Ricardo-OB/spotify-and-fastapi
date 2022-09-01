# FastAPI y Spotify API

[![FastAPI](https://geekflare.com/wp-content/uploads/2019/07/fast-api-logo.png =210x80)](https://fastapi.tiangolo.com/)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[![Spotify](https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Spotify_logo_with_text.svg/1024px-Spotify_logo_with_text.svg.png =210x80)](https://developer.spotify.com/documentation/web-api/)

API para obtener los nombres, artistas y links de todas tus canciones de una Playlist de Spotify.

## Pasos

1. Clona o descarga el repositorio

2. Crea el entorno virtual

3. Instala los requerimientos: `pip install -r requirements.txt`

4. Dirigite a la pagina web para desarrolladores de Spotify ([API Spotify](https://developer.spotify.com/dashboard/login))

    4.1 Inicia sesión, crea una APP y copia las credenciales: `Client ID` y `Client Secret`
    4.2 Pega las credenciales en el archivo `utilities.py` que se encuentra en `/src/utils/`

5. Ejecuta la API: `python .\src\main.py`

6. Abre tu explorador y abre este link: http://localhost:8000/docs (documentación automática de FastAPI)

7. Pega el link de tu Playlist en el campo `"string"` de `{"url": "string"}`, que se encuentra en la ruta `defaul -> Get Songs`

## Proximamente...

Descargar todas las canciones de la Playlist con los links que retorna la API.
