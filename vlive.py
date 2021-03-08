import urllib.request
import urllib.parse
import subprocess
import os
import json
import re

def progress(block_count, block_size, total_size):
  ratio = block_count * block_size / total_size
  if ratio > 1.0:
    percentage = 1.0
  max_bar = 50
  bar_num = int(ratio*max_bar)
  progress_element = '▮' * bar_num
  bar_fill = ' '
  bar = progress_element.ljust(max_bar, bar_fill)
  total_size_mb = total_size / 1024 /1024
  print(f'[{bar}] {ratio*100:.2f}% ( {total_size_mb:.0f}MB )\r',end='')

def get_video_key(seq):
    url = "https://www.vlive.tv/globalv-web/vam-web/video/v1.0/vod/{}/inkey?appId=8c6cc7b45d2568fb668be6e05b6e5a3b".format(seq)
    req = urllib.request.Request(url,headers = {"referer": "https://www.vlive.tv/","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"})
    with urllib.request.urlopen(req) as res:
        key = json.loads(res.read())["inkey"]
    return key

def get_video_url(vod_id,key):
    url = "https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/{}?key={}".format(vod_id,key)
    req = urllib.request.Request(url,headers = {"referer": "https://www.vlive.tv/","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"})
    with urllib.request.urlopen(req) as res:
        res_json = json.loads(res.read())
        video_url = res_json["videos"]["list"][0]["source"]
    return video_url

def get_video(url,save_name):
    """
    req = urllib.request.Request(url,headers = {"referer": "https://www.vlive.tv/","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"})
    with urllib.request.urlopen(req) as res:
        with open("{}.mp4".format(save_name), mode="wb") as f:
                f.write(res.read())
    """
    print("download:{}.mp4".format(save_name))
    urllib.request.urlretrieve(url,"{}.mp4".format(save_name),progress)

def download(video_post):
    for i in range(len(video_post["data"])):
        video_seq = video_post["data"][i]["officialVideo"]["videoSeq"]
        if os.path.exists(f"{video_seq}.mp4"):
            continue
        vod_id = video_post["data"][i]["officialVideo"]["vodId"]
        thumb_url = video_post["data"][i]["officialVideo"]["thumb"]
        save_name = str(video_seq)
        title = video_post["data"][i]["title"]
        key = get_video_key(video_seq)
        video_url = get_video_url(vod_id,key)
        get_video(video_url,save_name)

board_id = input("input url").split("/")[-1]
if not os.path.exists(board_id):
    os.mkdir(board_id)
os.chdir(board_id)

url = "https://www.vlive.tv/globalv-web/vam-web/post/v1.0/board-{}/videoPosts?appId=8c6cc7b45d2568fb668be6e05b6e5a3b&fields=officialVideo,url,title&locale=ko_KR&sortType=LATEST&limit=100".format(board_id)
req = urllib.request.Request(url,headers = {"referer": "https://www.vlive.tv/","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"})
with urllib.request.urlopen(req) as res:
    video_post = json.loads(res.read())

download(video_post)

while True:
    try:
        after = video_post["paging"]["nextParams"]["after"]
    except KeyError:
        break
    url = "https://www.vlive.tv/globalv-web/vam-web/post/v1.0/board-{}/videoPosts?appId=8c6cc7b45d2568fb668be6e05b6e5a3b&fields=officialVideo,url,title&locale=ko_KR&sortType=LATEST&limit=100&after={}".format(board_id,after)
    req = urllib.request.Request(url,headers = {"referer": "https://www.vlive.tv/","user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36"})
    with urllib.request.urlopen(req) as res:
        video_post = json.loads(res.read())
    download(video_post)
