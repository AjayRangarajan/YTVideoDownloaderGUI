import os
from dotenv import load_dotenv

load_dotenv()



APP_VERSION = os.environ.get('APP_VERSION', '(latest)')

MAX_LOG_SIZE = eval(os.environ.get('MAX_LOG_SIZE', "10 * 1024 * 1024"))

# app
APP_WIDTH = int(os.environ.get('APP_WIDTH', 800))
APP_HEIGHT = int(os.environ.get('APP_HEIGHT', 450))
APP_GEOMETRY = "{}x{}+{}+{}"
MIN_WIDTH = int(os.environ.get('MIN_WIDTH', 550))
MIN_HEIGHT = int(os.environ.get('MIN_HEIGHT', 1000))
MAX_WIDTH = int(os.environ.get('MAX_WIDTH', 550))
MAX_HEIGHT = int(os.environ.get('MAX_HEIGHT', 500))
APPEARANCE_MODE = os.environ.get('APPEARANCE_MODE', "System")
COLOR_THEME = os.environ.get('COLOR_THEME', "blue")

# widgets
URL_ENTRY_WIDTH = int(os.environ.get('URL_ENTRY_WIDTH', 400))
THUMBNAIL_IMAGE_WIDTH = int(os.environ.get('THUMBNAIL_IMAGE_WIDTH', 180))
THUMBNAIL_IMAGE_HEIGHT = int(os.environ.get('THUMBNAIL_IMAGE_HEIGHT', 120))

DOWNLOAD_BUTTON_COLOR = os.environ.get('DOWNLOAD_BUTTON_COLOR', "#f71511")
DOWNLOAD_BUTTON_HOVER_COLOR = os.environ.get('DOWNLOAD_BUTTON_HOVER_COLOR', "#c4322f")
DOWNLOAD_BUTTON_FONT_COLOR = os.environ.get('DOWNLOAD_BUTTON_FONT_COLOR', "white")

# icons
ICON_CANCEL = "cancel"
ICON_WARNING = "warning"

# Messages
CANCELLED = "Cancelled!"
DOWNLOAD_CANCELLED = "Download Cancelled!"
SUCCESS = "Success!"
DOWNLOAD_SUCCESS = "Successfully downloaded the video!\ndownload path:{}\ndownload time: {}"
ERROR = "Error!"
INVALID_URL = "Invalid URL!\nPlease enter a valid Link!"
EMPTY_URL_INPUT = "Please enter a Youtube video link to download"
EXTENSIONS_AND_FORMATS_NOT_AVAILABLE = "Extensions and Formats not available for the download type {}. Please try a different download type"
DOWNLOAD_QUALITIES_AND_FORMATS_NOT_AVAILABLE = "Download qualities and formats not available for the extension {}. Please try a different extension"
FORMATS_NOT_AVAILABLE_FOR_THIS_QUALITY = "Formats not available for this type of quality {}. Please try a different one"
VIDEO_DETAILS_FETCH_SUCCESS = "SUCCESS"
FILESIZE_NOT_AVAILABLE = "NA"

# download types
DOWNLOAD_TYPE_VIDEO = "video"
DOWNLOAD_TYPE_AUDIO = "audio only"
DOWNLOAD_TYPE_VIDEO_ONLY = "video only"

# menus
DOWNLOAD_TYPES = [DOWNLOAD_TYPE_VIDEO, DOWNLOAD_TYPE_AUDIO, DOWNLOAD_TYPE_VIDEO_ONLY]

# progress
PROGRESS_DETERMINATE = "determinate"
PROGRESS_INDETERMINATE = "indeterminate"

NONE = 'none'