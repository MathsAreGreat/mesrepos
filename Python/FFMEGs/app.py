import subprocess
from pathlib import Path


def merge_video_audio(video_file: Path, audio_file: Path, output_file: Path) -> None:
    cmd = [
        "ffmpeg",
        "-i",
        str(video_file),
        "-i",
        str(audio_file),
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        str(output_file),
    ]

    subprocess.run(cmd)


def split_video_specific_part(
    video_file: Path, start_time: int = 0, part_duration: int = 180
) -> None:
    output_dir = video_file.parent / video_file.stem
    output_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        "ffmpeg",
        "-ss",
        format_time(start_time),
        "-i",
        str(video_file),
        "-c",
        "copy",
        "-t",
        str(part_duration),
        str(output_dir / f"{start_time}-{part_duration}{video_file.suffix}"),
    ]
    subprocess.run(cmd)


def split_video_into_parts(
    video_file: Path,
    part_duration: int = 180,
    part_pattern: str = "[Part %03d]",
) -> None:
    output_dir = video_file.parent / video_file.stem
    output_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{video_file.stem}.mp4"
    if part_pattern:
        fname = f"{video_file.stem} {part_pattern}.mp4"

    cmd = [
        "ffmpeg",
        "-i",
        str(video_file),
        "-c",
        "copy",
        "-segment_time",
        str(part_duration),
        "-f",
        "segment",
        "-reset_timestamps",
        "1",
        "-segment_start_number",
        "1",
        str(output_dir / fname),
    ]

    try:
        subprocess.run(cmd, check=True)
        # video_file.unlink()
    except subprocess.CalledProcessError as err:
        print(err)
    part_pattern = part_pattern.replace("%03d", "002")
    fname = output_dir / f"{video_file.stem} {part_pattern}.mp4"
    if not fname.exists():
        part_pattern = part_pattern.replace("002", "001")
        fname = output_dir / f"{video_file.stem} {part_pattern}.mp4"
        fname.rename(video_file.with_suffix(".mp4"))


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


# Example usage:

pr = Path("/home/mohamed/Videos/Youtube/gsleveil20")


for output_file in pr.glob("*.webm"):
    split_video_into_parts(output_file, 30)
