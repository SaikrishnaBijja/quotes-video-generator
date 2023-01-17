from uuid import uuid4
from video_manager import make_final_video, download_video, get_video_link
import os, shutil, random, datetime
from add_used_link import to_enter, is_exist
from send_telegram import send_to_telegram
from get_tweet_img.screenshot import get_screen_shot
import itertools
import threading
import time
import sys

# theme=int(input('1.Motive\n2.Sad\nChoose Theme: '))
theme=1
themes={
    1:'Motive',
    2:'Sad',
}


def main():
    if theme ==1:
        open_tweets='tweets_motiv.txt'
        used_links='used_link_motiv.json'
    else:
        open_tweets='tweets_sad.txt'
        used_links='used_link_sad.json'

    with open(open_tweets, 'r') as data:
        tweets=data.readlines()

    for x in tweets:
        if is_exist(x, used_links):

            image_name=datetime.datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())+".png"
            video_name=image_name.replace(".png", ".mp4")

            get_screen_shot(x,f'temp_files/{image_name}', 0, 0)

            bg_music=random.choice(os.listdir(f'base_files/background_music/{themes[theme]}'))
            print(themes[theme])

            video_link=get_video_link(theme, used_links, f'temp_files/{video_name}')
            print('Got Video Link')

            make_final_video(video_path=f'temp_files/{video_name}', audio_path=f'base_files/background_music/{themes[theme]}/{bg_music}', result=f'result/{video_name}', image_path=f'temp_files/{image_name}')
            print('Final Video Created')

            send_to_telegram(f'result/{video_name}', theme)
            clean()

            to_enter(video_link, used_links)
            to_enter(x, used_links)

def clean():
    folder = 'temp_files'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

if __name__ == '__main__':
    main()


