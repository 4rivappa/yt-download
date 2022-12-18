import datetime
import re
import traceback
from pytube import YouTube
from pytube.cli import on_progress
import ffmpeg
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--ignore-certificate-errors-spki-list')
options.add_argument("--log-level=3")
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")

chrome_driver = r"C:/users/arivappa/documents/seleniumDrivers/chromedriver_108.exe"
ser = Service(chrome_driver)
driver = webdriver.Chrome(service=ser, options=options)
# driver = webdriver.Chrome(executable_path=chrome_driver, options=options)

# link = "https://www.youtube.com/watch?v=tyB0ztf0DNY"

def download_video(video_link):
    video = YouTube(video_link, on_progress_callback=on_progress)
    print(video.title)

    video_stream = video.streams.filter(mime_type="video/mp4", type="video", res="1080p")
    audio_stream = video.streams.filter(mime_type="audio/mp4", type="audio", abr="128kbps")

    if os.path.exists('video.mp4'):
        os.remove('video.mp4')
    if os.path.exists('audio.mp4'):
        os.remove('audio.mp4')
    video_stream[0].download('.', 'video.mp4')
    audio_stream[0].download('.', 'audio.mp4')

    video_ffmpeg = ffmpeg.input('video.mp4')
    audio_ffmpeg = ffmpeg.input('audio.mp4')

    # final_file_path = folder_path + video.title + ".mp4"
    final_file_path = str(video.title)
    final_file_path.replace("|", " ")
    final_file_path.replace("  ", " ")
    final_file_path.replace(" ", "-")

    print(final_file_path)
    final_file_path = re.sub('[^A-Za-z0-9\s]+', '', final_file_path)

    ffmpeg.output(audio_ffmpeg, video_ffmpeg, "./devaslife-yt/" + final_file_path + ".mp4", codec='copy').run()


# download_video(link , "D:\\content\\striver-dp-series\\")

def get_playlist(playlist_link):
    file = open('playlist-videos.txt', 'w', encoding='utf-8')
    driver.get(playlist_link)
    time.sleep(8)
    innerHTML = driver.page_source
    soup = BeautifulSoup(innerHTML, 'html.parser')
    # print(soup)
    for div in soup.find_all('ytd-playlist-panel-video-renderer'):
        # print("Div")
        a_tag = div.find('a')
        link = a_tag['href']
        complete_link = "https://www.youtube.com" + link
        particular_video = complete_link[:43]
        file.write(particular_video)
        print(particular_video)
        file.write("\n")
    file.close()

# get_playlist("https://www.youtube.com/watch?v=FfXoiwwnxFw&list=PLgUwDviBIf0qUlt5H_kiKYaNSqJ81PMMY")
# get_playlist("https://www.youtube.com/watch?v=M3_pLsDdeuU&list=PLgUwDviBIf0oE3gA41TKO2H5bHpPd7fzn")

# get_playlist("https://www.youtube.com/watch?v=yVdKa8dnKiE&list=PLgUwDviBIf0rGlzIn_7rsaR2FQ5e6ZOL9")
# get_playlist("https://www.youtube.com/watch?v=dBGUmUQhjaM&list=PLgUwDviBIf0pcIDCZnxhv0LkHf5KzG9zp")
# get_playlist("https://www.youtube.com/watch?v=9uaXG62Y8Uw&list=PLgUwDviBIf0rf5CQf_HFt35_cF04d8dHN")
# get_playlist("https://www.youtube.com/watch?v=UmJT3j26t1I&list=PLgUwDviBIf0q8Hkd7bK2Bpryj2xVJk8Vk")
# get_playlist("https://www.youtube.com/watch?v=rZ41y93P2Qo&list=PL9gnSGHSqcnr_DxHsP7AW9ftq0AtAyYqJ")
# time.sleep(2)

list_file = open('playlist-videos.txt', 'r', encoding='utf-8')
list_file = list_file.readlines()[22:]
for line in list_file:
    if line == "":
        continue
    try:
        start = time.time()
        download_video(line)
        end = time.time()
        log_file = open('log.txt', 'a', encoding='utf-8')
        log = str(datetime.datetime.now())
        log += " COMPLETED "
        log += line + " " + str(end-start) + " seconds\n"
        log_file.close()
    except Exception:
        print(traceback.format_exc())
        log_file = open('log.txt', 'a', encoding='utf-8')
        log = str(datetime.datetime.now())
        log += " EXCEPTION "
        log += line + "\n"
        log_file.write(log)
        log_file.close()

# download_video("https://youtu.be/RRVYpIET_RU")
# download_video("https://youtu.be/ajmK0ZNcM4Q")

## to-download
# download_video("https://youtu.be/b7AYbpM5YrE")

print("Exiting...")
