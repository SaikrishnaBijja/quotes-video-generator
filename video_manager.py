import moviepy.editor as mp
from moviepy.editor import  ImageClip,  CompositeVideoClip
from email import header
import requests
from add_used_link import is_exist
import urllib.request
from PIL import Image
import math, time, random

PIXEL_API='563492ad6f9170000100000195141cd33b264b29b96c5c5ba01a5865'
PIXEL_ENDPOINT='https://api.pexels.com/videos/search'

sad=['nightsky', 'night', 'nightcity', 'stars', 'fog', 'dark', 'alone', 'dark clouds', 'sunset', 'astronomy']
motiv=['nature', 'forest', 'cities', 'lamp', 'mountains', 'fog', 'clouds', 'time lapse','motivation' ,'running', 'cycling', 'bicycle', 'watch', 'sunset']

header={
    'Authorization': PIXEL_API
}

def get_video_link(num, filepath, file):
    if num==1:
        to_search=motiv
    else:
        to_search=sad
    search={
        'query':random.choice(to_search),
        'orientation':'portrait',
        'per_page':'80',
    }
    res=requests.get(PIXEL_ENDPOINT, params=search, headers=header)
    for x in res.json()['videos']:
        if x['duration'] >= 15 and x['duration'] <= 20:
            for y in x['video_files']:
                if y['width'] == 1080 and  y['height'] == 1920:
                    if is_exist(y['link'], filepath):
                        try:
                            download_video(y['link'], file)
                        except TypeError:
                            get_video_link(num, filepath, file)
                        else:
                            return y['link']


def download_video(url_link, file_path):
    urllib.request.urlretrieve(url_link, file_path)
        

def make_final_video(video_path, audio_path, result, image_path):
    image_size_changer(image_path)
    audio = mp.AudioFileClip(audio_path)
    video1 = mp.VideoFileClip(video_path)

    newclip = video1.set_audio(audio)
    title = ImageClip(image_path).set_start(0).set_duration(video1.duration).set_pos(("center","center")).set_opacity(.79)

    final = CompositeVideoClip([newclip, title])
    final.subclip(0, video1.duration).write_videofile(result,
                     threads='12', bitrate='8000k',
                     ffmpeg_params=[
                         '-tile-columns', '6', '-frame-parallel', '0',
                         '-auto-alt-ref', '1', '-lag-in-frames', '25', '-g',
                         '128', '-pix_fmt', 'yuv420p', '-row-mt', '1'])


def image_size_changer(image_name):
    try:
        image = Image.open(image_name)
        width = image.width        
        height = image.height
        print(width, height)
        width = width+(width*0.35)
        height=height+(height*0.35)
        new_size=(math.floor(width), math.floor(height))
        print(new_size)
    except FileNotFoundError:
        pass
    else:
        sunset_resized = image.resize(new_size)
        sunset_resized.save(image_name)

# def image_on_video(video_path, image_path, result):
#     # image_size_changer(image_path)
#     video = VideoFileClip(video_path)

#     title = ImageClip(image_path).set_start(0).set_duration(video.duration).set_pos(("center","center")).set_opacity(.79)

#     final = CompositeVideoClip([video, title])
#     final.subclip(0, video.duration).write_videofile(result,
#                  codec='libvpx-vp9',
#                      threads='12', bitrate='8000k',
#                      ffmpeg_params=[
#                          '-tile-columns', '6', '-frame-parallel', '0',
#                          '-auto-alt-ref', '1', '-lag-in-frames', '25', '-g',
#                          '128', '-pix_fmt', 'yuv420p', '-row-mt', '1'])
#     # final.write_videofile(result)
# # image_on_video()