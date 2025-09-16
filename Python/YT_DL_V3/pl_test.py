import json
import os
from pathlib import Path

DOM = "https://www.youtube.com"

# c = "abdullatif1"
# txt_file = f"{c}.txt"
# cmd = f"""yt-dlp --flat-playlist --skip-download --print "%(id)s==%(title)s" "https://www.youtube.com/@{c}/playlists"  > {txt_file}"""
# os.system(cmd)

cs = [
    "PLJ_GEgUjCHpKqMIUy2giTQGYi5Gdx3U4r",
    "PLJ_GEgUjCHpLya7jQRv1l5RrR5T7O5fsc",
    "PLJ_GEgUjCHpIWXnF0BFFmL_NTcnjNMIlc",
    "PLJ_GEgUjCHpJJx05NlwZgW_m7X9_equ_N",
    "PLJ_GEgUjCHpJlavXYJpK9hBk4uPxxsDpr",
    "PLJ_GEgUjCHpLx7RtIMEuLZtlfKnPCw5il",
]

for c in cs:
    dd = f"{DOM}/playlist?list={c}"
    txt_file = Path(f"Files/{c}.txt")
    print("Loading", c, "!")
    cmd = f'yt-dlp "{dd}" --flat-playlist --dump-json > {txt_file}'
    os.system(cmd)
    print("Loaded", c, "!")
    with txt_file.open("r") as el:
        lines = [e.strip() for e in el.readlines() if e.strip()]
    for st in lines:
        data = json.loads(st)
        keys = {"id", "playlist_id", "playlist_title"}
        info = {k: v for k, v in data.items() if k in keys}
        ID = info["id"]
        del info["id"]
        json_file = Path(f"/home/mohamed/Documents/Youtube/IDs/{ID}.json")
        if json_file.exists():
            with json_file.open("r") as e:
                infos = json.load(e)
            infos.update(info)
            with json_file.open("w") as e:
                json.dump(infos, e)
    txt_file.unlink()
