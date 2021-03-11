import urllib.request
import const
import json

def get_json(url):
    req = urllib.request.Request(url,headers = const.HEADER)
    with urllib.request.urlopen(req) as res:
        res_json = json.loads(res.read())
    return res_json
