import os
import shutil
from pytube import YouTube

def print_banner():
    banner = """
░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░  
░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	You Tube Downloader
░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	I was up making burger buns
 ░▒▓██████▓▒░   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	X: @vargnaar
   ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	W: https://varghalla.neocities.org
   ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	L: MIT
   ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓███████▓▒░  	C: Sat 17 Feb 2:32am
"""
    print(banner)

def progress_function(stream, chunk, bytes_remaining):
    current = ((stream.filesize - bytes_remaining)/stream.filesize)
    percent = ('{0:.1f}').format(current*100)
    progress = int(50*current)
    status = '█' * progress + '-' * (50 - progress)
    print(f' {percent}% [{status}]', end='\r')

def get_user_choice(prompt, options):
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    choice = input("Enter your choice: ")
    return choice

def download_video_or_audio(yt, folder, stream):
    print("[+] Downloading")
    stream.download(folder)
    print("\n[+] Download completed.")

def handle_download(yt, folder, download_option):
    if download_option == '1':
        stream = yt.streams.first()
        filename = f"{yt.title}.mp4"
    elif download_option == '2':
        stream = yt.streams.filter(only_audio=True).first()
        filename = f"{yt.title}.mp3"
    else:
        print("Invalid option. Try again.")
        return

    if filename in os.listdir(folder):
        print("This video has already been downloaded.")
        download_choice = get_user_choice("What would you like to do?", ["Download anyway", "Try a new video"])
        if download_choice == '2':
            return

    download_video_or_audio(yt, folder, stream)

def download_video():
    video_folder = "Downloaded Videos"
    audio_folder = "Downloaded Audio"
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    while True:
        link = input("Enter link: ")
        try:
            yt = YouTube(link, on_progress_callback=progress_function)
            print(f"Video title: {yt.title}")
            option = get_user_choice("Is this the correct video?", ["Yes - Download it", "No - Try again", "Exit"])
            if option == '1':
                download_option = get_user_choice("Do you want to download:", ["Full video with audio", "Only audio"])
                folder = video_folder if download_option == '1' else audio_folder
                handle_download(yt, folder, download_option)
            elif option == '3':
                print("[+] Goodbye!\n")
                break
        except Exception as e:
            print("[-] An error occurred: ", e)

        option = get_user_choice("\nWhat would you like to do next?", ["Download another video", "Exit"])
        if option == '2':
            print("[+] Goodbye!\n")
            break

    for file_name in os.listdir():
        if file_name.endswith('.mp4'):
            shutil.move(file_name, video_folder)
        elif file_name.endswith('.mp3'):
            shutil.move(file_name, audio_folder)

print_banner()
download_video()
