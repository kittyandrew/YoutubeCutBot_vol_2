from pydub import AudioSegment
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

        start_time = start_m * 60 * 1000 + start_s * 1000
        end_time = finish_m * 60 * 1000 + finish_s * 1000

        # File manipulation
        song = AudioSegment.from_mp3(file_path)
        extracted = song[start_time:end_time]
        # Saving
        new_name = f"{start_m}m{start_s}s-{finish_m}m{finish_s}s-extracted.mp3"
        new_path = os.path.join(*file_path.split("\\")[:-1], new_name)
        extracted.export(new_path, format="mp3")
        result.append(new_path)
    return result