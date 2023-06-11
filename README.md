# **YTVideoDownloaderGUI**

![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)  ![Latest Tag](https://img.shields.io/github/v/tag/AjayRangarajan/YTVideoDownloaderGUI)  ![Total Commits](https://img.shields.io/github/commit-activity/t/AjayRangarajan/YTVideoDownloaderGUI)  ![Last commit](https://img.shields.io/github/last-commit/AjayRangarajan/YTVideoDownloaderGUI)  ![Repo size](https://img.shields.io/github/repo-size/AjayRangarajan/YTVideoDownloaderGUI)

###### version 0.3.3

A simple GUI for downloading Youtube videos using Python.

### Release notes:

Refer [CHANGELOG.md](CHANGELOG.md) for release notes.

### Dependencies:

* `CTkMessagebox==2.0`
* `customtkinter==5.1.3`
* `pytube==15.0.0`

Refer [requirements.txt](requirements.txt) for complete list of dependencies.

### Packaging:

`pyinstaller --noconfirm --onedir --windowed --add-data "<path\to\library_1\source;destination>" --add-data "<path\to\library_2\source;destination>" "<gui_file.py>"`

After running the above command, the `.exe` file will be available in the `dist/gui` folder.

### Screenshots

###### App v0.2.2

![App v0.2.2](images/screenshots/v0.2.2/App_v0.2.2.png)

###### Download success message:

![Download success v0.2.1](images/screenshots/v0.2.1/download_success_v0.2.1.png)

###### progressbar:

![Progressbar v0.3.2](images/screenshots/v0.3.2/progressbar_v0.3.2.png)

###### Download cancelled message:

![Download cancelled v0.2.1](images/screenshots/v0.2.1/download_cancelled_v0.2.1.png)

###### Invalid URL error message:

![Invalid URL error v0.2.1](images/screenshots/v0.2.1/invalid_url_error_v0.2.1.png)

###### Invalid video id error message:

![Invalid URL error v0.2.1](images/screenshots/v0.2.1/invalid_video_id_error_v0.2.1.png)

###### Empty URL error message:

![Empty URL error v0.2.1](images/screenshots/v0.2.1/empty_url_error_v0.2.1.png)
