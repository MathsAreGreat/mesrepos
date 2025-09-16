import argparse
import json
import re
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from convert import convert, teggings

# Configuration
AT_PATH = Path("/home/mohamed/Music/Soundtracks/Youtube")
YT_PATH = Path("/home/mohamed/Videos/Youtube")
DATA_PATH = Path("/home/mohamed/Documents/datas")
FILES_PATH = Path("Files")

# Ensure necessary directories exist
DATA_PATH.mkdir(parents=True, exist_ok=True)
FILES_PATH.mkdir(parents=True, exist_ok=True)


cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear

# Load existing unique IDs
uniques = []

uniques += [f.stem for f in Path("Audios").glob("*")]
uniques += [
    f.stem.split(" ")[-1][1:-1] for f in YT_PATH.rglob("*") if f.stem.endswith(")")
]

DOM = "https://www.youtube.com"
URL_PREFIXES = {
    "PL": f"{DOM}/playlist?list=",
    "==": f"{DOM}/",
    "ht": f"{DOM}/watch?v=",
    "RD": "https://www.youtube.com/watch?v=kPa7bsKwL-c&list=",
}


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

# Extract video IDs from filenames
for f in YT_PATH.rglob("*.*"):
    video_id = f.stem.split(" ")[-1][1:-1]
    (DATA_PATH / video_id).touch()

for f in AT_PATH.rglob("*.*"):
    video_id = f.stem
    (DATA_PATH / video_id).touch()


def run_command(cmd):
    """Runs a shell command and streams output live."""
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True
    )
    for line in iter(process.stdout.readline, ""):
        print(f"{upclear}{line}", end="")
    process.wait()
    return process.returncode == 0


def download_video(video_id, split_chapters=False, audio_only=False, custom_path=False):
    """Downloads a video using yt-dlp with specified options."""
    if video_id in uniques:
        print(f"Video '{video_id}' already exists.")
        return 0

    # Quality settings

    dv = "(mergeall[format_id~=251]/mergeall[format_id~=140])"

    q = "/".join(f"{e}" for e in [299, 303, 335, 137, 399, 248, 169])
    quality = f"({q})+{dv}/37/46/96/22/({q}/bestvideo[height<=1080])+{dv}"

    output_dir = "/home/mohamed/Videos/Youtube"
    uploader = "%(uploader_id)s"
    if custom_path:
        uploader = custom_path

    url = f"https://www.youtube.com/watch?v={video_id}"
    extra_options = (
        "--cookies-from-browser firefox --write-sub --sub-langs ar,fr,en,-live_chat"
    )

    output_template = (
        f"""{output_dir}/{uploader}/%(upload_date)s_%(title)s (%(id)s).%(ext)s"""
    )

    if audio_only:
        quality = "bestaudio"
        output_template = "Audios/%(id)s.%(ext)s"
    if split_chapters:
        output_template = f"{output_dir}/deleteme.%(id)s.%(ext)s"
        chapters_template = f"""{
            output_dir
        }/%(uploader_id)s/%(title)s/[%(upload_date)s_%(section_number)03d] %(section_title)s (%(id)s).%(ext)s"""
        extra_options += f' --split-chapters -o "chapter:{chapters_template}"'

    cmd = f'yt-dlp -f "{quality}" -i "{url}" -o "{output_template}" {extra_options} --audio-multistreams'

    if run_command(cmd):
        (DATA_PATH / video_id).touch()
        return 1
    return 0


def fetch_playlist_data(playlist_url, filter_text=None, max_in=0):
    if not filter_text:
        filter_text = ""
    """Fetches and filters playlist videos."""
    playlist_id = re.sub(r"^=+", "@", playlist_url)
    playlist_id = re.sub(r"^00+", "", playlist_id)
    url = playlist_id
    data_file = FILES_PATH / f"{playlist_id}.txt"
    json_file = FILES_PATH / f"{playlist_id}.json"
    if json_file.exists():
        return [playlist_id]

    if prefix := URL_PREFIXES.get(playlist_url[:2]):
        url = f"{prefix}{playlist_id}"

    print(f"Fetching playlist data for {playlist_id}...")
    if not data_file.exists():
        cmd = f'yt-dlp "{url}" --flat-playlist --dump-json'
        if max_in:
            cmd += f" --playlist-end {max_in}"
        run_command(f'{cmd} > "{data_file}"')
    # Read and filter playlist
    results = []
    with data_file.open("r", encoding="utf-8") as f:
        lesdatas = f.read()
    try:
        lesdata = json.loads(lesdatas)
        results.append(lesdata["id"])
        with open(json_file, "w", encoding="utf-8") as fl:
            json.dump({k: v for k, v in lesdata.items() if k in filters}, fl)
    except:
        for line in lesdatas.strip().split("\n"):
            try:
                entry = json.loads(line)
                if filter_text.lower() in entry.get("title", "").lower():
                    results.append(entry["id"])
            except Exception as err:
                print(err)

    data_file.unlink()

    print(f"Found {len(results)} matching videos in playlist.")
    return results


def clean_up():
    """Cleans up empty directories and moves files to YT_PATH."""
    print("Cleaning up...")

    # Move downloaded files to final location
    moved_files = 0
    for file in Path("/home/mohamed/Videos/Youtube").rglob("*"):
        if file.is_dir():
            continue
        if file.suffix == ".part":
            continue
        if "deleteme." in file.name:
            file.unlink()
            print(f"Removed temporary file: {file.name}")
            continue
        file_parts = [e[0] for e in file.parent.parts]
        if "@" not in file_parts:
            continue

        *file_parts, _ = list(dict.fromkeys(file.parts))
        file_parent = "/".join(
            e.replace("@", "")
            for i, e in enumerate(file_parts)
            if i > file_parts.index("Youtube")
        )
        dest_path = YT_PATH / file_parent / file.name
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file), str(dest_path))
        print(f"Moved: {file.name}")
        moved_files += 1

    if moved_files:
        print(f"Moved {moved_files} files to final location")
    # Remove empty directories
    removed_dirs = 1
    while removed_dirs:
        print(f"Removing {removed_dirs} empty directories")
        removed_dirs = 0
        for path in sorted(
            Path("/home/mohamed/Videos").rglob("*"),
            key=lambda p: len(p.parts),
            reverse=True,
        ):
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
                print(f"Removed empty directory: {path}")
                removed_dirs += 1

    pth = "Audios"
    for f in Path(pth).rglob("*).*"):
        f.rename(f.with_stem(f.stem.split(" ")[-1][1:-1]))
    nb = 1
    while nb:
        nb = convert(pth)
    teggings(pth)
    nb = 1
    while nb:
        nb = 0
        for f in Path().rglob("*"):
            try:
                f.rmdir()
                nb += 1
            except:
                pass


def main():
    parser = argparse.ArgumentParser(
        description="YouTube media downloader with playlist support."
    )
    parser.add_argument("targets", type=str, nargs="+", help="Video IDs or URLs")
    parser.add_argument(
        "-f", "--filter", type=str, help="Filter playlist videos by title"
    )
    parser.add_argument(
        "-p", "--path", type=str, help="Custom folder name for organization"
    )
    parser.add_argument(
        "-a", "--audio", action="store_true", help="Download audio only"
    )
    parser.add_argument(
        "-c", "--chapters", action="store_true", help="Split into chapters"
    )
    parser.add_argument(
        "-j", "--json", action="store_true", help="Process playlist JSON"
    )
    parser.add_argument(
        "-m", "--maxin", type=str, help="Custom folder name for organization"
    )

    args = parser.parse_args()

    video_ids = []
    if args.json:
        for target in args.targets:
            nbr = target.replace("+", "-")
            if nbr.startswith(("PL", "UC", "=", "RD")):
                video_ids += fetch_playlist_data(nbr, args.filter, args.maxin)
            else:
                video_ids.append(nbr)
        if nbr.startswith(("PL", "UC", "@", "RD")):
            with ThreadPoolExecutor(max_workers=10) as executor:
                executor.map(
                    lambda nbr: fetch_playlist_data(nbr, args.filter),
                    video_ids,
                )
    else:
        video_ids = [e.replace("+", "-") for e in args.targets]

    # Multithreading for downloads
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(
            executor.map(
                lambda vid: download_video(vid, args.chapters, args.audio, args.path),
                video_ids,
            )
        )

    print(f"Completed {sum(results)}/{len(video_ids)} downloads successfully")
    clean_up()


if __name__ == "__main__":
    main()
    for fn in Path("/home/mohamed/Documents/datas").glob("*"):
        if not fn.is_file():
            continue
        if fn.stat().st_size > 10:
            continue
        fn.unlink()
