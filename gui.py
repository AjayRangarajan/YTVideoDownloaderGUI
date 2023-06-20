import timeit
import tkinter as tk
from pathlib import Path
from sys import platform
import urllib.request
import io

import pytube
from pytube.exceptions import RegexMatchError
from pytube.contrib.channel import Channel
import customtkinter as ctk
import CTkMessagebox as ctkmb
from PIL import Image

from utils.constants import *
from utils.helpers import *


class App(ctk.CTk):

    def __init__(self, title: str, width: int, height: int, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.title(title)
        x, y = calculate_center(self, width, height)
        self.geometry(APP_GEOMETRY.format(width, height, x, y))
        # self.maxsize(width, height)
        self.resizable(False, False)
        
        if platform.startswith("win"):
            self.icon_path = ROOT_FOLDER.joinpath("images/icons/ico/icon1.ico")
            self.wm_iconbitmap(bitmap=self.icon_path)
        else:
            self.icon_path = ROOT_FOLDER.joinpath("images/icons/xbm/icon1.xbm")
            self.wm_iconbitmap(bitmap=self.icon_path)

        self.create_widgets()
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

        if not self.url:
            ctkmb.CTkMessagebox(title=ERROR, message=EMPTY_URL_INPUT, icon=ICON_CANCEL)
            return
        if not is_valid_youtube_url(self.url):
            ctkmb.CTkMessagebox(title=ERROR, message=INVALID_URL, icon=ICON_CANCEL)
            return
        
        try:
            self.yt = pytube.YouTube(
                self.url, 
                on_progress_callback=lambda *args, **kwargs: self.download_frame.update_progress(*args, **kwargs)
                )
        except RegexMatchError:
            ctkmb.CTkMessagebox(title=ERROR, message=INVALID_VIDEO_ID, icon=ICON_CANCEL)
            return
        except Exception as exception:
            ctkmb.CTkMessagebox(title=ERROR, message=exception, icon=ICON_CANCEL)
            return

        if hasattr(self, "download_frame"):
            if hasattr(self.download_frame, "progress_frame"):
                self.download_frame.progress_frame.destroy()
            self.download_frame.destroy()

        self.download_frame = DownloadFrame(self, yt=self.yt)


class ProgressFrame(ctk.CTkFrame):

    def __init__(self, parent: tk.Tk, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.app = parent
        self.create_widgets()
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
        self.streams = yt.streams
        self.title = self.yt.title
        self.channel = Channel(url=self.yt.channel_url)
        self.channel_name = self.channel.channel_name
        self.duration = get_formatted_time(self.yt.length)
        self.published_date = get_formatted_published_date(self.yt)

        self.download_type = ctk.StringVar(self, value="Download Type")
        self.mime_type = ctk.StringVar(self, value="Mime Type")
        self.download_quality = ctk.StringVar(self, value="Quality")

        self.create_widgets()
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

    def update_mime_types(self, download_type: str) -> None:
        self.mime_type.set("Mime Type")
        self.download_quality.set("Quality")
        self.download_frame.download_button.configure(state=tk.DISABLED)
        self.download_frame.download_button.update()

        self.download_type_streams = get_streams(download_type, self.streams)
        self.mime_types = get_mime_types(self.download_type_streams)
        self.mime_type_menu.configure(values=self.mime_types)
        self.mime_type_menu.update()

    def update_download_quality(self, mime_type: str) -> None:
        self.download_quality.set("Quality")
        self.download_frame.download_button.configure(state=tk.DISABLED)
        self.download_frame.download_button.update()

        if 'video' in mime_type:
            self.download_quality_menu.configure(values=get_resolution(mime_type, self.download_type_streams))
            self.download_quality_menu.update()
        elif 'audio' in mime_type or mime_type == 'mp3':
            self.download_quality_menu.configure(values=get_abr(mime_type, self.download_type_streams))
            self.download_quality_menu.update()
        
    def filter_streams(self, download_quality: str) -> None:
        mime_type = self.mime_type.get()
        download_type = self.download_type.get()
        quality = download_quality

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

        start_time = timeit.default_timer()
        self.filtered_stream = self.streams.filter(**stream_filter).first()
        end_time = timeit.default_timer()
        self.filter_time = end_time - start_time

        self.filesize = get_formatted_size(self.filtered_stream.filesize)
        self.download_frame.filesize.set(self.filesize)

        self.download_frame.download_button.configure(state=tk.NORMAL)
        self.download_frame.download_button.update()


class DownloadFrame(ctk.CTkFrame):

    def __init__(self, parent: tk.Tk, yt: pytube.YouTube, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.app = parent
        self.yt = yt
        self.title = yt.title
        self.filesize = ctk.StringVar(self, value="File size")

        self.thumbnail_url = self.yt.thumbnail_url
        with urllib.request.urlopen(self.thumbnail_url) as u:
            raw_img_data = u.read()
        self.img = Image.open(io.BytesIO(raw_img_data))
        self.thumbnail_image = ctk.CTkImage(
            light_image=self.img, 
            dark_image=self.img, 
            size=(THUMBNAIL_IMAGE_WIDTH, THUMBNAIL_IMAGE_HEIGHT)
        )

        self.create_widgets()
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

    def update_progress(self, stream: pytube.Stream, chunk: bytes, bytes_remaining: int) -> None:
        total_bytes = stream.filesize
        downloaded_bytes = total_bytes - bytes_remaining
        download_percentage = int((downloaded_bytes / total_bytes) * 100)
        self.progress_frame.progressbar.set(float(download_percentage / 100))
        downloaded_size = get_formatted_size(downloaded_bytes)
        total_size = get_formatted_size(total_bytes)
        self.progress_frame.progress_label.configure(
            text=f"{download_percentage} % ({downloaded_size}/{total_size})"
        )
        self.progress_frame.progress_label.update()

    def get_download_location(self, file_name: str) -> str:
        download_path = tk.filedialog.askdirectory()
        if not download_path:
            ctkmb.CTkMessagebox(
                title=CANCELLED,
                message=DOWNLOAD_CANCELLED,
                icon="warning",
                option_1="Close",
            )
            return
            
        file_path = Path(download_path).joinpath(file_name)
        if file_path.exists():
            file_exists = ctkmb.CTkMessagebox(
                    title=FILE_EXISTS_TITLE, 
                    message=FILE_EXISTS_MESSAGE,
                    icon="warning", 
                    option_1="Cancel", 
                    option_2="Choose another folder", 
                    option_3="Yes"
                )
            res = file_exists.get()
            if res == "Yes":
                try:
                    file_path.unlink()
                    return download_path
                except Exception as exception:
                    ctkmb.CTkMessagebox(title=ERROR, message=exception, icon="cancel")
                    return
                
            elif res == "Choose another folder":
                download_path = self.get_download_location(file_name)
                return download_path
            
            else:
                return
        else:
            return download_path

    def download(self) -> None:
        try:

            if hasattr(self, "progress_frame"):
                self.progress_frame.destroy()

            mime_type = self.video_details_frame.mime_type.get()
            file_name = f'{self.yt.title}.{mime_type.split("/")[-1]}'

            download_path = self.get_download_location(file_name)
            if not download_path:
                return

            self.progress_frame = ProgressFrame(app, fg_color="transparent")
            self.progress_frame.video_title_label.configure(text=self.title)
            self.progress_frame.video_title_label.update()

            # download the filtered stream
            self.progress_frame.progressbar.set(0)
            start_time = timeit.default_timer()
            self.video_details_frame.filtered_stream.download(output_path=download_path, filename=file_name)
            end_time = timeit.default_timer()
            self.progress_frame.progressbar.set(1)

            # update progress label to 100%
            self.progress_frame.progress_label.configure(text=f"100 % ({self.filesize.get()})")
            self.progress_frame.progress_label.update()

            download_time = end_time - start_time
            download_time = get_formatted_time(self.video_details_frame.filter_time + download_time)
            ctkmb.CTkMessagebox(title=SUCCESS, message=DOWNLOAD_SUCCESS.format(download_path, download_time))

        except RegexMatchError:
            ctkmb.CTkMessagebox(title=ERROR, message=INVALID_VIDEO_ID, icon=ICON_CANCEL)

        except Exception as exception:
            ctkmb.CTkMessagebox(title=ERROR, message=exception, icon=ICON_CANCEL)



if __name__ == "__main__":

    ROOT_FOLDER = Path(__file__).resolve().parent

    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)

    app = App(f"YouTube Video Downloader GUI {APP_VERSION}", APP_WIDTH, APP_HEIGHT)

    app.mainloop()
