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