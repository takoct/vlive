import urllib.request
from const import HEADER
import json

def get_json(url):
    req = urllib.request.Request(url,headers = HEADER)
    with urllib.request.urlopen(req) as res:
        res_json = json.loads(res.read())
    return res_json
def get_json_from_vlive_html(req):
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
    return text_json
