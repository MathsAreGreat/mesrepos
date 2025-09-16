import json
from pathlib import Path

from converts import gad_all

if __name__ == "__main__":
    to = Path("/home/mohamed/Music/Soundtracks")
    inf_path = Path("/home/mohamed/Documents/Youtube/IDs")
    usd_path = Path("users_id.json")
    us_path = Path("users.json")
    gs_path = Path("genres.json")
    pl_path = Path("pls.json")

    try:
        with pl_path.open("r", encoding="utf-8") as e:
            pls = json.load(e)
    except FileNotFoundError:
        pls = {}

    try:
        with usd_path.open("r", encoding="utf-8") as e:
            users_id = json.load(e)
    except FileNotFoundError:
        users_id = {}

    try:
        with us_path.open("r", encoding="utf-8") as e:
            users = json.load(e)
    except FileNotFoundError:
        users = {}

    try:
        with gs_path.open("r", encoding="utf-8") as e:
            genres = json.load(e)
    except FileNotFoundError:
        genres = {}

    for fn in inf_path.rglob("*.json"):
        try:
            with fn.open("r", encoding="utf-8") as e:
                data = json.load(e)
        except FileNotFoundError:
            data = {}

        if not (chid := data.get("channel_id")):
            continue

        if data.get("playlist_id"):
            pid = data.get("playlist_id")
            if pid[:2] == "PL" and not pls.get(pid):
                pls[pid] = data["playlist_title"]

        if genres.get(chid):
            print(chid, ":", genres[chid])
            data["genre"] = genres[chid]

        if pls.get(chid):
            data["playlist_title"] = pls[chid]

        if pls.get(pid):
            data["playlist_title"] = pls[pid]

        with fn.open("w", encoding="utf-8") as e:
            json.dump(data, e)

    for fn in to.rglob("*.mp3"):
        fn.rename(Path("Audios") / fn.name)

    with pl_path.open("w", encoding="utf-8") as e:
        json.dump(pls, e, indent=4)
    with usd_path.open("w", encoding="utf-8") as e:
        json.dump(users_id, e, indent=4)
    with us_path.open("w", encoding="utf-8") as e:
        json.dump(users, e, indent=4)
    with gs_path.open("w", encoding="utf-8") as e:
        json.dump(genres, e, indent=4)

    gad_all()
