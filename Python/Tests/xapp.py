from Mido.variables import download_m3u8_with_ytdlp
from pathlib import Path

u = "https://ok.ru/video/9938265639655"

filename = "/home/mohamed/Videos/vid.%(ext)s"
download_m3u8_with_ytdlp(u, filename, "https://ok.ru/")
