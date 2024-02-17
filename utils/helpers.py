import re
from typing import List, Tuple, MutableSet, Any
from pathlib import Path
import tkinter as tk
import datetime

from .log_helper import LogHelper
from .constants import *


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

def get_validated_unique_filename(download_path: Path, filename: str) -> str:
    filename = validate_filename(filename)
    logger.debug(f"Checking if the filename: '{filename}' already exists in the path: {download_path}")
    filepath = download_path.joinpath(filename)
    if filepath.exists():
        logger.debug(f"filename: '{filename}' already exists in the path: {download_path}")
        base_name, extension = filepath.stem, filepath.suffix
        counter = 1
        unique_filename = filename

        while (download_path / unique_filename).exists():
            unique_filename = f"{base_name}({counter}){extension}"
            counter += 1
        logger.debug(f"filename changed to '{unique_filename}'")
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

def get_formatted_upload_date(upload_date_str: str) -> str:
    upload_date = datetime.datetime.strptime(upload_date_str, '%Y%m%d')
    formatted_date = upload_date.strftime('%d %B, %Y')

    return formatted_date

def get_extensions_and_formats(download_type: str, formats: Any) -> Tuple[MutableSet[str], List[dict]]:
    extensions = set()
    download_type_formats = []

    if download_type == DOWNLOAD_TYPE_VIDEO_WITH_AUDIO:
        for fmt in formats:
            if (fmt.get('vcodec') != NONE) and (fmt.get('acodec') != NONE):
                download_type_formats.append(fmt)
                extensions.add(fmt.get('ext'))

    elif download_type ==  DOWNLOAD_TYPE_AUDIO:
        for fmt in formats:
            if (fmt.get('vcodec') == NONE) and (fmt.get('acodec') != NONE):
                download_type_formats.append(fmt)
                extensions.add(fmt.get('ext'))

    elif download_type == DOWNLOAD_TYPE_VIDEO_ONLY:
        for fmt in formats:
            if (fmt.get('vcodec') != NONE) and (fmt.get('acodec') == NONE):
                download_type_formats.append(fmt)
                extensions.add(fmt.get('ext'))

    return extensions, download_type_formats

def get_download_qualities_and_formats(extension: str, formats: Any) -> Tuple[MutableSet[str], List[dict]]:
    download_qualities = set()
    extension_type_formats = []
    for fmt in formats:
        if fmt.get('ext') == extension:
            if format_note := fmt.get('format_note'):
                download_qualities.add(format_note)
                extension_type_formats.append(fmt)
    return download_qualities, extension_type_formats