import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Constants
DOM = "https://www.youtube.com"
TIMEOUT = 180  # seconds for each yt-dlp call

USERS_FILE = Path("users.json")
PLAYLISTS_FILE = Path("pls.json")
USERS_ID_FILE = Path("users_id.json")

# Load data from files
with PLAYLISTS_FILE.open("r", encoding="utf-8") as f:
    playlists = json.load(f)

with USERS_FILE.open("r", encoding="utf-8") as f:
    users = json.load(f)

with USERS_ID_FILE.open("r", encoding="utf-8") as f:
    users_id = json.load(f)

# Create dictionaries for easy lookup
users_map = {v: k for k, v in users.items()}
users_id_map = {v: k for k, v in users_id.items()}


# Function to download audio
def download_audio(video_id: str) -> None:
    try:
        print(f"[INFO] Starting download for video {video_id}")
        cmd = [
            "yt-dlp",
            "-f",
            "bestaudio",
            f"{DOM}/watch?v={video_id}",
            "--ignore-errors",
            "--match-filter",
            "!is_live",
            "-o",
            "Audios/%(id)s.%(ext)s",
            "--concurrent-fragments",
            "16",
            "-x",
            "--audio-format",
            "mp3",
            "--audio-quality",
            "0",
            "--cookies-from-browser",
            "firefox",
        ]
        subprocess.run(cmd, check=True, timeout=TIMEOUT)
        print(f"[OK] Finished download for video {video_id}")
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] Download stuck for {video_id}, skipping")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed downloading {video_id}: {e}")


# Function to save video info
def save_video_info(line: str) -> int:
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        print("[WARN] Skipped invalid JSON line")
        return 0

    if data.get("title") == "[Private video]":
        print("[INFO] Skipped private video")
        return 0

    video_id = data.get("id")
    if not video_id:
        print("[WARN] No video ID found in JSON")
        return 0

    json_file = Path(f"Files/{video_id}.json")
    if json_file.exists():
        print(f"[INFO] Skipped {video_id}, JSON file already exists")
        return 0

    json_file_id = Path(f"/home/mohamed/Documents/Youtube/IDs/{video_id}.json")
    if json_file_id.exists():
        print(f"[INFO] Skipped {video_id}, already in IDs folder")
        return 0

    info = {
        "id": video_id,
        "playlist_id": data.get("playlist_id"),
        "playlist_title": data.get("playlist_title"),
    }

    # Fetch channel info (single video case)
    print(f"[INFO] Channelizing video {video_id}")
    channel_info = channelize((f"=={video_id}", 1))
    if not channel_info:
        print(f"[WARN] No channel info for {video_id}")
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
    video_info = {k: channel_info.get(k) for k in keys if k in channel_info}
    video_info.update(info)

    subtitles = video_info.get("subtitles")
    if subtitles:
        subtitles = {k: v[-1]["url"] for k, v in subtitles.items() if k != "live_chat"}
        video_info["subtitles"] = subtitles

    video_info.pop("id", None)

    with json_file.open("w", encoding="utf-8") as f:
        json.dump(video_info, f, indent=2)

    print(f"[OK] Saved info for {video_id}")
    return 1


# Function to channelize
def channelize(args: tuple) -> dict:
    channel_id, max_videos, *filters = args
    if max_videos < 0:
        return {}

    txt_file = Path("Files") / f"{channel_id}.txt"
    if not txt_file.exists():
        cmd = get_download_command(channel_id, max_videos, filters)
        print(f"[INFO] Running yt-dlp for {channel_id}")
        try:
            with txt_file.open("w", encoding="utf-8") as f:
                subprocess.run(cmd, stdout=f, check=True, timeout=TIMEOUT)
            print(f"[OK] Download finished for {channel_id}")
        except subprocess.TimeoutExpired:
            print(f"[TIMEOUT] Skipped {channel_id}, yt-dlp hung")
            return {}
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] yt-dlp failed for {channel_id}: {e}")
            return {}

    try:
        with txt_file.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        if len(lines) < 2:
            return json.loads(lines[0])
        print(f"[INFO] Loaded {len(lines)} lines for {channel_id}")
        txt_file.unlink()

        results = []
        with ThreadPoolExecutor(30) as executor:
            results = list(executor.map(save_video_info, lines))

        total_processed = sum(results)
        print(f"[OK] Processed {total_processed}/{len(lines)} items for {channel_id}")
        return {"processed": total_processed, "total": len(lines)}
    except Exception as e:
        print(f"[ERROR] Channelize failed for {channel_id}: {e}")
        return {}


def get_channel_url(channel_id: str) -> str:
    if channel_id.startswith("UC"):
        return f"{DOM}/channel/{channel_id}/videos"
    elif channel_id.startswith("PL"):
        return f"{DOM}/playlist?list={channel_id}"
    elif channel_id.startswith("=="):
        return f"{DOM}/watch?v={channel_id[2:]}"
    else:
        return f"{DOM}/@{channel_id}/videos"


def get_download_command(channel_id: str, max_videos: int, filters: list) -> list:
    url = get_channel_url(channel_id)
    cmd = [
        "yt-dlp",
        url,
        "--cookies-from-browser",
        "firefox",
        "--flat-playlist",
        "--dump-json",
    ]
    if max_videos:
        cmd += ["--playlist-end", str(max_videos)]
    if filters:
        match_title = "|".join(f"({e})" for e in filters if not e.startswith("+="))
        reject_title = "|".join(f"({e[2:]})" for e in filters if e.startswith("+="))
        if match_title:
            cmd += ["--match-title", match_title]
        if reject_title:
            cmd += ["--reject-title", reject_title]
    return cmd


# Function to stabilize
def stablize(data: dict) -> None:
    print("[INFO] Stabilizing files...")
    for file in Path("Files").glob("*.json"):
        if file.suffix != ".json":
            print(f"[WARN] Removing invalid file {file}")
            file.unlink()
            continue

        with file.open("r", encoding="utf-8") as f:
            video_data = json.load(f)

        channel_id = video_data.get("channel_id")
        if channel_id:
            video_data["title"] = " ".join(e for e in video_data["title"].split() if e)

            user_id = users_id.get(channel_id)
            if user_id:
                video_data["uploader_id"] = f"@{user_id}"
            elif video_data.get("uploader_id"):
                users_id[channel_id] = video_data.get("uploader_id")[1:]

            user = users.get(channel_id)
            if user:
                video_data["uploader"] = user
            elif video_data.get("uploader"):
                users[channel_id] = video_data["uploader"]

            playlist_title = get_playlist_title(data, channel_id, video_data["title"])
            if playlist_title:
                video_data["playlist_title"] = playlist_title

        with file.open("w", encoding="utf-8") as f:
            json.dump(video_data, f)

    with USERS_FILE.open("w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

    with USERS_ID_FILE.open("w", encoding="utf-8") as f:
        json.dump(users_id, f, indent=4)

    print("[OK] Stabilization completed")


def get_playlist_title(data: dict, channel_id: str, title: str) -> str | None:
    user_id = users_id.get(channel_id)
    if user_id:
        for key, value in data.items():
            if "==" not in key:
                continue
            channel, keyword = key.split("==", 1)
            if channel == user_id and keyword in title:
                return value
    return None
