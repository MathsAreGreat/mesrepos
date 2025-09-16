import json
from pathlib import Path
from yt_dlp import YoutubeDL
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor


def download_with_all_audio(url):
    ydl_opts = {"listformats": False, "quiet": True}
    langs = []
    datas = {}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        for f in info.get("formats", []):
            if f.get("acodec") != "none" and f.get("vcodec") == "none":
                if f["format_id"].startswith("251"):
                    lang = f.get("language")  # und = undefined
                    format_id = f.get("format_id")  # und = undefined
                    format_note = f.get("format_note")  # und = undefined
                    langs.append([format_id, lang, format_note])
        key = info["id"]
        datas["title"] = info["title"]
        datas["formats"] = langs
        with Path(f"/home/mohamed/Documents/{key}.json").open("w") as fl:
            json.dump(datas, fl)

    fs = ["bv"]
    fs += [f for f, *_ in langs]
    links = [(url, f) for f in fs]

    with ThreadPoolExecutor() as executor:
        executor.map(lambda args: dwn(*args), links)

    return key, info["title"], langs


def dwn(url, f):
    outtmpl = f"/home/mohamed/Videos/%(id)s.{f}.%(ext)s"
    ydl_opts = {
        "format": f,
        "merge_output_format": "mkv",
        "audio_multistreams": True,
        "outtmpl": outtmpl,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(url)


def tag_languages(tt, key, langs):
    video = f"/home/mohamed/Videos/{key}.bv.mp4"
    audios = [f"/home/mohamed/Videos/{key}.{f}.webm" for f, *_ in langs]

    cmd = ["ffmpeg", "-i", video]
    for a in audios:
        cmd += ["-i", a]

    # mapping
    cmd += ["-map", "0:v"]
    for i in range(len(audios)):
        cmd += ["-map", f"{i+1}:a"]

    for i, (c, l, t) in enumerate(langs):
        cmd += [
            f"-metadata:s:a:{i}",
            f"language={l}",
            f"-metadata:s:a:{i}",
            f"title={t}",
        ]
    cmd += [
        "-c",
        "copy",
        f"/home/mohamed/Videos/{tt} ({key}).mkv",
    ]

    subprocess.run(cmd, check=True)

    Path(video).unlink()
    for audio in audios:
        Path(audio).unlink()


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=Y_JQti8YLn0"
    key, tt, langs = download_with_all_audio(url)
    tag_languages(tt, key, langs)
