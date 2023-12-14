# **YTVideoDownloaderGUI**

![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)  ![Latest Tag](https://img.shields.io/github/v/tag/AjayRangarajan/YTVideoDownloaderGUI)  ![Total Commits](https://img.shields.io/github/commit-activity/t/AjayRangarajan/YTVideoDownloaderGUI)  ![Last commit](https://img.shields.io/github/last-commit/AjayRangarajan/YTVideoDownloaderGUI)  ![Repo size](https://img.shields.io/github/repo-size/AjayRangarajan/YTVideoDownloaderGUI)

A GUI for downloading Youtube videos using Python.

## Features:

* Downloads YouTube video in any available format with high quality.
* Allows user to choose the download location.
* Shows progress of the download.
* Choose download type (video, audio, video only) with respective file types and quality (resolution/average bitrate)
* Added logging feature.

### Release notes:

Refer [CHANGELOG.md](CHANGELOG.md) for release notes.

### Dependencies:

* `CTkMessagebox`
* `customtkinter`
* `yt-dlp`
* `Pillow`
* `python-dotenv`

Refer [requirements.txt](requirements.txt) for complete list of dependencies.

### Environment variables:

* All environment variables are mentioned in the *env.sample* file.
* Environment variables can also be stored in a *.env* file.
* If environment variables are not available, no errors will be shown instead default values will be taken.

### Packaging:

`pyinstaller --noconfirm --onedir --windowed --add-data "<path\to\library_1\source;destination>" --add-data "<path\to\library_2\source;destination>" "<gui_file.py>"`

After running the above command, the `.exe` file will be available in the `dist/gui` folder.

### Screenshots

###### Main window:

![Main window](images/screenshots/v0.7.1/main_window_v0.7.1.png)

###### Download options:

![Download options](images/screenshots/v0.7.1/download_options_v0.7.1.png)

###### Downloading video:

![Downloading video](images/screenshots/v0.7.1/downloading_video_v0.7.1.png)

###### Download success message:

![Download success](images/screenshots/v0.2.1/download_success_v0.2.1.png)

###### Download cancelled message:

![Download cancelled](images/screenshots/v0.2.1/download_cancelled_v0.2.1.png)

###### Invalid URL error message:

![Invalid URL error](images/screenshots/v0.2.1/invalid_url_error_v0.2.1.png)

###### Empty URL error message:

![Empty URL error](images/screenshots/v0.2.1/empty_url_error_v0.2.1.png)
