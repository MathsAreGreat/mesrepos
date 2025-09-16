import json
from pathlib import Path
import re
from time import sleep
from urllib.parse import urljoin

import eyed3
import requests
from Mido.variables import upclear, print, split_video_into_size

sess = requests.Session()
DOM = "https://moussiqa.com"
sess.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Referer": DOM,
}

Path("infos").mkdir(exist_ok=True)


def get_infos(track_id):
    fname = Path(f"infos/tracks_{track_id}.json")
    if not fname.exists():
        return 0
    with fname.open("r") as f:
        track_info = json.load(f)
    return track_info


def get_lyrics(track_id):
    fname = Path(f"infos/lyrics_{track_id}.json")
    if not fname.exists():
        return 0
    with fname.open("r") as f:
        lyrics = json.load(f)
    return lyrics


def get_albums(artist_id, nb=0):
    url = f"https://moussiqa.com/api/v1/artists/{artist_id}/albums?perPage=100&query=&paginate=simple&page=1"
    r = sess.get(url)
    data = r.json()
    datas = data["pagination"]["data"]
    ids = []
    for data in datas:
        for track in data["tracks"]:
            track_id = track["id"]
            ids.append(track_id)
            fname = Path(f"infos/tracks_{track_id}.json")
            lrc_file = Path(f"infos/lyrics_{track_id}.lrc")
            if not nb and not lrc_file.exists():
                url = f"https://moussiqa.com/api/v1/tracks/{track_id}/lyrics"
                print(f"{upclear}{url}")
                r = sess.get(url)
                lyrics = r.json()
                with Path(f"infos/lyrics_{track_id}.json").open("w") as f:
                    json.dump(lyrics, f)
            if not nb and not fname.exists():
                print(f"{upclear}{fname}")
                track_info = {
                    "name": track["name"],
                    "album_name": track["album_name"],
                    "number": track["number"],
                    "artist": track["artists"][0]["name"],
                    "src": urljoin(DOM, track["src"]),
                    "created_at": track["created_at"],
                    "image": urljoin(DOM, track["image"]),
                }
                with fname.open("w") as f:
                    json.dump(track_info, f)
    with Path(f"infos/artist_{artist_id}.json").open("w") as f:
        json.dump(data, f)
    return ids


def get_track(track_id):
    fname = Path(f"infos/tracks_{track_id}.json")
    if not fname.exists():
        return 0
    with fname.open("r") as f:
        track_info = json.load(f)
    src = track_info["src"]
    r = sess.get(src)
    audio_file = Path(
        f"/home/mohamed/Music/Moosiqa/{track_info["artist"]}/{track_id}.mp3"
    )
    if not audio_file.exists():
        audio_file.parent.mkdir(parents=True, exist_ok=True)
        with audio_file.open("wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"{upclear}{audio_file}")
        return 1
    return 0


def modify_metadata(
    file_path,
    title=None,
    artist=None,
    album=None,
    album_artist=None,
    genre=None,
    year=None,
    comment=None,
    track_number=None,
    album_cover=None,
    image_url=None,
    lyrics=None,
):
    audio: eyed3.AudioFile = eyed3.load(file_path)
    audio.initTag()

    # Apply tag updates
    if title:
        audio.tag.title = title
    if artist:
        audio.tag.artist = artist
    if album:
        audio.tag.album = album
    if album_artist:
        audio.tag.album_artist = album_artist
    if genre:
        audio.tag.genre = genre
    if year:
        audio.tag.recording_date = eyed3.core.Date(int(year))
    if comment:
        audio.tag.comments.set(comment)
    if track_number:
        audio.tag.track_num = int(track_number)

    # Add album cover image
    if album_cover:
        fn = dwn_jpeg(album_cover, image_url)  # You must define this function elsewhere
        if fn.exists():
            with fn.open("rb") as img_fp:
                image_data = img_fp.read()
            audio.tag.images.set(3, image_data, "image/jpeg", "Cover")

    if lyrics:
        audio.tag.lyrics.set(lyrics.strip())

    audio.tag.save()
    print(":: Updated:", comment)
    return 1


def dwn_jpeg(k, url):
    covers_path = Path("/home/mohamed/Pictures/.Covers/MS_Covers")
    fn = covers_path / f"{k}.jpg"
    if fn.exists():
        return fn
    covers_path.mkdir(parents=True, exist_ok=True)
    with requests.get(url, timeout=10) as cover:
        bcontent = cover.content
        with fn.open("wb") as e:
            e.write(bcontent)
        return fn


import subprocess


def m4a_to_mp3(input_file, output_file):
    command = [
        "ffmpeg",
        "-y",
        "-i",
        input_file,  # -y overwrites if exists
        "-vn",  # no video
        "-acodec",
        "libmp3lame",
        output_file,
    ]
    try:
        if subprocess.run(command, check=True).returncode:
            print("No COMPLETE :", input_file)
        else:
            Path(input_file).unlink()
    except:
        print("ERROR :", input_file)


parent = Path("/home/mohamed/Videos/Youtube/LaLiga")

for f in parent.glob("*"):
    split_video_into_size(f, 2000)
