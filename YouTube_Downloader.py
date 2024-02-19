import customtkinter
from pytube import YouTube
'''
#TODO add audio-function, add auto-find downloads-folder independent of platform, add playlist functionality
#TODO customize Interface, add progress bar, add download finished message, add button press feedback?
'''
#* function to download a YT Video in highest res available
def DownloadYouTubeVideo(video_url):
    vid  = YouTube(video_url)
    # Get the highest resolution stream available
    stream = vid.streams.get_highest_resolution()
    # Download the video to the specified output path
    stream.download(output_path="/Users/jhecker/Downloads")   
    
#* function to download only Audio from a video
def DownloadYouTubeAudio(video_url):
    url  = YouTube(video_url)

# ! initialize app window and set dimensions and Title
app = customtkinter.CTk()
app.title("Test Program")
app.geometry("700x500")

#* add TextBox where user inputs YT-Link
my_entry = customtkinter.CTkEntry(app,placeholder_text="Enter YouTube Link", width=660)
my_entry.grid(row=0, column=0, padx=20, pady=20)

#* add Button in a grid that executes DownloadYouTubeVideo function when pressed
button = customtkinter.CTkButton(app, text="Download Video", command=lambda: DownloadYouTubeVideo(my_entry.get()))
button.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

#* add Button to download only MP3
button2 = customtkinter.CTkButton(app, text="Download Audio", command=lambda: DownloadYouTubeAudio(my_entry.get()))
button2.grid(row=2, column=0, padx=20, pady=10, sticky="ew")



# ! keeps window open until its closed
app.mainloop()

