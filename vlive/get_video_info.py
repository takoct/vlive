import urllib.request
from progress import progress
from get_json import get_json,get_json_from_vlive_html
from const import APP_ID,HEADER
import json

def get_video_seq(url):
    req = urllib.request.Request(url,headers=HEADER)
    text_json = get_json_from_vlive_html(req)
    video_seq = json.loads(text_json)["postDetail"]["post"]["officialVideo"]["videoSeq"]
    return video_seq
def get_vod_id(url):
    req = urllib.request.Request(url,headers=HEADER)
    text_json = get_json_from_vlive_html(req)
    vod_id = json.loads(text_json)["postDetail"]["post"]["officialVideo"]["vodId"]
    return vod_id
def get_key(url):
    video_seq = get_video_seq(url)
    get_key_api_url = "https://www.vlive.tv/globalv-web/vam-web/video/v1.0/vod/{}/inkey?appId={}&platformType=PC".format(video_seq,APP_ID)
    key = get_json(get_key_api_url)["inkey"]
    return key
def get_video_url(url):
    key = get_key(url)
    vod_id = get_vod_id(url)
    get_video_api_url = "https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/{}?key={}".format(vod_id,key)
    video_url = get_json(get_video_api_url)["videos"]["list"][0]["source"]
    return video_url
def get_video_name(url):
    req = urllib.request.Request(url,headers=HEADER)
    text_json = get_json_from_vlive_html(req)
    video_name = json.loads(text_json)["postDetail"]["post"]["officialVideo"]["title"]
    return video_name 
