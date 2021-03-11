import urllib.request
from progress import progress

def download(video_url,video_name):
    print("download:{}.mp4".format(video_name))
    urllib.request.urlretrieve(video_url,"{}.mp4".format(video_name),progress)
