import tkinter as tk
import customtkinter as ctk
import CTkMessagebox as ctkmb
import pytube
from helpers import *


APP_VERSION = "v0.1.0"


def download_video(url):
    try:
        yt = pytube.YouTube(url)
        stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
        download_path = tk.filedialog.askdirectory()
        if not download_path:
            ctkmb.CTkMessagebox(title="Cancelled", message="Download Cancelled!", icon="warning", option_1="Close")
            return
        stream.download(download_path)
        ctkmb.CTkMessagebox(title="Success!", message=f"Successfully downloaded the video in the path\n{download_path}")
    except pytube.exceptions.RegexMatchError:
        ctkmb.CTkMessagebox(title="Error!", message="Invalid URL!\nPlease enter a valid URL!", icon="cancel")
    except Exception as e:
        ctkmb.CTkMessagebox(title="Error!", message=e, icon="cancel")

def search_url():
    url = url_entry.get()
    if not url:
        ctkmb.CTkMessagebox(title="Error!", message="Please enter the Youtube video link", icon="cancel")
        return
    if not is_valid_youtube_url(url):
        ctkmb.CTkMessagebox(title="Error!", message="Invalid URL\nPlease enter a valid link!", icon="cancel")
        return
    download_video(url)

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(f"YouTube Video Downloader {APP_VERSION}")
        self.geometry("500x200")

if __name__ == "__main__":

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    app = App()

    url_entry_label = ctk.CTkLabel(app, text="Enter the Youtube video link below:")
    url_entry_label.grid(row=0, column=0, padx=0, pady=(10, 0))

    url_entry = ctk.CTkEntry(app, width=400)
    url_entry.grid(row=1, column=0)

    search_button = ctk.CTkButton(app, text="Download", command=search_url)
    search_button.grid(row=2, column=0, pady=(20, 5))

    app.grid_columnconfigure(0, weight=1)

    app.mainloop()
