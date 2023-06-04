# **YTVideoDownloaderGUI**

###### version 0.2.1

A simple GUI for downloading Youtube videos using Python.

### Release notes:

Refer [release_notes.md](release_notes.md) for release notes.

### Dependencies:

* `CTkMessagebox==2.0`
* `customtkinter==5.1.3`
* `pytube==15.0.0`

Refer [requirements.txt](requirements.txt) for complete list of dependencies.

### Packaging:

`pyinstaller --noconfirm --onedir --windowed --add-data "<path\to\library_1\source;destination>" --add-data "<path\to\library_2\source;destination>" "<gui_file.py>"`

After running the above command, the `.exe` file will be available in the `dist/gui` folder.

### Screenshots

###### App v0.2.1

![App v0.2.1](images/screenshots/v0.2.1/App_v0.2.1.png)

###### Download success message:

![Download success v0.2.1](images/screenshots/v0.2.1/download_success_v0.2.1.png)

###### Download cancelled message:

![Download cancelled v0.2.1](images/screenshots/v0.2.1/download_cancelled_v0.2.1.png)

###### Invalid URL error message:

![Invalid URL error v0.2.1](images/screenshots/v0.2.1/invalid_url_error_v0.2.1.png)

###### Invalid video id error message:

![Invalid URL error v0.2.1](images/screenshots/v0.2.1/invalid_video_id_error_v0.2.1.png)

###### Empty URL error message:

![Empty URL error v0.2.1](images/screenshots/v0.2.1/empty_url_error_v0.2.1.png)
