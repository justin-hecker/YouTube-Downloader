import subprocess
import customtkinter
import os
from sys import platform as sys_platform  # Renaming the imported platform module
from pytube import YouTube
from pytube import Playlist
from tkinter import filedialog
'''
#TODO add video counter for playlist dloading
#TODO customize Interface, make buttons smaller and next to eachother
'''
global DOWNLOAD_FOLDER

#? function to determine downloadsfolder of device
def Find_Download_Folder():
    global DOWNLOAD_FOLDER
    # Initialize download folder to default location
    if sys_platform == "win32":  # Windows
        DOWNLOAD_FOLDER = os.path.join(os.environ.get('USERPROFILE'), 'Downloads')
    elif sys_platform == "darwin":  # macOS
        DOWNLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')
    elif sys_platform.startswith('linux'):  # Linux
        DOWNLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'Downloads')
    else:
        DOWNLOAD_FOLDER = None  # Unsupported platform

#* function to allow changing of install location
def change_download_location():
    global DOWNLOAD_FOLDER
    new_download_folder = filedialog.askdirectory()
    DOWNLOAD_FOLDER = new_download_folder
    percentage_label.configure(text="Save Location set!")

#* function to download a YT Video in highest res available
def DownloadYouTubeVideo(video_url):
    try:
        # reset Progressbar in case of multiple downloads
        progressbar.set(0)
        progressbar.update()
        # get video details
        vid = YouTube(video_url, on_progress_callback=on_progress)
        # Get the highest resolution stream available
        stream = vid.streams.get_highest_resolution()
        # Sanitize the video title to remove invalid characters
        sanitized_title = "".join(x for x in vid.title if x.isalnum() or x in (' ', '.', '_', '-'))
        # Download the video to the specified output path
        file_path = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}.mp4")
        #stream.download(filename=f"{vid.title}.mp4", output_path=DOWNLOAD_FOLDER) 
        stream.download(filename=file_path)
    except:
        #TODO ADD display invalid link! (make sure its a valid YT Link, and not age restricted)
        percentage_label.configure(text="Invalid link (make sure its a valid YT Link, and the Video is not age restricted)")    
  
#* function to download only Audio from a video
def DownloadYouTubeAudio(video_url):
    try:   
        # reset progressbar in case of multiple downloads
        progressbar.set(0)   
        progressbar.update()
        # get video details
        vid = YouTube(video_url, on_progress_callback=on_progress)
        # filter video to only stream Audio
        stream = vid.streams.filter(only_audio=True).first()
        sanitized_title = "".join(x for x in vid.title if x.isalnum() or x in (' ', '.', '_', '-'))
        # Download the video to the specified output path
        file_path = os.path.join(DOWNLOAD_FOLDER, f"{sanitized_title}.mp3")
        #stream.download(filename=f"{vid.title}.mp3", output_path=DOWNLOAD_FOLDER) 
        stream.download(filename=file_path)
    except:
        percentage_label.configure(text="Invalid link (make sure its a valid YT Link, and the Video is not age restricted)")    
            
#* function to calculate download-percentage
def on_progress(stream, chunk, bytes_remaining):
    # get toal size and remaining bytes from YouTube class from pytube
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    # calculate percentage of download
    percentage_of_completion = bytes_downloaded / total_size * 100
    # convert to string to print out on label
    per = str(int(percentage_of_completion))
    # check if download is finished
    if int(per)>= 100:
        percentage_label.configure(text="Download Complete!")
        percentage_label.update()
        download_complete = True
    else:    
        percentage_label.configure(text="Downloading... (" + per + "%)")
        percentage_label.update()
    
    # update progress bar
    progressbar.set(float(percentage_of_completion)/100)
    progressbar.update()

# function to open save location
def open_file_location():
    try:
        global DOWNLOAD_FOLDER
        if sys_platform == 'win32':  # Checking the value of the platform string
            subprocess.Popen(f'explorer "{os.path.abspath(DOWNLOAD_FOLDER)}"', shell=True)
        elif sys_platform == 'darwin':  # macOS
            subprocess.Popen(['open', DOWNLOAD_FOLDER])
        else:
            print("Unsupported platform")
    except:
        percentage_label.configure(text="Save Location not set yet!")  
        
#* Function to download all Videos in a Playlist
def DownloadPlaylistVideo(playlist_url):
    try:
        # load playlist
        playlist = Playlist(playlist_url)
        # download playlist
        for video in playlist.videos:
            DownloadYouTubeVideo(video.watch_url)
    except:
        percentage_label.configure(text="Downloading Playlist went wrong")
        

#* Function to download all Videos in a Playlist as mp3
def DownloadPlaylistAudio(playlist_url):
    try:
        # load playlist
        playlist = Playlist(playlist_url)
        # download playlist
        for video in playlist.videos:
            DownloadYouTubeAudio(video.watch_url)
    except:
        percentage_label.configure(text="Downloading Playlist went wrong")

# ! initialize app window and set dimensions and Title
app = customtkinter.CTk()
app.title("YouTube Downloader")
app.geometry("700x550")

#* add TextBox where user inputs YT-Link
my_entry = customtkinter.CTkEntry(app, placeholder_text="Click to enter YouTube Link.. (Also dont forget to set Save location with the button below)", width=660,height=45, placeholder_text_color="white")
my_entry.grid(row=0, column=0, padx=20, pady=20)

#* add download-percentage
percentage_label = customtkinter.CTkLabel(app, text="0%", text_color="white")
percentage_label.grid(row=1, column=0, padx=20, pady=0, sticky="ew")

#* add progress-bar to show download progress
progressbar = customtkinter.CTkProgressBar(app, orientation="horizontal",height=20, progress_color="white")
progressbar.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
progressbar.set(0)

#* add Button in a grid that executes DownloadYouTubeVideo function when pressed
button = customtkinter.CTkButton(app, text="Download Video", command=lambda: DownloadYouTubeVideo(my_entry.get()), height=40, fg_color="red", hover_color="orange")
button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

#* add Button to download only MP3
button2 = customtkinter.CTkButton(app, text="Download Audio", command=lambda: DownloadYouTubeAudio(my_entry.get()), height=40, fg_color="red", hover_color="orange")
button2.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

#* add "Open File Location" button
open_file_button = customtkinter.CTkButton(app, text="Open File Location", command=open_file_location, height=40, fg_color="red", hover_color="orange")
open_file_button.grid(row=8, column=0, padx=20, pady=10, sticky="ew")

# Add "Change Download Location" button
change_location_button = customtkinter.CTkButton(app, text="Change Download Location", command=change_download_location, height=40, fg_color="red", hover_color="orange")
change_location_button.grid(row=7, column=0, padx=20, pady=10, sticky="ew")

#* add Button in a grid that executes DownloadPlaylistVideo function when pressed
button = customtkinter.CTkButton(app, text="Download Playlist (Video)", command=lambda: DownloadPlaylistVideo(my_entry.get()), height=40, fg_color="red", hover_color="orange")
button.grid(row=5, column=0, padx=20, pady=10, sticky="ew")

#* add Button to download only MP3
button2 = customtkinter.CTkButton(app, text="Download Playlist (Audio)", command=lambda: DownloadPlaylistAudio(my_entry.get()), height=40, fg_color="red", hover_color="orange")
button2.grid(row=6, column=0, padx=20, pady=10, sticky="ew")

# ! keeps window open until its closed
app.mainloop()

