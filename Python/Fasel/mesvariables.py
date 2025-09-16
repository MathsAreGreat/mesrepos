import subprocess
from time import perf_counter, sleep
from functools import wraps
from bs4 import BeautifulSoup
from shutil import rmtree
import requests
import re
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


requests.packages.urllib3.disable_warnings()


DOM = "www.faselhds.care"

dwn_cols = ["#00ff00", "red", "green", "yellow",
            "blue", "magenta", "cyan", "white"]

cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear

NB = 50


rmtree(
    "/home/mohamed/Documents/datas/Fasel/Datas",
    ignore_errors=True
)

rmtree(
    "temps",
    ignore_errors=True
)


temp_path = Path("temps")
ses_path = Path("Backups")
lib_path = Path("Library")

temp_path.mkdir(parents=True, exist_ok=True)
ses_path.mkdir(parents=True, exist_ok=True)
lib_path.mkdir(parents=True, exist_ok=True)


sess = requests.session()
sess.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
}


def do_thread(fnc, dt, nb):
    with ThreadPoolExecutor(nb) as executor:
        executor.map(lambda args: fnc(*args), dt)


def concatize(*files, o="output", ex="ts"):
    """
    Concatenate multiple files using FFmpeg.

    Parameters:
        files (*args): List of file paths to concatenate.
        o (str): Name of the output file.
        ex (str): Extension for the output file.
    """
    if not files:
        print("No files provided for concatenation.")
        return

    list_file = Path("concat_list.txt")

    # Write file names to a temporary list file
    with list_file.open("w") as f:
        for file in files:
            f.write(f"file '{file}'\n")

    output_path = Path(f"{o}.{ex}")
    cmd = f'ffmpeg -f concat -safe 0 -i "{list_file}" -c copy "{output_path}"'

    try:
        subprocess.run(cmd, shell=True, check=True)
        print(f"* {output_path} Created!", end="\r")
    except subprocess.CalledProcessError:
        print("Error: Failed to concatenate files.")
    finally:
        list_file.unlink(missing_ok=True)


def combine_vids(pt):
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


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        print("Time :", perf_counter() - start, "seconds !")
        return result

    return wrapper


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
                    os.system("clear")
                    print(f"{upclear}> Attempt {attempts} failed !", end="\r")
                    sleep(wait_seconds)

        return wrapper

    return decorator
