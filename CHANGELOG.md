# **YTVideoDownloaderGUI**

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

![Downloading video](images/screenshots/v0.5.5/downloading_video_v0.5.5.png)
---

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
