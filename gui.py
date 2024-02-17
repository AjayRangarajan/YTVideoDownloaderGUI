import logging
import timeit
import tkinter as tk
from pathlib import Path
from sys import platform
import urllib.request
import io
from typing import Any

import yt_dlp
import customtkinter as ctk
import CTkMessagebox as ctkmb
from PIL import Image

from utils.constants import *
from utils.helpers import *
from utils.log_helper import LogHelper


class AppEntryWidget(ctk.CTkEntry):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

class App(ctk.CTk):

    def __init__(self, title: str, width: int, height: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.title(title)
        x, y = calculate_center(self, width, height)
        self.geometry(APP_GEOMETRY.format(width, height, x, y))
        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.maxsize(MAX_WIDTH, MAX_HEIGHT)
        
        logger.info("Setting icon for the app")
        try:
            if platform.startswith("win"):
                self.icon_path = ROOT_FOLDER.joinpath("images/icons/ico/icon1.ico")
                self.wm_iconbitmap(bitmap=self.icon_path)
            elif platform.lower() == "darwin":
                self.icon_path = ROOT_FOLDER.joinpath("images/icons/icns/icon1.icns")
                self.wm_iconbitmap(bitmap=self.icon_path)
            elif platform.lower() == "linux":
                self.icon_path = ROOT_FOLDER.joinpath("images/icons/xbm/icon1.xbm")
                self.wm_iconbitmap(bitmap=self.icon_path)
            else:
                logger.error("Unable to set icon! Unidentified type of operating system.")
        except Exception as exception:
            logger.exception(exception)

        logger.info("Creating App widgets")
        self.create_widgets()

        logger.info("Placing App widgets")
        self.place_widgets()
    
    @classmethod
    def create_search_entry_widget(cls, parent: tk.Tk, *args, **kwargs):
        return cls.SearchEntryWidget(parent, *args, **kwargs)

    def create_widgets(self) -> None:
        self.url_entry_label = ctk.CTkLabel(self, text="Enter the Youtube video link below:")
        self.url_entry = self.create_search_entry_widget(self, width=URL_ENTRY_WIDTH)
        self.search_button = ctk.CTkButton(self, text="Search", state=tk.DISABLED, command=self.search_url)
    
    def place_widgets(self) -> None:
        self.url_entry_label.pack(side="top", expand=False, padx=5, pady=5)
        self.url_entry.pack(side="top", expand=False, padx=5, pady=5)
        self.search_button.pack(side="top", expand=False, padx=5, pady=5)

    class SearchEntryWidget(AppEntryWidget):

        def __init__(self, parent: tk.Tk, *args, **kwargs) -> None:
            super().__init__(parent, *args, **kwargs)
            self.app = parent
            self.bind('<Return>', lambda event: self.app.search_url())
            self.bind('<KeyRelease>', self.key_release)

        def key_release(self, event):
            self.app.search_button.configure(state=tk.NORMAL)
            self.app.search_button.update()

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
            logger.error(f"The given url {self.url} is invalid")
            ctkmb.CTkMessagebox(title=ERROR, message=INVALID_URL, icon=ICON_CANCEL)
            return
        
        try:
            logger.debug(f"Extracting video info of the URL: {self.url}")
            with yt_dlp.YoutubeDL() as ytdlp:
                self.video_info = ytdlp.extract_info(self.url, download=False)
            logger.debug(f"Successfully extracted video info of the URL: {self.url}")

        except Exception as exception:
            logger.debug(f"Playlist URL entered. URL: {self.url}")
            ctkmb.CTkMessagebox(title=ERROR, message=PLAYLIST_URL_ENTERED, icon=ICON_CANCEL)
            return
        
        if self.video_info.get('_type') == 'playlist' or self.video_info.get('entries'):
            ctkmb.CTkMessagebox(title=ERROR, message=PLAYLIST_URL_ENTERED, icon=ICON_CANCEL)
            return

        logger.info("Creating download frame")
        self.download_frame = DownloadFrame(self, video_info=self.video_info)


class DeterminateProgressFrame(ctk.CTkFrame):

    def __init__(self, parent: tk.Tk, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.app = parent

        logger.info("Creating determinate progress_frame widgets")
        self.create_widgets()
        logger.info("Placing determinate progress_frame widgets")
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

class InDeterminateProgressFrame(ctk.CTkFrame):

    def __init__(self, parent: tk.Tk, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.app = parent

        logger.info("Creating indeterminate progress_frame widgets")
        self.create_widgets()
        logger.info("Placing indeterminate progress_frame widgets")
        self.place_widgets()

        self.pack(side="bottom", expand=False, fill='x', padx=5, pady=5)

    def create_widgets(self) -> None:
        self.video_title_label = ctk.CTkLabel(self, text=None)
        self.progress_label = ctk.CTkLabel(self, text="Downloading")
        self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal", mode=PROGRESS_INDETERMINATE, indeterminate_speed=10)
        self.progressbar.set(0)

    def place_widgets(self) -> None:
        self.video_title_label.pack(side="top", expand=False, padx=5, pady=5)
        self.progress_label.pack(side="top", expand=False, padx=5, pady=(5, 0))
        self.progressbar.pack(side="top", expand=False, padx=5, pady=(2, 5))       


class VideoDetailsFrame(ctk.CTkFrame):

    def __init__(self, parent: tk.Tk, video_info: Any, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)
        
        self.download_frame = parent
        self.video_info = video_info
        self.include_caption = ctk.StringVar(value=INCLUDE_CAPTIONS_ON)

        if self.fetch_video_details() == VIDEO_DETAILS_FETCH_SUCCESS:
            self.download_type = ctk.StringVar(self, value="Download Type")
            self.extension = ctk.StringVar(self, value="Extension")
            self.download_quality = ctk.StringVar(self, value="Quality")

            logger.info("Creating video_details widgets")
            self.create_widgets()
            logger.info("Placing video_details widgets")
            self.place_widgets()

            self.grid_columnconfigure((0, 1, 2), weight=1)
            self.grid_rowconfigure((0, 1, 2), weight=1)

    def create_widgets(self) -> None:
        self.title_label = ctk.CTkLabel(self, text=self.title, anchor='w')
        self.include_caption_checkbox = ctk.CTkCheckBox(
            self, 
            text="Include captions", 
            variable= self.include_caption, 
            onvalue=INCLUDE_CAPTIONS_ON, 
            offvalue=INCLUDE_CAPTIONS_OFF)
        self.channel_label = ctk.CTkLabel(self, text=self.channel_name, anchor='w')
        self.duration_label = ctk.CTkLabel(self, text=self.duration)
        self.upload_date_label = ctk.CTkLabel(self, text=self.upload_date)
        self.download_types_menu = ctk.CTkOptionMenu(
            self, 
            variable=self.download_type,
            values=DOWNLOAD_TYPES,
            command=lambda download_type: self.update_extensions_menu(download_type)
            )
        self.extensions_menu = ctk.CTkOptionMenu(
            self, 
            variable=self.extension, 
            values=None,
            state=tk.DISABLED,
            command=lambda extension: self.update_download_qualities_menu(extension)
            )
        self.download_qualities_menu = ctk.CTkOptionMenu(
            self, 
            variable=self.download_quality, 
            values=None,
            state=tk.DISABLED,
            command=lambda download_quality: self.filter_download_quality_type_formats(download_quality)
            )
        
    def place_widgets(self) -> None:
        self.title_label.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=(10, 5))
        self.channel_label.grid(row=1, column=0, sticky='nsew', padx=(10, 5))
        self.duration_label.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        self.upload_date_label.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)
        self.include_caption_checkbox.grid(row=1, column=3, sticky='nsew', padx=5, pady=5)
        self.download_types_menu.grid(row=2, column=0, padx=5, pady=5)
        self.extensions_menu.grid(row=2, column=1, padx=5, pady=5)
        self.download_qualities_menu.grid(row=2, column=2, padx=5, pady=5)

    def fetch_video_details(self) -> str:
        try:
            logger.info("Fetching video formats")
            self.formats = self.video_info['formats']
            logger.info("Fetching title of the video")
            self.title = self.video_info['title']
            logger.debug(f"Video title: {self.title}")
            logger.info(f"Fetching channel name")
            self.channel_name = self.video_info['channel']
            logger.debug(f"Channel name: {self.channel_name}")
            logger.info(f"Fetching video duration")
            self.duration = get_formatted_time(self.video_info['duration'])
            logger.debug(f"Video duration: {self.duration}")
            logger.info("Fetching video uploaded date")
            self.upload_date = get_formatted_upload_date(self.video_info['upload_date'])
            logger.debug(f"Video uploaded date {self.upload_date}")

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

    def update_extensions_menu(self, download_type: str) -> None:
        logger.debug(f"Download type, {download_type} selected! Updating extensions menu!!")
        self.extension.set("Extension")
        self.download_quality.set("Quality")
        self.download_qualities_menu.configure(state=tk.DISABLED)
        self.download_qualities_menu.update()
        self.download_frame.download_button.configure(state=tk.DISABLED)
        self.download_frame.download_button.update()

        logger.debug(f"Fetching extensions and formats of download type: {download_type}")
        extensions, self.download_type_formats = get_extensions_and_formats(download_type, self.formats)
        if not extensions:
            logger.error(f"No extensions and formats available for the download type: {download_type}")
            logger.debug(f"Extensions: {extensions}")
            logger.debug(f"Download type formats: {self.download_type_formats}")
            ctkmb.CTkMessagebox(
                title=ERROR, 
                message=EXTENSIONS_AND_FORMATS_NOT_AVAILABLE.format(self.download_type.get()), 
                icon=ICON_CANCEL
            )
            return
        logger.debug(f"Available formats for the download type {download_type}:")
        for fmt in self.download_type_formats:
            logger.debug(fmt)

        self.extensions_menu.configure(values=extensions, state=tk.NORMAL)
        self.extensions_menu.update()
        logger.debug(f'Updated extensions: {extensions}')

    def update_download_qualities_menu(self, extension: str) -> None:
        logger.debug(f"Extension {extension} choosed! Updating download qualities menu!!")
        self.download_quality.set("Quality")
        self.download_frame.download_button.configure(state=tk.DISABLED)
        self.download_frame.download_button.update()

        logger.debug(f"Fetching available qualities and formats for the extension: {extension}")
        download_qualities, self.extension_type_formats = get_download_qualities_and_formats(extension, self.download_type_formats)
        if not download_qualities:
            logger.error(f"Qualities and formats not available for this extension {self.extension}")
            ctkmb.CTkMessagebox(
                title=ERROR, 
                message=DOWNLOAD_QUALITIES_AND_FORMATS_NOT_AVAILABLE.format(self.extension), 
                icon=ICON_CANCEL
            )
            return
        self.download_qualities_menu.configure(values=download_qualities, state=tk.NORMAL)
        self.download_qualities_menu.update()
        logger.debug(f"Updated download qualities: {download_qualities}")

    def filter_download_quality_type_formats(self, download_quality: str) -> None:

        download_type = self.download_type.get()
        extension = self.extension.get()
        quality = download_quality
        logger.debug(f"Filtering formats of DOWNLOAD_TYPE: {download_type}; EXTENSION: {extension}; QUALITY: {quality}")

        download_quality_type_formats = []
        for fmt in self.extension_type_formats:
            if fmt['format_note'] == quality:
                download_quality_type_formats.append(fmt)

        if not download_quality_type_formats:
            logger.error(f"No formats available for this quality {quality}")
            ctkmb.CTkMessagebox(
                title=ERROR, 
                message=FORMATS_NOT_AVAILABLE_FOR_THIS_QUALITY.format(quality), 
                icon=ICON_CANCEL
            )
            return
        logger.debug(f"Filtered download quality type formats: {download_quality_type_formats}")
        self.selected_format = download_quality_type_formats[0]
        logger.debug(f"Selected format: {self.selected_format}")
        try:
            self.filesize = get_formatted_size(self.selected_format.get('filesize'))
        except TypeError:
            try:
                self.filesize = get_formatted_size(self.selected_format.get('filesize_approx'))
            except TypeError:
                self.filesize = FILESIZE_NOT_AVAILABLE
    
        self.download_frame.filesize.set(self.filesize)

        logger.debug(f"Update filesize to {self.filesize} in the download_frame")

        self.download_frame.download_button.configure(state=tk.NORMAL)
        self.download_frame.download_button.update()
        logger.info("Enable download button")


class DownloadFrame(ctk.CTkFrame):

    def __init__(self, parent: tk.Tk, video_info: Any, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.app = parent
        self.video_info = video_info
        self.downloaded_size = None

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
        self.video_details_frame = VideoDetailsFrame(self, video_info=self.video_info)
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
            logger.info("Fetching video details")
            logger.info("Fetching video title")
            self.title = self.video_info['title']
            logger.debug(f"Video title: {self.title}")
            self.filesize = ctk.StringVar(self, value="File size")
            logger.debug(f"Fetching thumbnail url for the video: {self.title}")
            self.thumbnail_url = self.video_info['thumbnail']
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

    def update_indeterminate_progress(self, progress) -> None:
        logger.info("Updating indeterminate download progress....")
        downloaded_bytes = progress.get('downloaded_bytes', None)
        logger.debug(f"Downloaded_Bytes: {downloaded_bytes}")
        if downloaded_bytes == None:
            self.downloaded_size = get_formatted_size(downloaded_bytes)
            self.progress_frame.progress_label.configure(text=f"Downloading ({self.downloaded_size})")
        else:
            self.progress_frame.progress_label.configure(text=f"Downloading...")
        self.progress_frame.progressbar.step()
        self.progress_frame.progressbar.update()

        logger.info("Indeterminate Progressbar updated!!!!")

    
    def update_progress(self, progress) -> None:
        logger.info("Updating determinate download progress....")
        total_bytes = progress.get('total_bytes', None)
        logger.debug(f"TOTAL_BYTES: {total_bytes}")
        downloaded_bytes = progress.get('downloaded_bytes', None)
        logger.debug(f"DOWNLOADED_BYTES: {downloaded_bytes}")
        downloaded_percentage = 50
        if downloaded_bytes != None and total_bytes != None:
            downloaded_percentage = int((downloaded_bytes / total_bytes) * 100)
            downloaded_size = get_formatted_size(downloaded_bytes)
            total_size = get_formatted_size(total_bytes)
        elif downloaded_bytes == None and total_bytes != None:
            downloaded_size = NOT_AVAILABLE
            total_size = get_formatted_size(total_bytes)
        elif downloaded_bytes != None and total_bytes == None:
            total_size = NOT_AVAILABLE
            downloaded_size = get_formatted_size(downloaded_bytes)
        else:
            total_size = get_formatted_size(total_bytes)
            downloaded_size = get_formatted_size(downloaded_bytes)
        logger.debug(f"DOWNLOADED_PERCENTAGE: {downloaded_percentage}")
        logger.debug(f"Total_Bytes: {total_bytes}; Downloaded_Bytes: {downloaded_bytes}; Downloaded_Percentage: {downloaded_percentage}")
        progressbar_value = float(downloaded_percentage / 100)
        logger.debug(f"progressbar value: {progressbar_value}")
        self.progress_frame.progressbar.set(progressbar_value)
        
        self.progress_frame.progress_label.configure(
            text=f"{downloaded_percentage} % ({downloaded_size}/{total_size})"
        )
        logger.debug(f"Total_Size: {total_size}; Downloaded_Size: {downloaded_size}; Downloaded_Percentage: {downloaded_percentage}")
        self.progress_frame.progress_label.update()
        logger.info("Determinate Progressbar updated!!!!")
            
    def download(self) -> None:
        try:
            logger.debug(f"downloading {self.title}")

            # Disable all inputs
            logger.info("Disabling all inputs")
            self.video_details_frame.include_caption_checkbox.configure(state=tk.DISABLED)
            self.video_details_frame.include_caption_checkbox.update()
            self.video_details_frame.download_types_menu.configure(state=tk.DISABLED)
            self.video_details_frame.download_types_menu.update()
            self.video_details_frame.download_qualities_menu.configure(state=tk.DISABLED)
            self.video_details_frame.download_qualities_menu.update()
            self.video_details_frame.extensions_menu.configure(state=tk.DISABLED)
            self.video_details_frame.extensions_menu.update()
            self.download_button.configure(state=tk.DISABLED)
            self.download_button.update()
            self.app.search_button.configure(state=tk.DISABLED)
            self.app.search_button.update()

            if hasattr(self, "progress_frame"):
                logger.info("Destroying existing progress_frame")
                self.progress_frame.destroy()

            extension = self.video_details_frame.extension.get()
            logger.debug(f"EXTENSION: {extension}")
            filename = f'{self.title}.{extension}'

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
            fmt_id = self.video_details_frame.selected_format['format_id']
            filepath = str(download_path / filename)

            logger.info("Creating progressbar")
            if self.filesize.get() == FILESIZE_NOT_AVAILABLE:
                logger.info("filesize not available. creating indeterminate progress frame.")
                self.progress_mode = PROGRESS_INDETERMINATE
                self.progress_frame = InDeterminateProgressFrame(app, fg_color="transparent")
                ytdlp_options = {
                    'progress_hooks': [self.update_indeterminate_progress],
                    'outtmpl': filepath,
                    'format': fmt_id,
                } 
            else:
                logger.info("filesize is available. creating determinate progress frame.")
                self.progress_mode = PROGRESS_DETERMINATE
                self.progress_frame = DeterminateProgressFrame(app, fg_color="transparent")
                ytdlp_options = {
                    'progress_hooks': [self.update_progress],
                    'outtmpl': filepath,
                    'format': fmt_id,
                }

            if self.video_details_frame.include_caption.get() == INCLUDE_CAPTIONS_ON:
                logger.info("Including subtitle options")
                ytdlp_options['writesubtitles'] = True
                ytdlp_options['writeautomaticsub'] = True

            logger.debug(f"Configuring video title: {self.title}")
            self.progress_frame.video_title_label.configure(text=self.title)
            self.progress_frame.video_title_label.update()

            # download the filtered stream
            start_time = timeit.default_timer()
            logger.debug(f"DOWNLOADING {self.title}; FILENAME: {filename}; DOWNLOAD_PATH: {download_path}")
            self.video_info['requested_formats'] = [self.video_details_frame.selected_format]
            with yt_dlp.YoutubeDL(ytdlp_options) as ytdl:
              ytdl.process_ie_result(self.video_info, download=True)
            end_time = timeit.default_timer()

            if self.progress_mode == PROGRESS_INDETERMINATE:
                pass
                logger.debug(f"Updating the progress_label to 'Downloaded' with downloaded filesize: {self.downloaded_size}")
                self.progress_frame.progress_label.configure(text=f"Video Downloaded ({self.downloaded_size})")
                self.progress_frame.progressbar.destroy()
                self.progress_frame.progress_label.update()

            else:
                # update progress label to 100%
                logger.info("Setting the value of progressbar to 1")
                self.progress_frame.progressbar.set(1)
                self.progress_frame.progressbar.update()
                logger.debug(f"Updating the progress_label to 100% with filesize: {self.filesize.get()}")
                self.progress_frame.progress_label.configure(text=f"100 % ({self.filesize.get()})")
                self.progress_frame.progress_label.update()

            download_time = end_time - start_time
            download_time = get_formatted_time(int(download_time))
            logger.debug(f"Time taken to download video: {download_time}")
            ctkmb.CTkMessagebox(title=SUCCESS, message=DOWNLOAD_SUCCESS.format(download_path, download_time))

        except Exception as exception:
            logger.exception(exception)
            ctkmb.CTkMessagebox(title=ERROR, message=exception, icon=ICON_CANCEL)
            return

        finally:
            # Enable all inputs
            logger.info("Enabling all inputs")
            self.video_details_frame.include_caption_checkbox.configure(state=tk.NORMAL)
            self.video_details_frame.include_caption_checkbox.update()
            self.video_details_frame.download_types_menu.configure(state=tk.NORMAL)
            self.video_details_frame.download_types_menu.update()
            self.video_details_frame.download_qualities_menu.configure(state=tk.NORMAL)
            self.video_details_frame.download_qualities_menu.update()
            self.video_details_frame.extensions_menu.configure(state=tk.NORMAL)
            self.video_details_frame.extensions_menu.update()
            self.download_button.configure(state=tk.NORMAL)
            self.download_button.update()
            self.app.search_button.configure(state=tk.NORMAL)
            self.app.search_button.update()


if __name__ == "__main__":

    for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

    log_helper = LogHelper()
    logger = log_helper.get_logger(__name__)

    ROOT_FOLDER = Path(__file__).resolve().parent
    logger.debug(f"ROOT_FOLDER: {ROOT_FOLDER}")

    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)

    logger.info("Creating App instance")
    app = App(f"YouTube Video Downloader GUI {APP_VERSION}", APP_WIDTH, APP_HEIGHT)

    app.mainloop()
