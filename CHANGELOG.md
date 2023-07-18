# **YTVideoDownloaderGUI**

#### version 0.7.1

> Created a new branch **yt-dlp** & shifted from **pytube** to **yt-dlp** to download video.
> ~~pytube~~ ➡️ **yt-dlp**

##### changes:

* Changed names:
  * **mime_type** is changed as **extension** in download options
  * **published_date** is changed as **upload_date**
  * insted of **streams**, **formats** are used here.
* Changed helper functions.
  * **get_streams()** method is removed and the available formats are returned with the available options in the helper functions.
  * instead of getting resolutions & abr separately,  **get_download_qualities_and_formats()** method is used to get download_qualities with available formats.
  * **get_formatted_upload_date()** method is created to format the upload_date.
* Removed error message for Invalid URL id. It will be shown in general exception message.
* Progressbar is faster now 🔥
* Only download time is calculated not the time taken to extract video info.
* **fetch_video_details()** method is created to check if there is an error when fetching the video details.
* Removed `pytube` from `requirements.txt` file

##### Screenshots

###### Main window:

![Main window](images/screenshots/v0.7.1/main_window_v0.7.1.png)

###### Download options:

![Download options](images/screenshots/v0.7.1/download_options_v0.7.1.png)

###### Downloading video:

![Downloading video](images/screenshots/v0.7.1/downloading_video_v0.7.1.png)

---

#### **version 0.6.2**

> ⚠️ **NOTE:** pytube version `15.0.0` is not working. Use the latest pytube version.

##### changes:

* Added **logging** feature
  * log messages will be added to a file inside the `logs` folder with date in the filename.
  * If the log folder size exceeds above 10MB, it will delete all the contents of the log file.
* Added proper error handling. If any error occurs the funcitons will show the error message and return `None`

---

#### **version 0.6.1**

##### changes:

* filename will be validated before download
* If there is already a file with the same name in the download path, the filename will be changed.
  * User won't be prompted to change directory or delete & overwrite the existing file.
* tag versioning fixed

---

#### **version 0.5.5**

##### changes:

* Add `__init__.py` file inside utils directory and import all the modules in it to make it a package.
* Renamed variables, added more contants & arranged them properly
* Changed button hover color
* Fixed multiple progress bar appearing (when download button clicked multiple times) issue
* Increased the space between the Download frame and Progress frame.
* Disabled window resizing

##### Screenshots

###### Downloading video:

#### **version 0.5.4**

##### changes:

* Refactor the entire code into object oriented.

##### features:

* Added feature to choose the download type (video, audio, video only) with respective file types and quality (resolution/average bitrate)
* Along with the downloaded percentage, (downlaoded size / total file size) will be shown.
* Display thumbnail image.
* Video details like, video title, channel name, video duration, published date will be shown with the download options.
* File size will be displayed once the download options are selected.

##### Screenshots

###### Main window:

![Main window](images/screenshots/v0.5.4/main_window_v0.5.4.png)

###### Download options:

![Download options](images/screenshots/v0.5.4/download_options_v0.5.4.png)

###### Downloading video:

![Downloading video](images/screenshots/v0.5.4/downloading_video_v0.5.4.png)

###### File exists prompt:

![](images/screenshots/v0.4.3/file_exists_prompt_v0.4.3.png)

---

#### **version 0.4.3**

##### features:

* Added function to check if the file is already present in the given download folder path if it is then, prompt the user to continue/cancel or change the download path.

##### Screenshots

###### File exists prompt:

![File exists prompt v0.4.3](images/screenshots/v0.4.3/file_exists_prompt_v0.4.3.png)

---

#### **version 0.3.3**

##### changes:

* Added type hinting
* Code refactoring

##### features:

* Download the highest resolution

---

#### **version 0.3.2**

##### features:

* Added progressbar

##### Screenshots

###### progressbar:

![App v0.3.2](images/screenshots/v0.3.2/progressbar_v0.3.2.png)

---

#### **version 0.2.2**

##### changes:

* changed the app layout

##### Screenshots

###### App v0.2.2

![App v0.2.2](images/screenshots/v0.2.2/App_v0.2.2.png)

---

#### **version 0.2.1**

##### features added:

* Added download time to the success message
* Centered the app window
* Changed the icon

##### Screenshots

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

---

#### version 0.1.0

A simple GUI for downloading Youtube videos using Python.

##### features:

* Downloads single youtube video.
* Show error message if no URL entered or and invalid URL is entered.
* Let the user choose the download location.
* Show success message with download path after the video is downloaded.

##### Screenshots

###### App v0.1.0

![App v0.1.0](./images/screenshots/v0.1.0/App_v0.1.0.png)

###### Download success message:

![Download success v0.1.0](./images/screenshots/v0.1.0/download_success_v0.1.0.png)

###### Download cancelled message:

![Download cancelled v0.1.0](./images/screenshots/v0.1.0/download_cancelled_v0.1.0.png)

###### Invalid URL error message:

![Invalid URL error v0.1.0](./images/screenshots/v0.1.0/invalid_url_error_v0.1.0.png)

###### Empty URL error message:

![Empty URL error v0.1.0](./images/screenshots/v0.1.0/empty_url_error_v0.1.0.png)
