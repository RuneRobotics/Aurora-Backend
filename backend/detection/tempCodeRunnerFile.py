def download_youtube_video(url: str, download_path: str):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension='mp4', res="720p").first()
        if not stream:
            stream = yt.streams.filter(file_extension='mp4').first()
        
        if not stream:
            print("Error: No valid stream found.")
            return None
        
        output_file = stream.download(output_path=download_path)
        return output_file

    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        return None
