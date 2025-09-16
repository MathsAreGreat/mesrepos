import os
from pathlib import Path
import re
from shutil import rmtree
import subprocess
from bs4 import BeautifulSoup
from functools import wraps
from time import sleep

DOWN_PATH = "/home/mohamed/Videos"


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
                    return result
                except Exception:
                    attempts += 1
                    print(f"> Attempt {attempts} failed !")
                    sleep(wait_seconds)

        return wrapper

    return decorator


def monhtml(sess, r, ref=None, data=None):
    if not ref:
        refs = r.split("/")[:3]
        ref = "/".join(refs)
    sess.headers["Referer"] = ref
    if data:
        r = sess.post(r, data=data)
    else:
        r = sess.get(r)
    encoding = (
        r.encoding if "charset" in r.headers.get(
            "content-type", "").lower() else None
    )
    parser = "html.parser"
    return BeautifulSoup(r.content, parser, from_encoding=encoding)


def concatize(*files, o="output", ex="ts"):
    """
    Concatenate multiple files using FFmpeg.

    Parameters:
        files (*args): List of file paths to concatenate.
        output_name (str): Name of the output file.
        extension (str): Extension for the output file.
    """
    if not files:
        print("No files provided for concatenation.")
        return

    input_files = "|".join(str(file) for file in files)
    output_path = Path(f"{o}.{ex}")
    cmd = f'ffmpeg -i "concat:{input_files}" -c copy "{output_path}"'

    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"* {output_path} Created!", end="\r")
    except subprocess.CalledProcessError:
        print("Error: Failed to concatenate files.")


def combine_vids(pt=DOWN_PATH):
    try:
        p = Path(pt)
    except:
        return 0
    nb = 0
    for v_out in p.rglob("*"):
        if v_out.is_file():
            continue
        fs = [f"{f}" for f in v_out.glob("*.part")]
        if fs:
            nb += 1
            continue
        fn = v_out.with_suffix(f"{v_out.suffix}.mp4")
        if not fn.exists():
            fs = [f"{f}" for f in v_out.glob("*.ts")]
            fs = sorted(
                fs, key=lambda e: re.sub(
                    r"[^0-9]", r"", e.rsplit(".", 1)[0]).zfill(20)
            )
            ph = 0
            j = 1
            NBR = 900
            while len(fs) > NBR:
                i = 0
                ph += 1
                while fs:
                    i += 1
                    concatize(*fs[:NBR], o=f"{v_out}_{j}_{i}")
                    fs = fs[NBR:]
                fs = [f"{v_out}_{j}_{n+1}.ts" for n in range(i)]
                j += 1
            concatize(*fs, o=v_out, ex="mp4")
            if ph:
                for f in fs:
                    os.remove(f)
                    msg = f"** Removing {f}"
                    print(f"{msg:<40}")
        if fn.exists():
            rmtree(f"{v_out}")
    msg = "> All is Done !"
    print(f"{msg:<40}")
    return nb
