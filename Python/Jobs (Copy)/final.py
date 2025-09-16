import json
from pathlib import Path
from random import choice
import subprocess
from tqdm.auto import tqdm
import requests

cols = ["#00ff00", "RED", "GREEN", "BLUE", "MAGENTA", "CYAN"]
parent = Path("/home/mohamed/Documents/.Socials/Facebook")
uns = []
for f in parent.rglob("*.*"):
    uns += f.stem.split("_")


def doun(doc: Path, dt, pre, u):
    if not u:
        return None
    fl = u.split("/")[-1].split("?")[0]
    fn: Path = doc / f"{dt}_{pre}_{fl}"
    if fn.exists():
        return fn
    doc.mkdir(parents=True, exist_ok=True)

    sess = requests.session()
    p_file: Path = fn.with_suffix(".part")
    try:
        sz = p_file.stat().st_size
    except:
        sz = 0
    sess.headers["Range"] = f"bytes={sz}-"
    response = sess.get(u, stream=True)
    total_size_in_bytes = float(response.headers.get("content-length", 0))

    if total_size_in_bytes < 1000:
        print(total_size_in_bytes, "Under !!")
        return None

    block_size = 2048
    progress_bar = tqdm(
        total=total_size_in_bytes,
        leave=False,
        colour=choice(cols),
        unit="iB",
        unit_scale=True,
        desc=f"{pre}_{fl} ",
    )
    with open(p_file, "ab") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("Download Error !")
        return 0
    p_file.rename(fn)
    print(fn.stem, ":", total_size_in_bytes)
    return fn


def monfile(f):
    doc = Path("/home/mohamed/Documents/.Socials/Facebook")
    ID = f.stem
    if ID in uns:
        return 0
    with open(f, "r") as fl:
        reps = json.load(fl)
    if not reps:
        fn = f"/home/mohamed/Documents/.Socials/Facebook/Vids/{ID}_vid.jpg"
        with open(fn, "wb") as f:
            f.write(b"")
    user = reps["user"]
    if not user:
        user = "NoUser"
    user = ".".join(e for e in user.split(" ") if e)
    if "uri" in reps:
        doun(doc / user, reps["date"], reps["ID"], reps["uri"])
        return 1
    if not reps["video"]:
        fn = f"/home/mohamed/Documents/.Socials/Facebook/Vids/{ID}_vid.jpg"
        with open(fn, "wb") as f:
            f.write(b"")
    fn = None
    for vid in reps["video"]:
        u = vid.get("base_url")
        if not u:
            continue
        fn = doun(doc / user, reps["date"], f"preitem_{ID}", u)
        if fn:
            break
    sn = None
    for vid in reps["audio"]:
        u = vid.get("base_url")
        if not u:
            continue
        sn = doun(doc / user, reps["date"], f"preitem_{ID}", u)
        if sn:
            break
    lds = doc / user / f'{reps["date"]}_{ID}.mp4'
    if not sn:
        fn.rename(lds)
    else:
        settings = "-c:v copy -c:a aac -strftime 1"
        cmd = f"""ffmpeg -i "{fn}" -i "{sn}" {settings} "{lds}" """
        subprocess.run(cmd, shell=True)
        if lds.exists():
            sn.unlink()
            fn.unlink()
    return 1
