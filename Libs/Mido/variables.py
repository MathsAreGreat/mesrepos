import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from random import choice
from time import sleep

import pyfiglet
import requests
from bs4 import BeautifulSoup
from numpy import base_repr
from rich import print
from tqdm.auto import tqdm

cols = ["#00ff00", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]

cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear


seasons = {
    "الاول": "01",
    "الأول": "01",
    "الثاني": "02",
    "الثالث": "03",
    "الرابع": "04",
    "الخامس": "05",
    "السادس": "06",
    "السابع": "07",
    "الثامن": "08",
    "التاسع": "09",
    "العاشر": "10",
}


def sprint(t):
    result = pyfiglet.figlet_format(t)
    print()
    print(result)
    print()


def retry_on_exception(wait_seconds=1):
    """
    A decorator to retry a function if an exception is raised.

    Args:
        wait_seconds (int): Number of seconds to wait before retrying.

    Returns:
        function: A wrapped function with retry logic.

    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    # Attempt to execute the function
                    result = func(*args, **kwargs)
                    break
                except KeyboardInterrupt:
                    print("Exiting...")
                    sys.exit(0)
                except Exception as e:
                    attempts += 1
                    print(e)
                    print(f"> Attempt {attempts} failed !")
                    sleep(wait_seconds)
            return result

        return wrapper

    return decorator


def monhtml(u, data=None, headers=None):
    sess = requests.session()
    if headers:
        sess.headers = headers
    r = sess.post(u, data=data) if data else sess.get(u)
    encoding = (
        r.encoding if "charset" in r.headers.get("content-type", "").lower() else None
    )
    parser = "html.parser"
    return BeautifulSoup(r.content, parser, from_encoding=encoding)


def aria_dwn(ref, target_dir, url, output_file="final_video.mp4", verify_cert=True):
    """
    Downloads an MP4 file using aria2c with a referer header.

    :param ref: The Referer header to use for the request.
    :param target_dir: The directory where the file will be saved.
    :param url: The URL of the MP4 file.
    :param output_file: The name of the output MP4 file.
    :param verify_cert: Whether to verify SSL certificates (default: True).
    """
    fn = Path(target_dir) / output_file
    if fn.exists():
        return 1
    temp_file = f"{output_file}.part"

    command = [
        "aria2c",
        "--referer=" + ref,
        "-c",  # Resume support
        "-x",
        "16",  # Use 16 connections for faster download
        "-d",
        target_dir,
        "-o",
        temp_file,
        "--quiet=false",
        "--summary-interval=1",
        "--console-log-level=notice",
    ]

    # Add certificate verification flag
    if not verify_cert:
        command.append("--check-certificate=false")

    command.append(url)

    col = choice(cols)

    try:
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
        )

        pattern = r"([\d\.]+[KMGT]iB)/([\d\.]+[KMGT]iB)\(.+?([\d\.]+[KMGT]iB).+?ETA:([a-z0-9]+)"
        progress_pattern = re.compile(pattern)

        unit_conversion = {"KiB": 1000, "MiB": 1000**2, "GiB": 1000**3, "TiB": 1000**4}

        pbar = None
        total_size = None

        for line in iter(process.stdout.readline, ""):
            sys.stdout.flush()
            match = progress_pattern.findall(line)

            if match:
                downloaded_str, total_str, speed, eta = match[0]

                downloaded_value, downloaded_unit = re.match(
                    r"([\d\.]+)([KMGT]iB)", downloaded_str
                ).groups()
                total_value, total_unit = re.match(
                    r"([\d\.]+)([KMGT]iB)", total_str
                ).groups()

                downloaded = float(downloaded_value) * unit_conversion[downloaded_unit]
                total_size = float(total_value) * unit_conversion[total_unit]

                if pbar is None:
                    pbar = tqdm(
                        total=total_size,
                        unit="iB",
                        unit_scale=True,
                        desc=f"{output_file[:30]}.. ",
                        colour=col,
                        postfix=["", ""],
                        bar_format="{l_bar}{bar} {n_fmt}/{total_fmt}B [Speed: {postfix[0]} | ETA: {postfix[1]}]",
                    )
                pbar.n = downloaded
                pbar.postfix[0] = speed
                pbar.postfix[1] = eta
                pbar.refresh()

        if pbar:
            pbar.close()

        process.wait()
        if process.returncode == 0:
            print(f"{upclear}Download complete: {output_file}")
            Path(f"{target_dir}/{temp_file}").rename(Path(target_dir) / output_file)
            return 1
    except Exception as e:
        print(f"Error downloading the file: {e}")
        fn = target_dir / output_file
        if fn.exists():
            fn.rename(target_dir / temp_file)
    return 0


def run_tasks(fn, ds, nb=10):
    def your_function(args):
        return fn(*args)

    with ThreadPoolExecutor(nb) as executor:
        datas = executor.map(your_function, ds)
    return datas


def decode_string(p, a, c, k, d):
    def e_func(c):
        return (e_func(c // a) if c >= a else "") + (
            chr(c + 29) if (c := c % a) > 35 else base_repr(c, 36).lower()
        )

    while c > 0:
        c -= 1
        d[e_func(c)] = k[c] or e_func(c)

    p = re.sub(r"\b\w+\b", lambda m: d.get(m.group(0), ""), p)

    return p


def get_m3u8(link, headers=None):
    try:
        response = requests.get(link, headers=headers, timeout=5, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch the link: {e}")
        return None

    text = response.text.replace("\\'", "<&>")
    parts = text.split("'")

    try:
        split_index = parts.index(".split(")
        expr, nums, words = parts[split_index - 3 : split_index]
    except (ValueError, IndexError) as e:
        print(f"[ERROR] Could not parse the m3u8 data: {e}")
        return None

    try:
        nums_list = [int(n) for n in nums.split(",") if n.strip()]
        words_list = words.replace("<&>", "'").split("|")
    except ValueError as e:
        print(f"[ERROR] Failed to parse integers or split words: {e}")
        return None

    try:
        return decode_string(expr.replace("<&>", "'"), *nums_list, words_list, {})
    except (TypeError, KeyError) as e:
        print(f"[ERROR] Decoding failed: {e}")
        return None


def download_m3u8_with_ytdlp(
    url,
    final_file,
    ref=None,
    quality="bestvideo[height<=1080p]+bestaudio/best[height<=1080]/best",
):
    cmd = [
        "yt-dlp",
        "-f",
        quality,
    ]
    if ref:
        cmd += [
            "--add-header",
            f"Referer: {ref}",
            "--add-header",
            "User-Agent: Mozilla/5.0",
        ]
    cmd += [
        "-o",
        final_file,
        url,
        "--cookies-from-browser",
        "firefox",
    ]

    now = datetime.now(timezone.utc)

    try:
        print(f"bbGO [{now}] YT Starting download ...")
        print(f"bbGO [{quality}] ...")
        subprocess.run(cmd, check=True)
        print(f"[{now}] ✅ Download completed successfully.")
    except subprocess.CalledProcessError:
        error_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{error_time}] ❌ Download failed for: {url}")
        return 0
    return 1


def download_m3u8_with_aria2c(
    url,
    final_file,
    ref=None,
    connections=16,
    quality="bv[height<=1080p]+ba/b[height<=1080]/best",
):
    """
    Downloads a .m3u8 video using yt-dlp with aria2c for faster parallel downloading.

    Args:
        url (str): The m3u8 URL to download.
        final_file (Path): yt-dlp output filename template.
        ref (Path): Referer in request headers default none.
        connections (int): Number of parallel connections (for -x and -s).
        quality (str): yt-dlp quality template.

    """
    #  --max-tries=5 --retry-wait=5
    output_template = str(final_file)
    print("URL :", url)
    print("Filename :", output_template)
    aria2_args = (
        f"-x{connections} -s{connections} -k1M "
        "--max-tries=5 "
        "--retry-wait=5 "
        "--auto-file-renaming=false "
        "--allow-overwrite=true "
        "--continue=true"
    )

    cmd = [
        "yt-dlp",
        "-f",
        quality,
    ]
    if ref:
        cmd += [
            "--add-header",
            f"Referer: {ref}",
            "--add-header",
            "User-Agent: Mozilla/5.0",
        ]
    cmd += [
        "-o",
        output_template,
        "--external-downloader",
        "aria2c",
        "--external-downloader-args",
        aria2_args,
        "--retries",
        str(connections),
        url,
    ]

    now = datetime.now(timezone.utc)

    try:
        print(f"bbGO [{now}] Starting download with {connections} connections...")
        subprocess.run(cmd, check=True)
        print(f"[{now}] ✅ Download completed successfully.")
    except subprocess.CalledProcessError:
        error_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{error_time}] ❌ Download failed for: {url}")
        c = Path(output_template).stem.split(".")[-1][1:-1]
        Path("Backups").mkdir(parents=True, exist_ok=True)
        Path(f"Backups/{c}").touch()
        return 0
    return 1


def hello():
    print("hello world")


def egybest(c, name, h, site):
    name = name.replace("جزء", "موسم")
    chemin = "/home/mohamed/Downloads/Library/Seasons"
    if "انمي" in name:
        chemin = "/home/mohamed/Downloads/Library/Animes"
    zed = f"({c})"
    if "حلق" in name:
        name = re.sub(r"Season [^0-9]*", r"موسم ", name)
        test = name.split("حلق")[0].split("موسم")[0]
        doc = test.replace("-", " ").replace(":", " ").strip().title()
        for k, v in seasons.items():
            name = name.replace(k, v)
        ep = re.findall(r"حلق[^0-9]*[0-9\.]+", name)
        sn = re.findall(r"موسم [^0-9]*[0-9]+", name)
        if ep:
            if "لاخيرة" in name:
                zed = f"END.{zed}"
            pp = "E"
            if "خاصة" in name:
                pp = "ONA"
            doc = re.sub(r"[^0-9a-z&\.]+", r" ", doc, flags=re.IGNORECASE)
            enb = re.sub(r"[^0-9\.]", r"", ep[0])
            rst = [
                e
                for e in re.sub(r"[^0-9a-z]", r" ", name, flags=re.IGNORECASE)
                .split(f" {enb}", 1)[-1]
                .split(" ")
                if e
            ]
            if rst:
                rst = ".".join(rst)
                zed = f"{rst}.{zed}"

            enb = enb.zfill(2)
            snb = "S01"
            if sn:
                snb = re.sub(r"[^0-9]", r"", sn[0]).zfill(2)
                snb = f"S{snb}"
            doc = doc.strip().title()
            name = doc.replace(":", "")
            name = re.sub(r"\s+", r" ", name)
            name = name.replace(" ", ".")
            doc = f"{chemin}/{doc}/{snb}"
            fn = f"[{site}].{name}.{snb}.{pp}{enb}.[{h}p].{zed}"
            return doc, fn
    chemin = "/home/mohamed/Downloads/Library/Movies"
    name = (
        re.sub(r"[^a-z0-9]+", r" ", name, flags=re.IGNORECASE)
        .replace(":", "")
        .replace("-", " ")
    )
    name = name.strip().title()
    name = re.sub(r"\s+", r" ", name)
    name = name.replace(" ", ".")
    return chemin, f"[{site}].{name}.[{h}p].{zed}"


def remove_empties(*paths):
    msg = " Time To Free Space "
    print(f"{msg:*^50}")
    print()
    for pt in paths:
        p = Path(pt)
        c = 1
        if not p.exists():
            c = 0
        while c > 0:
            c = 0
            for current in p.rglob("*"):
                if not current.is_dir():
                    continue
                items = list(current.glob("*"))
                if len(items) > 0:
                    continue
                current.rmdir()
                c += 1


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


def split_video_into_size(video_file: Path, max_mb_size: int) -> None:
    mx = max_mb_size * 1024 * 1024
    nb = video_file.stat().st_size // mx
    md = video_file.stat().st_size % mx
    if md:
        nb += 1
    dur = (get_duration(video_file) // nb) + 1
    split_video_into_parts(video_file, dur)


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
