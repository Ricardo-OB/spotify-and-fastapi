import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils.utilities import process_url_playlist, count_songs
import pathlib, os, shutil

def download_songs_from_url(url_playlist):
    parent_dir = pathlib.Path().resolve()

    try:
        os.remove('songs_not_downloaded.txt')
    except Exception as e:
        pass

    try:
        shutil.rmtree(os.path.join(parent_dir, 'songs'), ignore_errors=False)
    except Exception as e:
        pass

    path = os.path.join(parent_dir, 'songs')
    os.mkdir(path)

    with open('songs_not_downloaded.txt', 'w') as f:
        f.write('Canciones no descargadas:'+'\n')

    options = webdriver.ChromeOptions()
    #options.add_argument("--headless") # ocultar ventana
    p = {"download.default_directory": path+"\\"}
    options.add_experimental_option("prefs", p)

    url_webpage = 'https://www.soundloaders.com/spotify-downloader/'

    #url_playlist = 'https://open.spotify.com/playlist/2HXEldKjW91yxmljTqIBBp?si=cc5cfe233bf74867'
    songs = process_url_playlist(url_playlist)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    for keys, values in songs.items():

        files_count_pre = count_songs(path)

        try:
            url_song = values['url']
            
            driver.get(url_webpage)
            time.sleep(5)

            input = driver.find_element(By.CLASS_NAME, f'DownloaderTrackPage_Input__ZTfhW')
            input.send_keys(url_song)
            time.sleep(5)

            button_submit = driver.find_element(By.XPATH, f'//*[@id="__next"]/div/div/div[1]/div[1]/form/button')
            button_submit.click()
            time.sleep(5)

            button_download = driver.find_element(By.XPATH, f'//*[@id="__next"]/div/div/div[1]/div[1]/div[2]/button[1]')
            button_download.click()

            # Esperar hasta que se descargue la cancion o pasen 70 segundos
            files_count_post = count_songs(path)
            cont_time = 0
            while files_count_post == files_count_pre:
                time.sleep(1)
                cont_time += 1
                files_count_post = count_songs(path)
                if cont_time >= 70:
                    break

        except:
            pass

        # Cerrar primera ventana despues de tener X ventanas [abiertas]
        try:
            if int(keys) >= 6:
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(1.5)
                driver.close()
                driver.switch_to.window(driver.window_handles[-1])
                # driver.find_element(By.TAG_NAME, "body").send_keys(Keys.CONTROL + "w")
        except:
            pass

        # Abrir nueva ventana
        try:
            driver.execute_script("window.open('');")
            time.sleep(1.5)
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(1.5)
            driver.get(url_webpage)
        except:
            pass
        
        time.sleep(2)
        files_count_post = count_songs(path)

        try:
            if files_count_post == files_count_pre:
                file_txt = open('songs_not_downloaded.txt', 'a')
                file_txt.write(values['name']+'\n')
                file_txt.write(values['url']+'\n')
                file_txt.write('\n')
                file_txt.close()
        except:
            pass

    try:
        driver.quit()
    except:
        pass

    return {'Descarga Finalizada': f'El archivo "songs_not_downloaded.txt" contiene los nombres de las canciones que no fueron posible descargar. \n La carpeta "songs" contiene las canciones descargadas.'}
