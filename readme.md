# FastAPI y Spotify API

[<img src="https://geekflare.com/wp-content/uploads/2019/07/fast-api-logo.png" width="20%">](https://fastapi.tiangolo.com/)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/26/Spotify_logo_with_text.svg/1024px-Spotify_logo_with_text.svg.png" width="20%">](https://developer.spotify.com/documentation/web-api/)&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[<img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/Selenium_Logo.png" width="6%">](https://selenium-python.readthedocs.io/)

API para obtener los nombres, artistas y links de todas tus canciones de una Playlist de Spotify. Adicionalmente puedes descargar las canciones

## Pasos para ver las canciones de una Playlist

1. Clona o descarga el repositorio

2. Crea el entorno virtual

3. Instala los requerimientos: `pip install -r requirements.txt`

4. Dirigite a la pagina web para desarrolladores de Spotify ([API Spotify](https://developer.spotify.com/dashboard/login))

    4.1 Inicia sesión, luego crea una APP y copia las credenciales: `Client ID` y `Client Secret`

    4.2 Crea un archivo con el nombre `credentials.py` en la ruta src/utils/
    
    4.3 Pega las credenciales (en `credentials.py`) de tal modo que las contenga un diccionario `cred`, asi:

        cred = {'SPOTIPY_CLIENT_ID' : 'client id',
                'SPOTIPY_CLIENT_SECRET' : 'client secret'}

5. Ejecuta la API: `python .\src\main.py`

6. Abre tu explorador y abre este link: http://localhost:8000/docs (documentación automática de FastAPI)

7. En el endpoint `Show Songs` de tipo POST pega el link de tu Playlist: reemplaza el campo `"string"` de `{"url": "string"}` por el URL


## Pasos para descargar las canciones de una Playlist

*Nota 1: Las canciones se descargan empleando [Selenium](https://selenium-python.readthedocs.io/), Google Chrome y una pagina web externa ([Soundloaders](https://www.soundloaders.com/)).*

*Nota 2: Al descargar las canciones se abrirá una ventana de Google Chrome (no la cierres).*

*Nota 3: La API descarga una canción en aproximadamnete 1.3 minutos. La velocidad de descarga tambien depende de tu ancho de banda y del tiempo de respuesta de la pagina externa.*

1. Sigue los pasos 1 a 6 descritos anteriormente

2. En el endpoint `Download Songs` de tipo POST pega el link de tu Playlist: reemplaza el campo `"string"` de `{"url": "string"}` por el URL de tu playlist para descargar todas las canciones

3. En la ruta del repositorio se creará una carpeta (`songs`) y un archivo de texto (`songs_not_downloaded.txt`).

    - La carpeta contiene todas tus canciones

    - El archivo de texto contiene una lista de canciones que no fueron descargadas

    3.1 Debes copiar/cortar todas tus canciones fuera del directorio actual, de lo contrario cuando ejecutes otra descarga (desde la API) se borrará la carpeta y el archivo de texto.
