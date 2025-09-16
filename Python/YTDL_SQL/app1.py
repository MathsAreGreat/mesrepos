import argparse
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Configuration
YT_PATH = Path("/home/mohamed/.Kindas/TikToks")
DATA_PATH = Path("/home/mohamed/Documents/datas")
FILES_PATH = Path("Files")

# Ensure necessary directories exist
FILES_PATH.mkdir(parents=True, exist_ok=True)


cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear

# Load existing unique IDs
uniques = [f.stem.split("(")[-1].split(")")[0] for f in YT_PATH.rglob("*")]

filters = {
    "id",
    "title",
    "channel_id",
    "duration",
    "channel",
    "uploader",
    "uploader_id",
    "upload_date",
    "timestamp",
}


def run_command(cmd):
    """Runs a shell command and streams output live."""
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
    )
    for line in iter(process.stdout.readline, ""):
        print(f"{upclear}{line}", end="")
    process.wait()
    return process.returncode == 0


def download_video(video_id):
    """Downloads a video using yt-dlp with specified options."""
    if video_id in uniques:
        print(f"Video '{video_id}' already exists.")
        return 0

    uploader = "%(uploader)s"
    video_id = video_id.strip()

    url = f"https://www.tiktok.com/@user/video/{video_id}"

    output_template = f"""{YT_PATH}/{uploader}/{video_id}.%(ext)s"""

    cmd = f'yt-dlp -i "{url}" -o "{output_template}"'

    if run_command(cmd):
        return 1
    return 0


def fetch_playlist_data(playlist_id):
    """Fetches and filters playlist videos."""
    url = f"https://www.tiktok.com/@{playlist_id}"
    data_file = FILES_PATH / f"{playlist_id}.txt"
    print(f"Fetching playlist data for {playlist_id}...")
    if not data_file.exists():
        run_command(f'yt-dlp --flat-playlist --print "%(id)s" "{url}" > "{data_file}"')
    # Read and filter playlist
    results = []
    with data_file.open("r", encoding="utf-8") as f:
        results = [e.strip() for e in f.readlines() if e.strip()]

    data_file.unlink()

    print(f"Found {len(results)} matching videos in playlist.")
    return results


def main():
    parser = argparse.ArgumentParser(
        description="YouTube media downloader with playlist support."
    )
    parser.add_argument("targets", type=str, nargs="+", help="Video IDs or URLs")
    parser.add_argument(
        "-f", "--filter", type=str, help="Filter playlist videos by title"
    )
    parser.add_argument(
        "-j", "--json", action="store_true", help="Process playlist JSON"
    )

    args = parser.parse_args()

    video_ids = []
    if args.json:
        for nbr in args.targets:
            video_ids += fetch_playlist_data(nbr)
    else:
        video_ids = [e.replace("+", "-") for e in args.targets]

    print(len(video_ids), "items !")

    # Multithreading for downloads
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(
            executor.map(
                lambda vid: download_video(vid),
                video_ids,
            )
        )

    print(f"Completed {sum(results)}/{len(video_ids)} downloads successfully")


if __name__ == "__main__":
    main()
    for f in YT_PATH.glob("*"):
        name = f.name
        if name == "Backups":
            continue
        doc = YT_PATH / "Backups"
        doc.mkdir(parents=True, exist_ok=True)
        fl = doc / name
        fl.touch()
