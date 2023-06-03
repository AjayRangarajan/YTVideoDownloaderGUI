# **YTVideoDownloaderGUI**

###### version 0.1.0

A simple GUI for downloading Youtube videos using Python.

### Dependencies:

* `CTkMessagebox==2.0`
* `customtkinter==5.1.3`
* `pytube==15.0.0`

### Packaging:

`pyinstaller --noconfirm --onedir --windowed --add-data "<path\to\library_1\source;destination>" --add-data "<path\to\library_2\source;destination>" "<gui_file.py>"`

After running the above command, the `.exe` file will be available in the `dist/gui` folder.

### Screenshots

###### App v0.1.0

![App v0.1.0](./images/screenshots/v0.1.0/App_v0.1.0.jpg)

###### Download success message:

![Download success v0.1.0](./images/screenshots/v0.1.0/download_success_v0.1.0.jpg)

###### Download cancelled message:

![Download cancelled v0.1.0](./images/screenshots/v0.1.0/download_cancelled_v0.1.0.jpg)

###### Invalid URL error message:

![Invalid URL error v0.1.0](./images/screenshots/v0.1.0/invalid_url_error_v0.1.0.jpg)

###### Empty URL error message:

![Empty URL error v0.1.0](./images/screenshots/v0.1.0/empty_url_error_v0.1.0.jpg)
