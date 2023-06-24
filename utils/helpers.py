import re
from typing import Tuple, MutableSet
from pathlib import Path
import tkinter as tk

from pytube import YouTube
from pytube.query import StreamQuery

from .log_helper import LogHelper


log_helper = LogHelper()
logger = log_helper.get_logger("utils_helper")


def is_valid_youtube_url(url: str) -> bool:
    logger.info("checking if the url is a valid YouTube URL")
    pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$"
    matches = re.match(pattern, url)

    return bool(matches)

def validate_filename(filename: str) -> str:
    logger.debug(f"validating file name: {filename}")
    pattern = r'[<>:"/\\|?*\x00-\x1F]'
    validated_filename = re.sub(pattern, '', filename)
    logger.debug(f"Validated filename: {validated_filename}")
    return validated_filename

def get_validated_unique_filename(download_path: Path, filename: str) -> bool:
    filename = validate_filename(filename)
    logger.debug(f"Checking if the filename: {filename} already exists in the path: {download_path}")
    filepath = download_path.joinpath(filename)
    if filepath.exists():
        logger.debug(f"filename: {filename} already exists in the path: {download_path}")
        base_name, extension = filepath.stem, filepath.suffix
        counter = 1
        unique_filename = filename

        while (download_path / unique_filename).exists():
            unique_filename = f"{base_name}({counter}){extension}"
            counter += 1
        logger.debug(f"filename changed to {unique_filename}")
        return unique_filename
    return filename

def calculate_center(app: tk.Tk, app_width: int, app_height: int) -> Tuple[int, int]:
    logger.info("Calculating the center of the application")
    screen_width = int(app.winfo_screenwidth())
    screen_height = int(app.winfo_screenheight())

    x = int((screen_width / 2) - (app_width / 2))
    y = int((screen_height / 2) - (app_height / 2))
    logger.debug(f"Successfully calculated the center as {(x, y)}")
    return x, y

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
    logger.debug(f"Fetching streams of download type: {download_type}")
    download_type_streams = None

    if download_type == "video":
        download_type_streams = streams.filter(type="video", progressive=True)

    elif download_type == "audio":
        download_type_streams = streams.filter(type="audio")

    elif download_type ==  "video only":
        download_type_streams = streams.filter(type="video", adaptive=True)
    
    logger.debug(f"Available streams for the download type {download_type}:")
    if download_type_streams is None:
        logger.error(f"No streams available for the download type: {download_type}")
        return
    for stream in download_type_streams:
        logger.debug(stream)

    return download_type_streams

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
    if len(mime_types) == 0:
        return
    return mime_types

def get_resolution(download_mime_type: str, streams: StreamQuery) -> MutableSet[str]:
    logger.debug(f"Fetching available resolutions for the mime type: {download_mime_type}")
    resolutions = set()
    streams = streams.filter(mime_type=download_mime_type)
    for stream in streams:
        resolutions.add(stream.resolution)
    if len(resolutions) == 0:
        return
    return resolutions

def get_abr(download_mime_type: str, streams: StreamQuery) -> MutableSet[str]:
    logger.debug(f"Fetching available audio qualities for the mime type: {download_mime_type}")
    if download_mime_type == 'mp3':
        download_mime_type = "audio/mp4"
    streams = streams.filter(mime_type=download_mime_type)
    abr = set()
    for stream in streams:
        abr.add(stream.abr)
    if len(abr) == 0:
        return
    return abr

def get_formatted_published_date(yt: YouTube) -> str:
    published_date = yt.publish_date
    return published_date.strftime("%d %B, %Y")