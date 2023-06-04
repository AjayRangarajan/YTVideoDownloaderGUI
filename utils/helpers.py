import re

def is_valid_youtube_url(url):
    pattern = r"^(https?://)?(www\.)?(youtube\.com|youtu\.?be)/.+$"
    return re.match(pattern, url) is not None

def calculate_center(app, app_width, app_height):
    screen_width = int(app.winfo_screenwidth())
    screen_height = int(app.winfo_screenheight())

    x = (screen_width / 2) - (app_width / 2)
    y = (screen_height / 2) - (app_height / 2)
    
    return int(x), int(y)

def convert_download_time(seconds):
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

def get_resolutions_with_formatted_size(streams):
    resolutions = []
    for stream in streams:
        size_in_bytes = stream.filesize
        if size_in_bytes < 1024 * 1024:
            size_str = f"{size_in_bytes / 1024:.2f} KB"
        elif size_in_bytes < 1024 * 1024 * 1024:
            size_str = f"{size_in_bytes / (1024 * 1024):.2f} MB"
        else:
            size_str = f"{size_in_bytes / (1024 * 1024 * 1024):.2f} GB"
        resolutions.append((stream.resolution, size_str))
    return resolutions

def get_mime_types(streams):
    extensions = set()
    for stream in streams:
        mime_type = stream.mime_type
        ext = mime_type.split("/")[-1]
        extensions.add(ext)
    return extensions
