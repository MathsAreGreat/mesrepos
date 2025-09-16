import os
from pathlib import Path
import re
from shutil import rmtree


def concatize(*files, o="output", ex="ts"):
    filenames = "|".join(files[:])
    cmd = f'ffmpeg -i "concat:{filenames}" -c copy "Koora/{o}.{ex}"'
    os.system(cmd)
    msg = f"* {o}.{ex} Created !"
    print(f"{msg:<40}", end="\r")


def combine_vids(doc="Koora"):
    for v_out in os.listdir(doc):
        if (
            not v_out.endswith(".mp4")
            and not v_out.endswith(".ts")
            and not os.path.exists(f"Koora/{v_out}.mp4")
        ):
            fs = [
                f"Koora/{v_out}/{f}" for f in os.listdir(f"Koora/{v_out}") if f.endswith(".ts")]
            fs = sorted(
                fs, key=lambda e: re.sub(
                    r"[^0-9]", r"", e.rsplit(".", 1)[0]).zfill(20)
            )
            ph = 0
            j = 1
            while len(fs) > 100:
                i = 0
                ph += 1
                while fs:
                    i += 1
                    concatize(*fs[:100], o=f"{v_out}_{j}_{i}")
                    fs = fs[100:]
                fs = [f"Koora/{v_out}_{j}_{n+1}.ts" for n in range(i)]
                j += 1
            concatize(*fs, o=v_out, ex="mp4")
            if ph:
                for f in fs:
                    os.remove(f)
                    msg = f"** Removing {f}"
                    print(f"{msg:<40}", end="\r")
        if os.path.exists(f"Koora/{v_out}.mp4"):
            rmtree(f"Koora/{v_out}")
    msg = "> All is Done !"
    print(f"{msg:<40}")


def combine_vids(p="Koora"):
    doc = Path(p)
    for v_out in os.listdir(doc):
        if (
            not v_out.endswith(".mp4")
            and not v_out.endswith(".ts")
            and not os.path.exists(f"Koora/{v_out}.mp4")
        ):
            pass
