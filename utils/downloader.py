from typing import Union, List, Callable
import youtube_dl
import os


async def download_by_url(url: str, path: str,) -> None:

    # Defining postprocessing for converting to mp3
    #postproc = {'key': 'FFmpegExtractAudio',
    #            'preferredcodec': 'mp3'},
    # Options for youtube-dl
    #postproc = {}
    ydl_opts = {
        #'format': "best",
        #'postprocessors': postproc,
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s') if ("playlist?list=" not in url \
                   or "list=" not in url) else os.path.join(path, '%(playlist_index)s-%(title)s.%(ext)s'),
        'progress_hooks': [lambda x: None],
    }

    # Download video with youtube-dl, passing options
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
