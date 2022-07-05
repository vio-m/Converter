from __future__ import absolute_import, unicode_literals
from celery import shared_task, current_task
from celery_progress.backend import ProgressRecorder
import youtube_dl
import time


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


@shared_task(bind=True)
def callable_hook(self, response):
    if response["status"] == "downloading":
        eta = response["eta"]
        percent = response['_percent_str']
        chunk = response['downloaded_bytes']
        total = response['total_bytes']
        return progress_recorder.set_progress(chunk, total, description=f'>>> {percent}')
    elif response["status"] == "finished":
        return progress_recorder.set_progress(100, 100, description=f'>>> Converting to mp3...')
    else:
        pass

ydl_opts = {'format': 'bestaudio/best',
            'extractaudio': True,
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '128', }],
            'outtmpl': "static/media/%(title)s.%(ext)s",
            'noplaylist': True,
            'quiet': False,
            'logger': MyLogger(),
            'progress_hooks': [callable_hook],
            }
ydl = youtube_dl.YoutubeDL(ydl_opts)

def get_info(video_URL):
    with ydl:
        info = ydl.extract_info(video_URL, download=False)
        info_dict = {'duration': info['duration'],
                     'video_title': info['title'],
                     'thumbnail': info['thumbnail']}
    return info_dict

@shared_task(bind=True)
def get_audio(self, video_URL):
    global progress_recorder
    progress_recorder = ProgressRecorder(self)
    with ydl:
        ydl.download([video_URL])
    return 'The deed is done!'


