import customtkinter
from pytube import YouTube
'''
#TODO add auto-find downloads-folder independent of platform, add playlist functionality
#TODO customize Interface
#TODO make app executable independent of platform, error handling if link is wrong
#TODO 
'''
#? function to determine downloadsfolder of device
def Find_Download_Folder():
    print("Placeholder")


#* function to download a YT Video in highest res available
def DownloadYouTubeVideo(video_url):
    # reset Progressbar in case of multiple downloads
    progressbar.set(0)
    progressbar.update()
    # get video details
    vid = YouTube(video_url, on_progress_callback=on_progress)
    # Get the highest resolution stream available
    stream = vid.streams.get_highest_resolution()
    # Download the video to the specified output path
    stream.download(filename=f"{vid.title}.mp4", output_path="/Users/jhecker/Downloads") 
    
#* function to download only Audio from a video
def DownloadYouTubeAudio(video_url):
    # reset progressbar in case of multiple downloads
    progressbar.set(0)   
    progressbar.update()
    # get video details
    vid = YouTube(video_url, on_progress_callback=on_progress)
    # filter video to only stream Audio
    stream = vid.streams.filter(only_audio=True).first()
    # Download Audio file
    stream.download(filename=f"{vid.title}.mp3", output_path="/Users/jhecker/Downloads")

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
    else:    
        percentage_label.configure(text="Downloading... (" + per + "%)")
        percentage_label.update()
    
    # update progress bar
    progressbar.set(float(percentage_of_completion)/100)
    progressbar.update()


# ! initialize app window and set dimensions and Title
app = customtkinter.CTk()
app.title("YouTube Downloader")
app.geometry("700x500")

#* add TextBox where user inputs YT-Link
my_entry = customtkinter.CTkEntry(app, placeholder_text="Click to enter YouTube Link..", width=660,height=45, placeholder_text_color="white")
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



# ! keeps window open until its closed
app.mainloop()

