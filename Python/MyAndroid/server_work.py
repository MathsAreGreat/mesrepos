# *Refactored Code with Type Hints*
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# from Besites.variables import DOWN_PATH, retry_on_exception

# DOWNLOAD_DIR = Path(DOWN_PATH) / "Matches"
BACKUP_DIR = Path("Backups")


def run_tasks(func, args_list: list[tuple[str, str]], num_threads: int = 5) -> None:
    def wrapper(args: tuple[str, str]) -> None:
        return func(*args)

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        list(executor.map(wrapper, args_list))


# @retry_on_exception(1)
# def download_video(video_id: str, title: str) -> None:
#     backup_path = BACKUP_DIR / title
#     if backup_path.exists():
#         return

#     download_path = DOWNLOAD_DIR / f"{title}.mp4"
#     if download_path.exists():
#         return

#     try:
#         subprocess.run(
#             [
#                 "yt-dlp",
#                 f"https://www.dailymotion.com/video/{video_id}",
#                 "-o",
#                 str(download_path),
#                 "--no-warnings",
#                 "--no-check-certificate",
#                 "--no-playlist",
#                 "--merge-output-format",
#                 "mp4",
#             ],
#             check=True,
#         )
#     except subprocess.CalledProcessError as e:
#         print(f"Error downloading video: {e}")


def split_mp4_file(file_path: Path, max_size_gb: int = 1900) -> None:
    max_size_bytes = max_size_gb * 1024 * 1024
    output_dir = file_path.parent / file_path.stem
    output_dir.mkdir(parents=True, exist_ok=True)
    if file_path.stat().st_size < max_size_bytes:
        return 0

    part = 1
    start_time = 0
    duration = get_duration(file_path)

    while start_time < duration:
        output_file = output_dir / f"{file_path.stem} [Part {part:03}].mp4"
        cmd = [
            "ffmpeg",
            "-i",
            str(file_path),
            "-ss",
            format_time(start_time),
            "-fs",
            str(max_size_bytes),
            "-c",
            "copy",
            str(output_file),
        ]

        subprocess.run(cmd)

        part += 1
        start_time += get_duration(output_file)

    return 1


def get_duration(file_path: Path) -> float:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(file_path),
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout)


def format_time(time_in_seconds: float) -> str:
    hours = int(time_in_seconds // 3600)
    minutes = int((time_in_seconds % 3600) // 60)
    seconds = int(time_in_seconds % 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# def main(stream: list[tuple[str, str]]) -> None:
#     run_tasks(download_video, stream)


if __name__ == "__main__":
    for f in Path("/home/mohamed/Videos/Temps").glob("*mp4"):
        split_mp4_file(f)
