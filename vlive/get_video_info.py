import urllib.request
from progress import progress
from get_json import get_json
from const import APP_ID,HEADER
import json

def get_video_seq(url):
    req = urllib.request.Request(url,headers=HEADER)
    with urllib.request.urlopen(req) as res:
        text = res.read().decode()
        length = len(text)
        index = text.find("window.__PRELOADED_STATE__")
        text_json = ""
        num_bracket_1 = 0
        num_bracket_2 = 0
        for i in range(index,length):
            if text[i] == "{":
                num_bracket_1 += 1
            if text[i] == "}":
                num_bracket_2 += 1
            if num_bracket_1 > 0:
                text_json += text[i]
            if (num_bracket_1 == num_bracket_2) and (num_bracket_1 != 0):
                break
        video_seq = json.loads(text_json)["postDetail"]["post"]["officialVideo"]["videoSeq"]
        return video_seq
def get_vod_id(url):
    req = urllib.request.Request(url,headers=HEADER)
    with urllib.request.urlopen(req) as res:
        text = res.read().decode()
        length = len(text)
        index = text.find("window.__PRELOADED_STATE__")
        text_json = ""
        num_bracket_1 = 0
        num_bracket_2 = 0
        for i in range(index,length):
            if text[i] == "{":
                num_bracket_1 += 1
            if text[i] == "}":
                num_bracket_2 += 1
            if num_bracket_1 > 0:
                text_json += text[i]
            if (num_bracket_1 == num_bracket_2) and (num_bracket_1 != 0):
                break
        vod_id = json.loads(text_json)["postDetail"]["post"]["officialVideo"]["vodId"]
        return vod_id
def get_key(url):
    video_seq = get_video_seq(url)
    get_key_api_url = "https://www.vlive.tv/globalv-web/vam-web/video/v1.0/vod/{}/inkey?appId={}".format(video_seq,APP_ID)
    key = get_json(get_key_api_url)["inkey"]
    return key
def get_video_url(url):
    key = get_key(url)
    vod_id = get_vod_id(url)
    get_video_api_url = "https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/{}?key={}".format(vod_id,key)
    video_url = get_json(get_video_api_url)["videos"]["list"][0]["source"]
    return video_url
def get_video_name(url):
    return "test.mp4"
    
