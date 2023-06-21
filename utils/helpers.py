import re
from typing import Tuple, MutableSet
from pathlib import Path
import tkinter as tk

from pytube import YouTube
from pytube.query import StreamQuery


def is_valid_youtube_url(url: str) -> bool:
    pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$"
    matches = re.match(pattern, url)

    return bool(matches)

def validate_filename(filename: str) -> str:
    pattern = r'[<>:"/\\|?*\x00-\x1F]'
    valid_filename = re.sub(pattern, '', filename)

    return valid_filename

def get_validated_unique_filename(download_path: Path, filename: str) -> bool:
    filename = validate_filename(filename)
    filepath = download_path.joinpath(filename)
    if filepath.exists():
        base_name, extension = filepath.stem, filepath.suffix
        counter = 1
        unique_filename = filename

        while (download_path / unique_filename).exists():
            unique_filename = f"{base_name}({counter}){extension}"
            counter += 1

        return unique_filename
    return filename

def calculate_center(app: tk.Tk, app_width: int, app_height: int) -> Tuple[int, int]:
    screen_width = int(app.winfo_screenwidth())
    screen_height = int(app.winfo_screenheight())

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    
    return int(x), int(y)

def get_formatted_size(size_in_bytes: int) -> str:
    if size_in_bytes < 1024 * 1024:
        size_str = f"{size_in_bytes / 1024:.2f} KB"
    elif size_in_bytes < 1024 * 1024 * 1024:
        size_str = f"{size_in_bytes / (1024 * 1024):.2f} MB"
    else:
        size_str = f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"
    return size_str

def get_formatted_time(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        formatted_time = f"{hours}:{minutes:02d}:{remaining_seconds:02d} hours"
    elif minutes > 0:
        formatted_time = f"{minutes}:{remaining_seconds:02d} minutes"
    else:
        formatted_time = f"{round(remaining_seconds)} seconds"

    return formatted_time

def get_streams(download_type: str, streams: StreamQuery) -> StreamQuery:
    
    if download_type == "video":
        return streams.filter(type="video", progressive=True)

    elif download_type == "audio":
        return streams.filter(type="audio")

    elif download_type ==  "video only":
        return streams.filter(type="video", adaptive=True)
    
    else:
        return

def get_mime_types(streams: StreamQuery) -> MutableSet[str]:
    mime_types = set()
    for stream in streams:
        mime_types.add(stream.mime_type)
    for mime_type in mime_types:
        if 'mp3' in mime_type:
            break
        if 'audio' in mime_type and not 'mp3' in mime_types:
            mime_types.add('mp3')
            break
    return mime_types

def get_resolution(download_mime_type: str, streams: StreamQuery) -> MutableSet[str]:
    resolutions = set()
    streams = streams.filter(mime_type=download_mime_type)
    for stream in streams:
        resolutions.add(stream.resolution)
    return resolutions

def get_abr(download_mime_type: str, streams: StreamQuery) -> MutableSet[str]:
    if download_mime_type == 'mp3':
        download_mime_type = "audio/mp4"
    streams = streams.filter(mime_type=download_mime_type)
    abr = set()
    for stream in streams:
        abr.add(stream.abr)
    return abr

def get_formatted_published_date(yt: YouTube) -> str:
    published_date = yt.publish_date
    return published_date.strftime("%d %B, %Y")