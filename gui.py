import tkinter as tk
import customtkinter as ctk
import CTkMessagebox as ctkmb
import pytube
import timeit
from utils.helpers import *
from utils.constants import *
from pathlib import Path
from sys import platform


SCRIPT_PATH = Path(__file__).resolve().parent

def download_video(url):
    try:
        start_time = timeit.default_timer()
        yt = pytube.YouTube(url)
        stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
        end_time = timeit.default_timer()
        search_seconds = end_time - start_time
        download_path = tk.filedialog.askdirectory()
        if not download_path:
            ctkmb.CTkMessagebox(title=CANCELLED, message=DOWNLOAD_CANCELLED, icon="warning", option_1="Close")
            return
        start_time = timeit.default_timer()
        stream.download(download_path)
        end_time = timeit.default_timer()
        download_seconds = end_time - start_time
        download_time = convert_download_time(search_seconds + download_seconds)
        ctkmb.CTkMessagebox(title=SUCCESS, message=DOWNLOAD_SUCCESS.format(download_path, download_time))
    except pytube.exceptions.RegexMatchError:
        ctkmb.CTkMessagebox(title=ERROR, message=INVALID_VIDEO_ID, icon="cancel")
    except Exception as e:
        ctkmb.CTkMessagebox(title=ERROR, message=e, icon="cancel")

def search_url():
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
            self.icon_path = SCRIPT_PATH.joinpath("images/icons/ico/icon1.ico")
            self.wm_iconbitmap(bitmap = self.icon_path)
        else:
            self.icon_path = SCRIPT_PATH.joinpath("images/icons/xbm/icon1.xbm")
            self.wm_iconbitmap(bitmap = self.icon_path)

if __name__ == "__main__":

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = App()

    url_entry_label = ctk.CTkLabel(app, text="Enter the Youtube video link below:")
    url_entry_label.grid(row=0, column=0, sticky='s')

    url_entry = ctk.CTkEntry(app, width=400)
    url_entry.grid(row=1, column=0, padx=5)

    search_button = ctk.CTkButton(app, text="Download", command=search_url, anchor='n')
    search_button.grid(row=2, column=0, pady=(5, 0), sticky='n')

    app.grid_columnconfigure(0, weight=1)
    app.grid_rowconfigure(0, weight=1)
    app.grid_rowconfigure(2, weight=5)

    app.mainloop()
