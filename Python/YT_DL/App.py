import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

DOM = "https://www.youtube.com"


def load_json(line: str) -> dict:
    try:
        return json.loads(line)
    except json.JSONDecodeError as e:
        print(f"Error loading JSON: {e}")
        return {}


def extract_info(data: dict, keys: list) -> dict:
    return {k: v for k, v in data.items() if k in keys}


def save_video_info(line: str) -> int:
    data = load_json(line)
    if data.get("title") == "[Private video]":
        return 0

    video_id = data.get("id")
    if not video_id:
        return 0

    json_file = Path(f"Files/{video_id}.json")
    if json_file.exists():
        return 0

    keys = [
        "title",
        "channel_id",
        "duration",
        "subtitles",
        "chapters",
        "uploader",
        "uploader_id",
        "upload_date",
    ]
    info = extract_info(data, keys)
    info.update(
        {
            "id": video_id,
            "playlist_id": data.get("playlist_id"),
            "playlist_title": data.get("playlist_title"),
        }
    )

    subtitles = info.get("subtitles")
    if subtitles:
        subtitles = {k: v[-1]["url"] for k, v in subtitles.items() if k != "live_chat"}
        info["subtitles"] = subtitles

    with open(json_file, "w") as f:
        json.dump(info, f, indent=2)

    return 1


def channelize(args: tuple) -> None:
    channel_id, max_videos, *filters = args
    if max_videos < 0:
        return

    json_file = Path(f"Files/{channel_id}.json")
    if json_file.exists():
        return

    txt_file = Path(f"Files/{channel_id}.txt")
    url = f"{DOM}/@{channel_id}/videos"
    if channel_id.startswith("UC"):
        url = f"{DOM}/channel/{channel_id}/videos"
    elif channel_id.startswith("PL"):
        url = f"{DOM}/playlist?list={channel_id}"
    elif channel_id.startswith("=="):
        url = f"{DOM}/watch?v={channel_id[2:]}"

    cmd = f'yt-dlp "{url}" --cookies-from-browser firefox --flat-playlist --dump-json'
    if max_videos:
        cmd += f' --playlist-end "{max_videos}"'
    if filters:
        match_title = "|".join(f"({e})" for e in filters if not e.startswith("+="))
        reject_title = "|".join(f"({e[2:]})" for e in filters if e.startswith("+="))
        cmd += f' --match-title "{match_title}" --reject-title "{reject_title}"'
    cmd += f" > {txt_file}"

    subprocess.run(cmd, shell=True)

    with open(txt_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    txt_file.unlink()

    with ThreadPoolExecutor() as executor:
        executor.map(save_video_info, lines)


def download_video(video_id: str) -> None:
    quality = "/".join(
        f"{q}+bestaudio[ext=mp4]" for q in [299, 303, 335, 137, 399, 248, 169]
    )
    quality += "/37/46/96/22/"
    quality += "/".join(f"{q}+bestaudio" for q in [299, 303, 335, 137, 399, 248, 169])
    quality += "/bestvideo[height<=1080][protocol^=https]+bestaudio/bestvideo+bestaudio"

    dp = "Videos/%(uploader_id)s/%(upload_date)s_%(title)s (%(id)s).%(ext)s"
    url = f"{DOM}/watch?v={video_id}"

    cmd = f'yt-dlp -f "{quality}" "{url}" -o "{dp}" --ignore-errors --cookies-from-browser firefox'
    subprocess.run(cmd, shell=True)


def already_exist() -> list:
    existing_videos = set()
    for directory in ["/home/mohamed/Videos/Youtube", "Videos", "Backups"]:
        directory_path = Path(directory)
        if directory_path.exists():
            existing_videos.update(
                f.stem.split("(")[-1].split(")")[0]
                for f in directory_path.rglob("*")
                if f.stem.endswith(")")
            )

    for el in existing_videos:
        Path(f"Backups/({el}).tmp").touch(exist_ok=True)

    video_ids = []
    for file in Path("Files").glob("*.json"):
        video_id = file.stem
        if video_id not in existing_videos:
            with open(file, "r") as f:
                data = json.load(f)
                if data.get("duration") and data["duration"] > 60:
                    video_ids.append(video_id)

    return list(set(video_ids))


mx = 15

ds = [
    ("Alaraby-Tube", mx, "حضارة|في الحضارة"),
    ("Hawaripodcast", mx, "لؤي فوزي"),
    ("shoatt", mx, "11"),
]

with ThreadPoolExecutor(2) as executor:
    executor.map(channelize, ds)

datas = already_exist()

with ThreadPoolExecutor(20) as executor:
    executor.map(download_video, datas)

parent = Path("/home/mohamed/Documents/Projects/Python/YT_DL/Videos")
to = Path("/home/mohamed/Videos/Youtube/Favoris")
for dr in parent.glob("*"):
    doc = to / dr.name[1:]
    doc.mkdir(parents=True, exist_ok=True)
    for f in dr.glob("*"):
        f.rename(doc / f.name)

already_exist()
