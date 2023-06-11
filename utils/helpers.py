import re
from typing import Tuple, Union
import tkinter as tk


def is_valid_youtube_url(url: str) -> str:
    pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$"
    return re.match(pattern, url) is not None

def calculate_center(app: tk.Tk, app_width: int, app_height: int) -> Tuple[int, int]:
    screen_width = int(app.winfo_screenwidth())
    screen_height = int(app.winfo_screenheight())

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    
    return int(x), int(y)

def convert_download_time(seconds: Union[float, int]) -> str:
    seconds = round(seconds)
    if seconds >= 60:
        minutes = seconds // 60
        remainder_seconds = seconds % 60
        download_time = f"{minutes}:{remainder_seconds} minutes"
        return download_time
    if seconds >= 3600:
        hours = seconds // 3600
        remainder = seconds % 3600
        remainder_minutes = remainder // 60
        remainder_seconds = remainder % 60
        download_time = f"{hours}:{remainder_minutes}:{remainder_seconds} hours"
    return f"{seconds} seconds"