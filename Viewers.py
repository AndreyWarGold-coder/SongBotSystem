from youtubesearchpython import VideosSearch

def get_count_listen(name_music):
    videosSearch = VideosSearch(name_music, limit=1)
    count = videosSearch.result()["result"][0]["viewCount"]['text'].split(" views")[0]
    tmp = count.split(",")
    ineger = ""
    for i in tmp:
        ineger += i
    count = int(ineger)
    print(count)
    return count
