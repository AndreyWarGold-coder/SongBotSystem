import spotipy
from spotipy.oauth2 import SpotifyOAuth
import youtube_dl
from youtubesearchpython import VideosSearch
import pickle
import random
import os
import shutil
from threading import Thread
from moviepy.editor import *

import SL_Settings
import dropboxFN

def split_music(music, index):
    name_file = music.split(".mp3")[0]
    clip = AudioFileClip(name_file+".mp3")
    duration = round(clip.duration) - 1
    start_t = random.randint(0, duration - 10)
    end_t = start_t + 10
    withstart_clip = clip.cutout(end_t, clip.duration)
    end_clip = withstart_clip.cutout(0, start_t)
    end_clip.write_audiofile(name_file+"_"+str(index) + ".mp3")
    return name_file+"_"+str(index) + ".mp3"

def get_music_list_without_indexes(listM):
    tmp = []
    for i in listM:
        if(i.endswith("_0.mp3")):
            tmp.append(i.split("_0.mp3")[0])
    return tmp

def search(name_music):
    videosSearch = VideosSearch(name_music, limit = 1)
    videoresult = videosSearch.result()["result"][0]["link"]
    return videoresult

def download(videoresult, name_music):
    ydl_opts = {'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192', }],
                'outtmpl': f'./{name_music}.webm'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([videoresult])



def add_to_category(category, nameMusic):
    if((category+".pickle") in dropboxFN.dropbox_list_files("categorys")):
        tmp = SL_Settings.load_obj(category, "categorys")
        tmp.append(nameMusic)
        SL_Settings.save_obj(tmp, category, "categorys")
    else:
        tmp = [nameMusic]
        SL_Settings.save_obj(tmp, category, "categorys")

Thread_work = False
def start_download_thread(url, name_categoty, colvo=20):
    global Thread_work
    if(Thread_work):
        return "no"
    else:
        Thread_work=True
        th1 = Thread(target=start_downloading_from_spotify_playlist, args=[url, name_categoty, colvo])
        th1.start()
        return "yes"

def start_downloading_from_spotify_playlist(url, name_category, colvo=20, isFullCheck = False):
    global Thread_work
    list_music = {}
    url_re = url.split("/")[-1]
    url_re = url_re.split("?")[0]


    client_id = "aa4d49d1ffbf4e6b83db0fd175226929"
    client_secret = "9ccf181877244e9699e64bd9a39cce7f"
    redirect_url = "https://localhost:8888/collback"

    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret,
                                                   redirect_uri=redirect_url))
    results = sp.playlist(url_re)
    results = results["tracks"]
    list_have_music = get_music_list_without_indexes(dropboxFN.dropbox_list_files("music"))
    for idx, item in enumerate(results['items']):
        if (idx <= colvo):
            try:
                track = item['track']
                print(track)
                name_music = track['artists'][0]['name'] + "_" + track['name']
                print(idx, " - ", name_music)
                if not ((name_music) in list_have_music):
                    download(search(name_music), name_music)
                    dropboxFN.dropbox_upload_file(open(split_music(name_music+ ".mp3", 0), "rb").read(), name_music + ".mp3", "music")
                    dropboxFN.dropbox_upload_file(open(split_music(name_music + ".mp3", 1), "rb").read(),
                                                  name_music + ".mp3", "music")
                    dropboxFN.dropbox_upload_file(open(split_music(name_music + ".mp3", 2), "rb").read(),
                                                  name_music + ".mp3", "music")
                    os.remove(name_music + ".mp3")
                    print("Move good!")
                add_to_category(name_category, name_music + ".mp3")

            except Exception as ex:
                print("error: " +str(ex))
            finally:
                print("good")
    Thread_work=False