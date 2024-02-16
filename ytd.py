import os
import shutil
from pytube import YouTube

banner = """
░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	
░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	You Tube Downloader
 ░▒▓██████▓▒░   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	X: @vargnaar
   ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	W: https://varghalla.neocities.org
   ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	L: MIT
   ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓███████▓▒░  	C: Sat 17 Feb 2:32am
"""

def progress_function(stream, chunk, bytes_remaining):
    current = ((stream.filesize - bytes_remaining)/stream.filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    print(f' {percent}% [{status}]', end='\r')

def download_video():
    download_folder = "Downloaded Videos"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    while True:
        link = input("Enter link: ")
        try:
            yt = YouTube(link, on_progress_callback=progress_function)
            print("[+] Downloading...\n")
            yt.streams.first().download(download_folder)
            print("\n[+] Download completed.")
        except Exception as e:
            print("[-] An error occurred: ", e)

        print("\n1. Download another video")
        print("2. Exit")
        option = input("[+] Enter your choice (1 or 2): ")
        if option == '2':
            print("[+] Goodbye!\n")
            break

    for file_name in os.listdir():
        if file_name.endswith('.mp4'):
            shutil.move(file_name, download_folder)

print(banner)
download_video()

