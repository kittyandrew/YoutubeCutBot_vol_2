from moviepy.video.io.VideoFileClip import VideoFileClip
from typing import List
import secrets
import re
import os


def cut_the_butt(file_path:str, text:str) -> List[str]:
    pattern = re.compile(r"\d{1,3}\:\d\d\-\d{1,3}\:\d\d")
    result = []
    for each in pattern.findall(text):
        start, finish = each.split("-")
        start_m, start_s = start.split(":")
        finish_m, finish_s = finish.split(":")
        start_m, start_s = int(start_m), int(start_s)
        finish_m, finish_s = int(finish_m), int(finish_s)

        start_time = start_m * 60 + start_s
        end_time = finish_m * 60 + finish_s

        # Saving
        new_name = f"{start_m}m{start_s}s-{finish_m}m{finish_s}s-extracted.mp4"
        new_path = os.path.join(*file_path.split("\\")[:-1], new_name)
        with VideoFileClip(file_path) as video:
            new = video.subclip(start_time, end_time)
            new.write_videofile(new_path, audio_codec='aac')
        result.append(new_path)
    return result