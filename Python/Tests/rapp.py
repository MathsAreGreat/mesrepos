import json
from pathlib import Path
import subprocess

DOM = "https://www.youtube.com"

TIMEOUT = 180  # seconds for each yt-dlp call

channel_id = "AJplussaha"


def run_command(cmd):
    """Runs a shell command and streams output live."""
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
    )
    for line in iter(process.stdout.readline, ""):
        print(line, end="")
    process.wait()
    return process.returncode == 0


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


txt_file = (
    Path("/home/mohamed/Documents/Projects/Python/YTDL_SQL") / f"{channel_id}.txt"
)

json_file = (
    Path("/home/mohamed/Documents/Projects/Python/YTDL_SQL") / f"{channel_id}.json"
)
# if not txt_file.exists():
#     cmd = get_download_command(channel_id, 0, ["مع تميم"])
#     print(f"[INFO] Running yt-dlp for {channel_id}")

#     with txt_file.open("w", encoding="utf-8") as f:
#         subprocess.run(cmd, stdout=f, check=True, timeout=TIMEOUT)
#     print(f"[OK] Download finished for {channel_id}")
#     with txt_file.open("r", encoding="utf-8") as f:
#         lines = [json.loads(line.strip()) for line in f.readlines() if line.strip()]
#     info = {line["id"]: line["title"] for line in lines}
#     with json_file.open("w", encoding="utf-8") as f:
#         json.dump(info, f, ensure_ascii=False, indent=2)


with json_file.open("r", encoding="utf-8") as f:
    info = json.load(f)
    print(*list(info))
