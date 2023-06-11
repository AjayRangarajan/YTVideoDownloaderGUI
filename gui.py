import timeit
import tkinter as tk
from pathlib import Path
from sys import platform

import pytube
from pytube.exceptions import RegexMatchError
import customtkinter as ctk
import CTkMessagebox as ctkmb

from utils.constants import *
from utils.helpers import *


ROOT_FOLDER = Path(__file__).resolve().parent


def update_progress(stream: pytube.Stream, chunk: bytes, bytes_remaining: int) -> None:
    total_bytes = stream.filesize
    downloaded_bytes = total_bytes - bytes_remaining
    download_percentage = (downloaded_bytes / total_bytes) * 100
    progressbar.set(float(download_percentage / 100))
    progress_label.configure(text=f"{int(download_percentage)} %")
    progress_label.update()

def get_download_location(file_name: str) -> str:
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
            download_path = get_download_location(file_name)
            return download_path
        
        else:
            return
    else:
        return download_path


def download_video(url: str) -> None:
    try:

        # fetch stream
        start_time = timeit.default_timer()
        yt = pytube.YouTube(url, on_progress_callback=update_progress)
        stream = yt.streams.filter(file_extension="mp4", progressive=True).get_highest_resolution()
        end_time = timeit.default_timer()
        search_seconds = end_time - start_time

        #update video title
        video_title = stream.title
        file_name = f"{video_title}.mp4"
        download_path = get_download_location(file_name)
        if not download_path:
            return
        video_title_label.configure(text=video_title)
        video_title_label.grid(row=3, column=0)
        video_title_label.update()

        # create progress label
        progress_label.grid(row=4, column=0)
        # create progress bar
        progressbar.grid(row=5, column=0, sticky="n")
        app.update()

        progressbar.set(0)
        start_time = timeit.default_timer()
        stream.download(output_path=download_path, filename=file_name)
        end_time = timeit.default_timer()
        progressbar.set(1)

        # update progress label
        progress_label.configure(text="100 %")
        progress_label.update()

        download_seconds = end_time - start_time
        download_time = convert_download_time(search_seconds + download_seconds)
        ctkmb.CTkMessagebox(title=SUCCESS, message=DOWNLOAD_SUCCESS.format(download_path, download_time))

    except RegexMatchError:
        ctkmb.CTkMessagebox(title=ERROR, message=INVALID_VIDEO_ID, icon="cancel")

    except Exception as exception:
        ctkmb.CTkMessagebox(title=ERROR, message=exception, icon="cancel")


def search_url() -> None:

    # reset video title label
    video_title_label.configure(text="")
    # reset progressbar to 0
    progressbar.set(0)
    # reset progress label to 0 %
    progress_label.configure(text="0 %")
    progress_label.update()

    url = url_entry.get()
    if not url:
        ctkmb.CTkMessagebox(title=ERROR, message=EMPTY_URL_INPUT, icon="cancel")
        return
    if not is_valid_youtube_url(url):
        ctkmb.CTkMessagebox(title=ERROR, message=INVALID_URL, icon="cancel")
        return
    download_video(url)


class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(f"YouTube Video Downloader GUI {APP_VERSION}")
        x, y = calculate_center(self, APP_WIDTH, APP_HEIGHT)
        self.geometry(APP_GEOMETRY.format(APP_WIDTH, APP_HEIGHT, x, y))
        if platform.startswith("win"):
            self.icon_path = ROOT_FOLDER.joinpath("images/icons/ico/icon1.ico")
            self.wm_iconbitmap(bitmap=self.icon_path)
        else:
            self.icon_path = ROOT_FOLDER.joinpath("images/icons/xbm/icon1.xbm")
            self.wm_iconbitmap(bitmap=self.icon_path)


if __name__ == "__main__":

    ctk.set_appearance_mode(APPEARANCE_MODE)
    ctk.set_default_color_theme(COLOR_THEME)

    app = App()

    url_entry_label = ctk.CTkLabel(app, text="Enter the Youtube video link below:")
    url_entry_label.grid(row=0, column=0, sticky="s")

    url_entry = ctk.CTkEntry(app, width=400)
    url_entry.grid(row=1, column=0, padx=5)

    # app.focus()
    # url_entry.focus()

    search_button = ctk.CTkButton(app, text="Download", command=search_url)
    search_button.grid(row=2, column=0, pady=(5, 0), sticky="n")

    video_title_label = ctk.CTkLabel(app, text="")

    progress_label = ctk.CTkLabel(app, text="0 %")

    progressbar = ctk.CTkProgressBar(app, orientation="horizontal", mode="determinate")

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)
    app.grid_rowconfigure(2, weight=4)
    app.grid_rowconfigure(5, weight=7)

    app.mainloop()
