import sys
import re
from get_video_info import get_video_url,get_video_name
from download import download

args = sys.argv
url = sys.argv[1]
if (re.match("https://www.vlive.tv/post/.*",url) is None) and (re.match("https://www.vlive.tv/video/.*",url) is None):
    exit()
video_url = get_video_url(url)
video_name = get_video_name(url)
download(video_url,video_name)
