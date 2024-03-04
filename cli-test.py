import argparse
from pytube import YouTube
from pytube.cli import on_progress
from pytube.exceptions import VideoUnavailable

def download_video(url, rename, audio_only, quality, silent):
    try:
        yt = YouTube(url, on_progress_callback=None if silent else on_progress)
    except VideoUnavailable:
        print("The provided URL is not a valid YouTube video link.")
        return

    if audio_only:
        stream = yt.streams.get_audio_only()
    else:
        if quality == 'Hq':
            stream = yt.streams.get_highest_resolution()
        elif quality == 'Lq':
            stream = yt.streams.get_lowest_resolution()
        else:
            stream = yt.streams.get_highest_resolution()

    print(f"Downloading: {yt.title}")
    stream.download(filename=rename)
    print("Download completed!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='YouTube Video Downloader',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('url', help='URL of the YouTube video')
    parser.add_argument('-r', '--rename', default=None, help='Rename the downloaded video')
    parser.add_argument('-a', '--audio', action='store_true', help='Download audio only')
    parser.add_argument('-q', '--quality', choices=['Hq', 'Lq'], default='Hq', help='Quality of the video (default: highest quality)')
    parser.add_argument('-s', '--silent', action='store_true', help='Silence the printouts')

    args = parser.parse_args()
    download_video(args.url, args.rename, args.audio, args.quality, args.silent)
