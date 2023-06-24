import logging
import timeit
import tkinter as tk
from pathlib import Path
from sys import platform
import urllib.request
import io

import pytube
from pytube.contrib.channel import Channel
import customtkinter as ctk
import CTkMessagebox as ctkmb
from PIL import Image

from utils.constants import *
from utils.helpers import *
from utils.log_helper import LogHelper


class App(ctk.CTk):

    def __init__(self, title: str, width: int, height: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.title(title)
        x, y = calculate_center(self, width, height)
        self.geometry(APP_GEOMETRY.format(width, height, x, y))
        self.resizable(False, False)
        
        logger.info("Setting icon for the app")
        if platform.startswith("win"):
            self.icon_path = ROOT_FOLDER.joinpath("images/icons/ico/icon1.ico")
            self.wm_iconbitmap(bitmap=self.icon_path)
        else:
            self.icon_path = ROOT_FOLDER.joinpath("images/icons/xbm/icon1.xbm")
            self.wm_iconbitmap(bitmap=self.icon_path)

        logger.info("Creating App widgets")
        self.create_widgets()

        logger.info("Placing App widgets")
        self.place_widgets()

    def create_widgets(self) -> None:
        self.url_entry_label = ctk.CTkLabel(self, text="Enter the Youtube video link below:")
        self.url_entry = ctk.CTkEntry(self, width=URL_ENTRY_WIDTH)
        self.search_button = ctk.CTkButton(self, text="Search", command=self.search_url)
    
    def place_widgets(self) -> None:
        self.url_entry_label.pack(side="top", expand=False, padx=5, pady=5)
        self.url_entry.pack(side="top", expand=False, padx=5, pady=5)
        self.search_button.pack(side="top", expand=False, padx=5, pady=5)

    def search_url(self) -> None:

        self.url = self.url_entry.get()
        logger.debug(f"Searching for the url {self.url}")

        if hasattr(self, "download_frame"):
            
            if hasattr(self.download_frame, "progress_frame"):
                logger.info("Destroying the existing progress_frame")
                self.download_frame.progress_frame.destroy()
            
            logger.info("Destroying the existing download_frame object")
            self.download_frame.destroy()

        if not self.url:
            logger.error(f"Empty URL input")
            ctkmb.CTkMessagebox(title=ERROR, message=EMPTY_URL_INPUT, icon=ICON_CANCEL)
            return
        if not is_valid_youtube_url(self.url):
            logger.error(f"The give url {self.url} is invalid")
            ctkmb.CTkMessagebox(title=ERROR, message=INVALID_URL, icon=ICON_CANCEL)
            return
        
        try:
            logger.debug(f"Creating youtube object for the url: {self.url}")
            self.yt = pytube.YouTube(
                self.url, 
                on_progress_callback=lambda *args, **kwargs: self.download_frame.update_progress(*args, **kwargs)
                )
            # Fetching streams in App only to check if streams are available to download
            logger.debug(f"Checking if streams are available for the URL: {self.url}")
            self.yt.streams
            logger.debug(f"Streams are available for the URL: {self.url}")

        except Exception as exception:
            logger.exception(exception)
            ctkmb.CTkMessagebox(title=ERROR, message=exception, icon=ICON_CANCEL)
            return

        logger.info("Creating download frame")
        self.download_frame = DownloadFrame(self, yt=self.yt)


class ProgressFrame(ctk.CTkFrame):

    def __init__(self, parent: tk.Tk, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.app = parent

        logger.info("Creating progress_frame widgets")
        self.create_widgets()
        logger.info("Placing progress_frame widgets")
        self.place_widgets()

        self.pack(side="bottom", expand=False, fill='x', padx=5, pady=5)

    def create_widgets(self) -> None:
        self.video_title_label = ctk.CTkLabel(self, text=None)
        self.progress_label = ctk.CTkLabel(self, text="0 %")
        self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal", mode="determinate")
        self.progressbar.set(0)

    def place_widgets(self) -> None:
        self.video_title_label.pack(side="top", expand=False, padx=5, pady=5)
        self.progress_label.pack(side="top", expand=False, padx=5, pady=(5, 0))
        self.progressbar.pack(side="top", expand=False, padx=5, pady=(2, 5))        


class VideoDetailsFrame(ctk.CTkFrame):

    def __init__(self, parent: tk.Tk, yt: pytube.YouTube, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        
        self.download_frame = parent
        self.yt = yt

        if self.fetch_video_details() == VIDEO_DETAILS_FETCH_SUCCESS:
        
            self.download_type = ctk.StringVar(self, value="Download Type")
            self.mime_type = ctk.StringVar(self, value="Mime Type")
            self.download_quality = ctk.StringVar(self, value="Quality")

            logger.info("Creating video_details widgets")
            self.create_widgets()
            logger.info("Placing video_details widgets")
            self.place_widgets()

            self.grid_columnconfigure((0, 1, 2), weight=1)
            self.grid_rowconfigure((0, 1, 2), weight=1)

    def create_widgets(self) -> None:
        self.title_label = ctk.CTkLabel(self, text=self.title, anchor='w')
        self.channel_label = ctk.CTkLabel(self, text=self.channel_name, anchor='w')
        self.duration_label = ctk.CTkLabel(self, text=self.duration)
        self.published_date_label = ctk.CTkLabel(self, text=self.published_date)
        self.download_type_menu = ctk.CTkOptionMenu(
            self, 
            variable=self.download_type,
            values=DOWNLOAD_TYPES,
            command=lambda download_type: self.update_mime_types(download_type)
            )
        self.mime_type_menu = ctk.CTkOptionMenu(
            self, 
            variable=self.mime_type, 
            values=None,
            command=lambda mime_type: self.update_download_quality(mime_type)
            )
        self.download_quality_menu = ctk.CTkOptionMenu(
            self, 
            variable=self.download_quality, 
            values=None,
            command=lambda download_quality: self.filter_streams(download_quality)
            )
        
    def place_widgets(self) -> None:
        self.title_label.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=(10, 5))
        self.channel_label.grid(row=1, column=0, sticky='nsew', padx=(10, 5))
        self.duration_label.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        self.published_date_label.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)
        self.download_type_menu.grid(row=2, column=0, padx=5, pady=5)
        self.mime_type_menu.grid(row=2, column=1, padx=5, pady=5)
        self.download_quality_menu.grid(row=2, column=2, padx=5, pady=5)

    def fetch_video_details(self) -> str:
        try:
            logger.info("Fetching streams from the youtube object")
            self.streams = self.yt.streams
            logger.info("Fetching title of the video")
            self.title = self.yt.title
            logger.debug(f"Video title: {self.title}")
            logger.info(f"Fetching channel name")
            self.channel = Channel(url=self.yt.channel_url)
            self.channel_name = self.channel.channel_name
            logger.debug(f"Channel name: {self.channel_name}")
            logger.info(f"Fetching video duration")
            self.duration = get_formatted_time(self.yt.length)
            logger.debug(f"Video duration: {self.duration}")
            logger.info("Fetching video published date")
            self.published_date = get_formatted_published_date(self.yt)
            logger.debug(f"Video published date {self.published_date}")

            logger.info("All video details required for video_details frame are successfully fetched")

            return VIDEO_DETAILS_FETCH_SUCCESS
        
        except Exception as exception:
            logger.exception(exception)
            ctkmb.CTkMessagebox(
                title=ERROR, 
                message=exception, 
                icon=ICON_CANCEL
            )
            return

    def update_mime_types(self, download_type: str) -> None:
        logger.debug(f"Download type, {download_type} selected! Updating mime type menu!!")
        self.mime_type.set("Mime Type")
        self.download_quality.set("Quality")
        self.download_frame.download_button.configure(state=tk.DISABLED)
        self.download_frame.download_button.update()

        self.download_type_streams = get_streams(download_type, self.streams)
        if self.download_type_streams is None:
            ctkmb.CTkMessagebox(
                title=ERROR, 
                message=STREAMS_NOT_AVAILABLE.format(self.download_type), 
                icon=ICON_CANCEL
            )
            return
        logger.debug(f"Fetching mime types for the download type {download_type}")
        self.mime_types = get_mime_types(self.download_type_streams)
        if self.mime_types is None:
            logger.error(f"Mime types not available for this download type {download_type}")
            ctkmb.CTkMessagebox(
                title=ERROR, 
                message=MIME_TYPES_NOT_AVAILABLE.format(self.download_type), 
                icon=ICON_CANCEL
            )
            return
        self.mime_type_menu.configure(values=self.mime_types)
        self.mime_type_menu.update()
        logger.debug(f'Updated mime types: {self.mime_types} to the menu')

    def update_download_quality(self, mime_type: str) -> None:
        logger.debug(f"Mime type {mime_type} choosed! Updating download quality!!")
        self.download_quality.set("Quality")
        self.download_frame.download_button.configure(state=tk.DISABLED)
        self.download_frame.download_button.update()

        if 'video' in mime_type:
            resolutions = get_resolution(mime_type, self.download_type_streams)
            if resolutions is None:
                logger.error(f"Video resolutions not available for this mime type {self.mime_type}")
                ctkmb.CTkMessagebox(
                    title=ERROR, 
                    message=VIDEO_RESOLUTIONS_NOT_AVAILABLE.format(self.mime_type), 
                    icon=ICON_CANCEL
                )
                return
            self.download_quality_menu.configure(values=resolutions)
            self.download_quality_menu.update()
            logger.debug(f"Updated video resolutions {resolutions} to the menu")
        elif 'audio' in mime_type or mime_type == 'mp3':
            audio_quality = get_abr(mime_type, self.download_type_streams)
            if audio_quality is None:
                logger.error(f"Audio quality not available for this mime type {self.mime_type}")
                ctkmb.CTkMessagebox(
                    title=ERROR, 
                    message=AUDIO_QUALITY_NOT_AVAILABLE.format(self.mime_type), 
                    icon=ICON_CANCEL
                )
                return
            self.download_quality_menu.configure(values=audio_quality)
            self.download_quality_menu.update()
            logger.debug(f"Updated audio quality {audio_quality}to the menu")
        
    def filter_streams(self, download_quality: str) -> None:

        download_type = self.download_type.get()
        mime_type = self.mime_type.get()
        quality = download_quality
        logger.debug(f"Filtering streams of DOWNLOAD_TYPE: {download_type}; MIME_TYPE: {mime_type}; QUALITY: {quality}")

        if mime_type == "mp3":
            mime_type = "audio/mp4"

        stream_filter = {
            'mime_type': mime_type
        }

        if 'video' in download_type:
            stream_filter['res'] = quality
        if download_type == 'video':
            stream_filter['progressive'] = True
        if download_type == 'video only':
            stream_filter['adaptive'] = True
        elif 'audio' in download_type:
            stream_filter['abr'] = quality
        logger.debug(f"Stream filter: {stream_filter}")

        start_time = timeit.default_timer()
        self.filtered_stream = self.streams.filter(**stream_filter).first()
        end_time = timeit.default_timer()
        self.filter_time = end_time - start_time
        logger.debug(f"Time taken to filter the streams {get_formatted_time(self.filter_time)}")

        self.filesize = get_formatted_size(self.filtered_stream.filesize)
        self.download_frame.filesize.set(self.filesize)

        logger.debug(f"Update filesize to {self.filesize} in the download_frame")

        self.download_frame.download_button.configure(state=tk.NORMAL)
        self.download_frame.download_button.update()
        logger.info("Enable download button")


class DownloadFrame(ctk.CTkFrame):

    def __init__(self, parent: tk.Tk, yt: pytube.YouTube, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.app = parent
        self.yt = yt

        if self.fetch_video_details() == VIDEO_DETAILS_FETCH_SUCCESS:
    
            logger.info("Creating download_frame widgets")
            self.create_widgets()
            logger.info("Placing download_frame widgets")
            self.place_widgets()

            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=3)

            self.grid_rowconfigure(0, weight=3)
            self.grid_rowconfigure(1, weight=1)

            self.pack(side='bottom', expand=False, padx=20, pady=30)

    def create_widgets(self) -> None:
        self.thumbnail_image_label = ctk.CTkLabel(self, text=None, image=self.thumbnail_image)
        self.video_details_frame = VideoDetailsFrame(self, yt=self.yt)
        self.filesize_label = ctk.CTkLabel(self, textvariable=self.filesize, text=None)
        self.download_button = ctk.CTkButton(
            self, text="Download", 
            fg_color=DOWNLOAD_BUTTON_COLOR,
            text_color=DOWNLOAD_BUTTON_FONT_COLOR,
            hover_color=DOWNLOAD_BUTTON_HOVER_COLOR,  
            state=tk.DISABLED, 
            command=self.download
        )

    def place_widgets(self) -> None:
        self.thumbnail_image_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.video_details_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.filesize_label.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.download_button.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)

    def fetch_video_details(self) -> str:
        try:
            logger.info("Fetching video title")
            self.title = self.yt.title
            logger.debug(f"Video title: {self.title}")
            self.filesize = ctk.StringVar(self, value="File size")
            logger.debug(f"Fetching thumbnail url for the video: {self.title}")
            self.thumbnail_url = self.yt.thumbnail_url
            logger.info("Fetching raw image data from the thumbnail url")
            with urllib.request.urlopen(self.thumbnail_url) as u:
                raw_img_data = u.read()
            logger.info("Converting the raw image data into an Image object")
            self.img = Image.open(io.BytesIO(raw_img_data))
            logger.debug(f"Creating CTkImage object of size {(THUMBNAIL_IMAGE_WIDTH, THUMBNAIL_IMAGE_HEIGHT)}")
            self.thumbnail_image = ctk.CTkImage(
                light_image=self.img, 
                dark_image=self.img, 
                size=(THUMBNAIL_IMAGE_WIDTH, THUMBNAIL_IMAGE_HEIGHT)
            )
            logger.info("All video details required for download_frame are successfully fetched")
            return VIDEO_DETAILS_FETCH_SUCCESS
        
        except Exception as exception:
            logger.exception(exception)
            ctkmb.CTkMessagebox(
                title=ERROR, 
                message=exception, 
                icon=ICON_CANCEL
            )
            return

    def update_progress(self, stream: pytube.Stream, chunk: bytes, bytes_remaining: int) -> None:
        logger.info("Updating download progress....")
        total_bytes = stream.filesize
        downloaded_bytes = total_bytes - bytes_remaining
        downloaded_percentage = int((downloaded_bytes / total_bytes) * 100)
        logger.debug(f"Total_Bytes: {total_bytes}; Downloaded_Bytes: {downloaded_bytes}; Downloaded_Percentage: {downloaded_percentage}")
        progressbar_value = float(downloaded_percentage / 100)
        logger.debug(f"progressbar value: {progressbar_value}")
        self.progress_frame.progressbar.set(progressbar_value)
        downloaded_size = get_formatted_size(downloaded_bytes)
        total_size = get_formatted_size(total_bytes)
        self.progress_frame.progress_label.configure(
            text=f"{downloaded_percentage} % ({downloaded_size}/{total_size})"
        )
        logger.debug(f"Total_Size: {total_size}; Downloaded_Size: {downloaded_size}; Downloaded_Percentage: {downloaded_percentage}")
        self.progress_frame.progress_label.update()
        logger.info("Progressbar updated!!!!")
            
    def download(self) -> None:
        try:
            logger.debug(f"downloading {self.title}")

            if hasattr(self, "progress_frame"):
                logger.info("Destroying existing progress_frame")
                self.progress_frame.destroy()

            mime_type = self.video_details_frame.mime_type.get()
            logger.debug(f"MIME_TYPE: {mime_type}")
            filename = f'{self.yt.title}.{mime_type.split("/")[-1]}'

            download_path = tk.filedialog.askdirectory()
            if not download_path:
                ctkmb.CTkMessagebox(
                    title=CANCELLED,
                    message=DOWNLOAD_CANCELLED,
                    icon="warning",
                    option_1="Close",
                )
                return
            download_path = Path(download_path)
            logger.debug(f"DOWNLOAD_PATH: {download_path}")
            filename = get_validated_unique_filename(download_path, filename)
                
            logger.info("Creating progressbar")
            self.progress_frame = ProgressFrame(app, fg_color="transparent")
            logger.debug(f"Configuring video title to {self.title}")
            self.progress_frame.video_title_label.configure(text=self.title)
            self.progress_frame.video_title_label.update()

            # download the filtered stream
            logger.info("Setting the value of progressbar to 0")
            self.progress_frame.progressbar.set(0)
            start_time = timeit.default_timer()
            logger.debug(f"DOWNLOADING {self.title}; FILENAME: {filename}; DOWNLOAD_PATH: {download_path}")
            self.video_details_frame.filtered_stream.download(output_path=download_path, filename=filename)
            end_time = timeit.default_timer()
            logger.info("Setting the value of progressbar to 1")
            self.progress_frame.progressbar.set(1)

            # update progress label to 100%
            logger.debug(f"Updating the progress_label to 100% with filesize: {self.filesize.get()}")
            self.progress_frame.progress_label.configure(text=f"100 % ({self.filesize.get()})")
            self.progress_frame.progress_label.update()

            download_time = end_time - start_time
            logger.debug(f"Time taken to only downloading: {get_formatted_time(download_time)}")
            download_time = get_formatted_time(self.video_details_frame.filter_time + download_time)
            logger.debug(f"Total time taken to search and download: {download_time}")
            ctkmb.CTkMessagebox(title=SUCCESS, message=DOWNLOAD_SUCCESS.format(download_path, download_time))

        except Exception as exception:
            logger.exception(exception)
            ctkmb.CTkMessagebox(title=ERROR, message=exception, icon=ICON_CANCEL)
            return



if __name__ == "__main__":

    for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

    log_helper = LogHelper()
    logger = log_helper.get_logger(__name__)

    logger.info("===========PROGRAM START===========")

    ROOT_FOLDER = Path(__file__).resolve().parent
    logger.debug(f"ROOT_FOLDER: {ROOT_FOLDER}")

    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)

    logger.info("Creating App instance")
    app = App(f"YouTube Video Downloader GUI {APP_VERSION}", APP_WIDTH, APP_HEIGHT)

    app.mainloop()
