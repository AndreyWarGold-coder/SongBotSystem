import dropboxFN
import SL_Settings
import os
from moviepy.editor import *
import random
import downloader
import Viewers

list_music = dropboxFN.dropbox_list_files("music")

def get_list_views_file():
    return SL_Settings.load_obj("list_view", "options")

def add_list_views_file(slowire):
    list_file = dropboxFN.dropbox_list_files("options")
    if("list_view.pickle" in list_file):
        tmp = get_list_views_file()
        for i in slowire:
            tmp[i] = slowire[i]
        SL_Settings.save_obj(tmp, "list_view", "options")
    else:
        SL_Settings.save_obj(slowire, "list_view", "options")

def update_list_views_file():
    tmp = {}
    for music in list_music:
        author = music.split("_")[0]
        name = music.split("_")[1]
        tmp[author+"_"+name] = Viewers.get_count_listen(author+"_"+name)
        print("GOOD UPDATE!", tmp[author+"_"+name])
    add_list_views_file(tmp)
    print("DONE")

def get_music_list_without_indexes(listM):
    tmp = []
    for i in listM:
        if(i.endswith("_0.mp3")):
            tmp.append(i.split("_0.mp3")[0])
    return tmp

def clear_mp3_ends(listM):
    tmp = []
    for i in listM:
        tmp.append(i.split(".mp3")[0])
    return tmp

def is_okay(category):
    tmp = SL_Settings.load_obj(category, "categorys")
    tmp = clear_mp3_ends(tmp)
    tmp2 = get_music_list_without_indexes(list_music)
    error = []
    for i in tmp:
        if i in tmp2:
            pass
        else:
            error.append(i)
    print("ERRORS ", error)
    return error


def is_okay_full(category):
    tmp = SL_Settings.load_obj(category, "categorys")
    tmp = clear_mp3_ends(tmp)
    list_music_tmp = clear_mp3_ends(list_music)
    error = []
    for i in tmp:
        for y in range(3):
            if (i+"_"+str(y)) in list_music_tmp:
                pass
            else:
                error.append(i+"_"+str(y))
    print("ERRORS ", error)
    return error


def split_music(music, index):
    name_file = music.split(".mp3")[0]
    save = open(name_file+"_"+str(index) + "_tmp.mp3", "wb")
    file = dropboxFN.dropbox_download_file("music/" + music, content=True)
    save.write(file)
    save.close()
    clip = AudioFileClip(name_file+"_"+str(index) + "_tmp.mp3")
    duration = round(clip.duration) - 1
    start_t = random.randint(0, duration - 10)
    end_t = start_t + 10
    withstart_clip = clip.cutout(end_t, clip.duration)
    end_clip = withstart_clip.cutout(0, start_t)
    end_clip.write_audiofile(name_file+"_"+str(index) + ".mp3")
    return name_file+"_"+str(index) + ".mp3"

def start_rewrite_files():
    a = 0
    for i in list_music:
        a+=1
        print(str(a)+" with " + str(len(list_music)))
        print(i+" will split")
        for t in range(3):
            print(str(t) + " frame split")
            name_frame = split_music(i, t)
            dropboxFN.dropbox_upload_file(open(name_frame, "rb").read(), name_frame, "music")
        os.remove(name_frame)
        dropboxFN.dropbox_delete_file("music/" + i)
        print(i+" done split")

def ckeck_random():
    error = []
    list_music_tmp = clear_mp3_ends(list_music)
    list_music_without = get_music_list_without_indexes(list_music)
    for i in list_music_without:
        for y in range(3):
            if(i+"_"+str(y)) in list_music_tmp:
                pass
            else:
                error.append(i+"_"+str(y))
    print(error)
    return error

def check_categorys_is_okey(isFull = False):
    list_files = dropboxFN.dropbox_list_files("categorys")
    list_error = []
    for i in list_files:
        tmp = []
        if isFull:
            tmp = is_okay_full(i.split(".")[0])
        else:
            tmp = is_okay(i.split(".")[0])
        list_error.append(tmp)


    print("Result check ", list_error)

def download_link(url, category):
    all_files = get_music_list_without_indexes(list_music)
    all_categorys = dropboxFN.dropbox_list_files("categorys") #with .pickle
    all_categorys_without_pickle = []
    for i in all_categorys:
        all_categorys_without_pickle.append(i.split(".")[0])
    category_list_music = []
    if(category in all_categorys_without_pickle):
        category_list_music = SL_Settings.load_obj(category, "categorys")


update_list_views_file()

downloader.start_download_thread("https://open.spotify.com/playlist/6hyQKlkQsGchQYEaLOVItN?si=f0398785e0084ba1", "VibeUkr", 65)
while(True):
    pass