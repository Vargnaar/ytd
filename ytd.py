import os
import shutil
from pytube import YouTube, Playlist
from urllib.parse import urlparse, parse_qs
from colorama import Fore, Back, Style

def print_colored_banner():
    banner = """
    ░▒▓█▓▒░░▒▓█▓▒░▒▓████████▓▒░▒▓███████▓▒░  
    ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	
    ░▒▓█▓▒░░▒▓█▓▒░  ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	
     ░▒▓██████▓▒░   ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	
       ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 	
       ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓█▓▒░░▒▓█▓▒░ 
       ░▒▓█▓▒░      ░▒▓█▓▒░   ░▒▓███████▓▒░  
    """

    for line in banner.split('\n'):
        for char in line:
            if char == '█':
                print(Fore.WHITE + char, end='')
            else:
                print(Fore.RED + char, end='')
            print(Style.RESET_ALL, end='')
        print()

print(f"\nTwitter: {Back.LIGHTBLUE_EX}{Fore.WHITE}@Vargnaar{Style.RESET_ALL}")
print(f"Website: {Back.BLUE}{Fore.WHITE}https://varghalla.neocities.org{Style.RESET_ALL}")
print(f"Created: {Back.LIGHTBLUE_EX}{Fore.WHITE}Sat Feb 17 2024 | 2:32am{Style.RESET_ALL}")

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

def file_exists(folder, filename):
    return os.path.isfile(os.path.join(folder, filename))

def get_unique_filename(folder, filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    while file_exists(folder, filename):
        filename = f"{base}_{counter}{ext}"
        counter += 1
    return filename

def download_video_or_audio(yt, folder, stream, filename=None):
    print(f"\n[{Fore.LIGHTYELLOW_EX}+{Style.RESET_ALL}] {Fore.LIGHTYELLOW_EX}Downloading{Style.RESET_ALL}")
    if filename:
        # Set the 'outtmpl' option to our filename
        yt.register_on_complete_callback(lambda stream, file: os.rename(file, os.path.join(folder, filename)))
    stream.download(folder)
    print(f"[{Fore.GREEN}+{Style.RESET_ALL}] {Fore.GREEN}Download completed.{Style.RESET_ALL}")

def get_stream(yt, download_option):
    if download_option == '1':
        # Get all available streams for the video
        streams = yt.streams.filter(progressive=True)
    elif download_option == '2':
        streams = yt.streams.filter(only_audio=True)
    else:
        print(f"{Back.BLACK}{Fore.RED}Invalid option, try again.{Style.RESET_ALL}")
        return None, None

    # Display all available streams and let the user choose
    print("\nAvailable qualities:")
    for i, stream in enumerate(streams, 1):
        print(f"{i}. {stream.resolution}")
    stream_number = int(input("Which version do you want?: "))
    chosen_stream = streams[stream_number - 1]

    # Calculate the download size in MB
    download_size = chosen_stream.filesize / (1024 * 1024)
    print(f"The download size is {download_size:.2f} MB")

    filename = f"{yt.title}.{chosen_stream.subtype}"
    return chosen_stream, filename

def handle_download(yt, folder, download_option, filename=None):
    chosen_stream, filename = get_stream(yt, download_option)
    if chosen_stream is None:
        return

    filename = get_unique_filename(folder, filename)

    if filename in os.listdir(folder):
        print(f"{Fore.MAGENTA}This video has already been downloaded{Style.RESET_ALL}.")
        download_choice = get_user_choice("What would you like to do?", ["Download anyway", "Try a new video"])
        if download_choice == '2':
            return

    download_video_or_audio(yt, folder, chosen_stream, filename)

def download_video():
    video_folder = "Downloaded Videos"
    audio_folder = "Downloaded Audio"
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    while True:
        link = input("Enter link: ")
        parsed_url = urlparse(link)
        if not all([parsed_url.scheme, parsed_url.netloc, parsed_url.path]):
            print("Invalid URL. Please enter a valid YouTube link.")
            continue

        query = parse_qs(parsed_url.query)
        if 'list' in query:
            print("This is a playlist link. Do you want to download the entire playlist?")
            option = get_user_choice("", ["Yes", "No"])
            if option == '1':
                pl = Playlist(link)
                for url in pl.video_urls:
                    try:
                        yt = YouTube(url, on_progress_callback=progress_function)
                        print(f"Video title: {yt.title}")
                        download_option = get_user_choice("Do you want to download:", ["Full video with audio", "Only audio"])
                        folder = os.path.join(video_folder if download_option == '1' else audio_folder, pl.title)
                        if not os.path.exists(folder):
                            os.makedirs(folder)
                        handle_download(yt, folder, download_option)
                    except Exception as e:
                        print(f"An error occurred while downloading video at {url}: {e}")
                continue
            elif option == '2':
                continue

        try:
            yt = YouTube(link, on_progress_callback=progress_function)
            print(f"\nVideo title: {Back.LIGHTGREEN_EX}{yt.title}{Style.RESET_ALL}")
            option = get_user_choice("Is this the correct video?", ["Yes - Download it", "Yes - Download and rename", "No - Try again", "Exit"])
            if option == '1':
                download_option = get_user_choice("\nDo you want to download:", ["Full video with audio", "Only audio"])
                folder = video_folder if download_option == '1' else audio_folder
                handle_download(yt, folder, download_option)
            elif option == '2':
                new_name = input("Enter the new name for the video: ")
                download_option = get_user_choice("\nDo you want to download:", ["Full video with audio", "Only audio"])
                folder = video_folder if download_option == '1' else audio_folder
                handle_download(yt, folder, download_option, new_name)
            elif option == '4':
                print("[+] Goodbye!\n")
                break
        except Exception as e:
            print(f"[{Fore.RED}-{Style.RESET_ALL}] {Fore.RED}An error occurred{Style.RESET_ALL}: ", e)

        option = get_user_choice("\nWhat would you like to do next?", ["Download another video", "Exit"])
        if option == '2':
            print("\n[+] Goodbye!\n")
            break

    for file_name in os.listdir():
        if file_name.endswith('.mp4'):
            shutil.move(file_name, video_folder)
        elif file_name.endswith('.mp3'):
            shutil.move(file_name, audio_folder)

print_colored_banner()
download_video()
