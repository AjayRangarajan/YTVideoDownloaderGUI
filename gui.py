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

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)
        self.title(f"YouTube Video Downloader GUI {APP_VERSION}")
        x, y = calculate_center(self, APP_WIDTH, APP_HEIGHT)
        self.geometry(APP_GEOMETRY.format(APP_WIDTH, APP_HEIGHT, x, y))
        self.maxsize(APP_WIDTH, APP_HEIGHT)
        
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
        self.url_entry = ctk.CTkEntry(self, width=400)
        self.search_button = ctk.CTkButton(self, text="Download", command=self.validate_url)
    
    def place_widgets(self) -> None:
        self.url_entry_label.pack(side="top", expand=False, padx=5, pady=5)
        self.url_entry.pack(side="top", expand=False, padx=5, pady=5)
        self.search_button.pack(side="top", expand=False, padx=5, pady=5)

    def validate_url(self) -> None:
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
        self.create_widgets()
        self.place_widgets()
        self.pack(side="bottom", expand=False, fill='x', padx=5, pady=5)

    def create_widgets(self) -> None:
        self.video_title_label = ctk.CTkLabel(self, text="")
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

        self.mime_types = None
        self.download_quality = None
        self.selected_download_type = ctk.StringVar(self, value="Download Type")
        self.selected_mime_type = ctk.StringVar(self, value="Mime Type")
        self.selected_download_quality = ctk.StringVar(self, value="Quality")

        self.create_widgets()
        self.place_widgets()

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)


    def create_widgets(self) -> None:
        self.title_label = ctk.CTkLabel(self, text=self.title, anchor='w')
        self.author_label = ctk.CTkLabel(self, text=self.channel_name, anchor='w')
        self.duration_label = ctk.CTkLabel(self, text=self.duration)
        self.published_date_label = ctk.CTkLabel(self, text=self.published_date)
        self.download_type = ctk.CTkOptionMenu(
            self, 
            variable=self.selected_download_type,
            values=DOWNLOAD_TYPES,
            command=lambda download_type: self.update_mime_types(download_type)
            )
        self.download_mime_type = ctk.CTkOptionMenu(
            self, 
            variable=self.selected_mime_type, 
            values=self.mime_types,
            command=lambda download_mime_type: self.update_download_quality(download_mime_type)
            )
        self.download_quality = ctk.CTkOptionMenu(
            self, 
            variable=self.selected_download_quality, 
            values=self.download_quality,
            command=lambda download_quality: self.filter_streams(download_quality)
            )
        
    def place_widgets(self) -> None:
        self.title_label.grid(row=0, column=0, columnspan=3, sticky='nsew', padx=(10, 5))
        self.author_label.grid(row=1, column=0, sticky='nsew', padx=(10, 5))
        self.duration_label.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)
        self.published_date_label.grid(row=1, column=2, sticky='nsew', padx=5, pady=5)
        self.download_type.grid(row=2, column=0, padx=5, pady=5)
        self.download_mime_type.grid(row=2, column=1, padx=5, pady=5)
        self.download_quality.grid(row=2, column=2, padx=5, pady=5)

    def update_mime_types(self, download_type: str) -> None:
        self.selected_mime_type.set("Mime Type")
        self.selected_download_quality.set("Quality")
        self.download_frame.download_button.configure(state=tk.DISABLED)
        self.download_frame.download_button.update()
        self.download_streams = get_streams(download_type, self.streams)
        self.mime_types = get_mime_types(self.download_streams)
        self.download_mime_type.configure(values=self.mime_types)
        self.download_mime_type.update()

    def update_download_quality(self, download_mime_type: str) -> None:
        self.selected_download_quality.set("Quality")
        self.download_frame.download_button.configure(state=tk.DISABLED)
        self.download_frame.download_button.update()
        if 'video' in download_mime_type:
            self.download_quality.configure(values=get_resolution(download_mime_type, self.download_streams))
            self.download_quality.update()
        elif 'audio' in download_mime_type or download_mime_type == 'mp3':
            self.download_quality.configure(values=get_abr(download_mime_type, self.download_streams))
            self.download_quality.update()
        else:
            return
        
    def filter_streams(self, download_quality: str) -> None:
        mime_type = self.selected_mime_type.get()
        download_type = self.selected_download_type.get()
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
        self.search_seconds = end_time - start_time

        self.filesize = get_formatted_size(self.filtered_stream.filesize)
        self.download_frame.filesize.set(self.filesize)

        self.download_frame.download_button.configure(state=tk.NORMAL)
        self.download_frame.download_button.update()


class DownloadFrame(ctk.CTkFrame):
    def __init__(self, parent: tk.Tk, yt: pytube.YouTube, *args, **kwargs) -> None:

        super().__init__(parent, *args, **kwargs)

        self.app = parent
        self.yt = yt
        self.title = self.yt.title
        self.channel_name = self.yt.author
        self.duration = get_formatted_time(self.yt.length)
        self.published_date = get_formatted_published_date(self.yt)
        self.filesize = ctk.StringVar(self, value="File Size")

        self.thumbnail_url = self.yt.thumbnail_url
        with urllib.request.urlopen(self.thumbnail_url) as u:
            raw_data = u.read()
        self.img = Image.open(io.BytesIO(raw_data))
        self.thumbnail_image = ctk.CTkImage(light_image=self.img, dark_image=self.img, size=(180, 120))

        self.create_widgets()
        self.place_widgets()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)

        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)

        self.pack(side='bottom', expand=False, padx=20, pady=(5, 30))

    def create_widgets(self) -> None:
        self.thumbnail_label = ctk.CTkLabel(self, text="", image=self.thumbnail_image)
        self.video_details_frame = VideoDetailsFrame(self, yt=self.yt)
        self.download_size_label = ctk.CTkLabel(self, textvariable=self.filesize, text="")
        self.download_button = ctk.CTkButton(self, text="Download", fg_color="red", state=tk.DISABLED, command=self.download)

    def place_widgets(self) -> None:
        self.thumbnail_label.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.video_details_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.download_size_label.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        self.download_button.grid(row=1, column=1, sticky='nsew', padx=5, pady=5)

    def update_progress(self, stream: pytube.Stream, chunk: bytes, bytes_remaining: int) -> None:
        total_bytes = stream.filesize
        downloaded_bytes = total_bytes - bytes_remaining
        download_percentage = (downloaded_bytes / total_bytes) * 100
        self.progress_frame.progressbar.set(float(download_percentage / 100))
        progress_text = f"{int(download_percentage)} % ({get_formatted_size(downloaded_bytes)}/{get_formatted_size(total_bytes)})"
        self.progress_frame.progress_label.configure(text=progress_text)
        self.progress_frame.progress_label.update()

    @classmethod
    def get_download_location(cls, file_name: str) -> str:
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
                download_path = cls.get_download_location(file_name)
                return download_path
            
            else:
                return
        else:
            return download_path

    def download(self) -> None:
        try:
            mime_type = self.video_details_frame.selected_mime_type.get()
            file_name = f'{self.yt.title}.{mime_type.split("/")[-1]}'

            download_path = self.get_download_location(file_name)
            if not download_path:
                return

            self.progress_frame = ProgressFrame(app, fg_color='transparent')
            self.progress_frame.video_title_label.configure(text=self.title)
            self.progress_frame.video_title_label.update()

            # download stream
            self.progress_frame.progressbar.set(0)
            start_time = timeit.default_timer()
            self.video_details_frame.filtered_stream.download(output_path=download_path, filename=file_name)
            end_time = timeit.default_timer()
            self.progress_frame.progressbar.set(1)

            # update progress label
            self.progress_frame.progress_label.configure(text="100 %")
            self.progress_frame.progress_label.update()

            download_seconds = end_time - start_time
            download_time = get_formatted_time(self.video_details_frame.search_seconds + download_seconds)
            ctkmb.CTkMessagebox(title=SUCCESS, message=DOWNLOAD_SUCCESS.format(download_path, download_time))

        except RegexMatchError:
            ctkmb.CTkMessagebox(title=ERROR, message=INVALID_VIDEO_ID, icon=ICON_CANCEL)

        except Exception as exception:
            ctkmb.CTkMessagebox(title=ERROR, message=exception, icon=ICON_CANCEL)



if __name__ == "__main__":

    ROOT_FOLDER = Path(__file__).resolve().parent

    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)

    app = App()

    app.mainloop()
