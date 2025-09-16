import requests
import os
import re
import spotipy
import pickle
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.id3 import ID3, TIT2, TPE1, TPE2, TALB, TCON, TDRC, APIC, COMM
from concurrent.futures import ThreadPoolExecutor
from sprinter import sprint
from rich import print

infos = []
names = []


def hawl(f):
    name, _ = os.path.splitext(f)
    if os.path.exists(f"{name}.mp3"):
        os.remove(f)
        print(f, "is removed !")
    else:
        os.system(f'ffmpeg -i "{f}" "{name}_tmp.mp3"')
        print(f"{name}.mp3", "is extracted !")
        os.rename(f"{name}_tmp.mp3", f"{name}.mp3")


def convert():
    pth = "/home/mohamed/Music/Spotify"
    mesfiles = []
    for c, _, files in os.walk(pth):
        c = c.replace("\\", "/")
        mesfiles += [f"{c}/{f}" for f in files if f.endswith(("webm", "m4a"))]
    with ThreadPoolExecutor(10) as executor:
        executor.map(hawl, mesfiles)
    return len(mesfiles)


def audio(nbr):
    u = f"https://open.spotify.com/track/{nbr}"
    o = f"PreMp3/{nbr}"
    cmd = f'spotify_dl -l {u} -o "{o}"'
    os.system(cmd)


def mesdatas(n="", r=""):
    p = "/home/mohamed/Documents/datas/Spotify"
    infos = {}
    names = {}
    for f in os.listdir(p):
        if f.endswith("plsptf"):
            continue
        if not f.endswith("sptf"):
            continue
        fn = os.path.join(p, f)
        with open(fn, "rb") as e:
            datas = pickle.load(e)
        if f.endswith(".albsptf"):
            for k, v in datas.items():
                if k not in infos:
                    if (
                        n.lower() in v["title"].lower()
                        and r.lower() in v["album"].lower()
                    ):
                        infos[k] = v
        elif f.endswith(".arsptf"):
            k = f.rsplit(".", 1)[0]
            names[k] = datas["name"]
    return infos, names


def getname(albms, ID):
    for item in albms:
        artis = item["artists"]
        for ar in artis:
            if ID == ar["id"]:
                return ar["name"]
    return None


def artists(ARTSs):
    print()
    print(len(ARTSs), "Artists !")
    print()
    p = "/home/mohamed/Documents/datas/Spotify"
    albs = []
    for lindex, ID in enumerate(ARTSs, start=1):
        fn = os.path.join(p, f"{ID}.arsptf")
        if os.path.exists(fn):
            with open(fn, "rb") as e:
                datas = pickle.load(e)
            albs += datas["albums"]
            continue
        lz_uri = f"spotify:artist:{ID}"
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        results = spotify.artist_albums(lz_uri)
        albms = results["items"]
        art = getname(albms, ID)
        while results["next"]:
            results = spotify.next(results)
            if not art:
                art = getname(results["items"], ID)
            albms.extend(results["items"])
        if not art:
            art = "Unknown"
        msg = f" {art} "
        print(lindex, f"{msg:=^50}")
        alb = [album["id"] for album in albms]
        albs += list(set(alb))
        with open(fn, "wb") as e:
            pickle.dump({"name": art, "albums": albs}, e)
    return albs


def playlists(ID):
    if not ID:
        return [], [], []
    pspot = "/home/mohamed/Documents/datas/Spotify"
    os.makedirs(pspot, exist_ok=True)
    fn = os.path.join(pspot, f"{ID}.plsptf")
    lz_uri = f"spotify:playlist:{ID}"
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    results = spotify.user_playlist_tracks("31ea4zcy5q7w3oaoedmyvlsi6z6u", lz_uri)
    items = [item["track"] for item in results["items"]]
    i = 1
    while results["next"]:
        print(">>", i)
        i += 1
        results = spotify.next(results)
        items += [item["track"] for item in results["items"]]
    album = [it["album"]["id"] for it in items]
    track = [it["id"] for it in items]
    artist = []
    for item in items:
        artist += [it["id"] for it in item["artists"]]
    infos = {
        "track": [ar for ar in set(track)],
        "album": [ar for ar in set(album)],
        "artist": [ar for ar in set(artist)],
    }
    with open(fn, "wb") as e:
        pickle.dump(infos, e)
    return infos["artist"], infos["album"], infos["track"]


def albums(IDs):
    print()
    print(len(IDs), "Albums !")
    print()
    pspot = "/home/mohamed/Documents/datas/Spotify"
    os.makedirs(pspot, exist_ok=True)

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    for ID in IDs:
        fn = os.path.join(pspot, f"{ID}.albsptf")
        if not os.path.exists(fn):
            lz_uri = f"spotify:album:{ID}"
            results = spotify.album(lz_uri)
            datas = {}
            pl = results["name"]
            release_date = results["release_date"]
            print(">", pl)
            u = results["images"][0]["url"]
            for track in results["tracks"]["items"]:
                if track["type"] != "track":
                    continue
                c = track["id"]
                name = re.sub(r'[:"]', r"", track["name"]).strip()
                name = re.sub(r"/", r" ", name).strip()
                name = re.sub(r"\s+", r" ", name).strip()
                artist = {e["id"]: e["name"] for e in track["artists"]}
                for ky, vy in artist.items():
                    an = os.path.join(pspot, f"{ky}.arsptf")
                    if not os.path.exists(an):
                        with open(an, "wb") as e:
                            pickle.dump({"name": vy}, e)
                datas[c] = {
                    "title": name,
                    "poster": u,
                    "album": pl,
                    "release_date": release_date,
                    "artist": list(artist),
                }
            with open(fn, "wb") as e:
                pickle.dump(datas, e)
            fn = os.path.join(pspot, f"{ID}.alsptf")
            if os.path.exists(fn):
                os.remove(fn)
    return 1


def dwnld(ids):
    print()
    print(len(ids), "Tracks !")
    print()
    with ThreadPoolExecutor(5) as executor:
        executor.map(audio, ids)
    sprint("Converting Files !")
    c = convert()
    while c:
        c = convert()

    currentPath = "PreMp3"
    infos, names = mesdatas()
    genre = "Indefined"

    def tagging(dd):
        c, f = dd
        file_path = f"{c}/{f}"
        ID = c.split("PreMp3/")[-1].split("/")[0]
        v = infos[ID]
        doc = v["album"]
        doc = doc.replace("?", "")
        doc = re.sub(r"[/:#!\-\.]+", r" - ", doc)
        doc = re.sub(r"\s+", r" ", doc)
        album = re.sub(r"[^a-z0-9ا-ي]+$", r"", doc)

        artist = [names[e] for e in v["artist"] if e in names]
        ar = "Unknown"
        artist = [e for e in artist if e != "Unknown"]
        if artist:
            ar = artist[0]
            ar = str(ar).title()
        title = v["title"].title()
        title = title.replace("?", "")
        title = re.sub(r"[:#!\-\.]+", r" - ", title)
        title = re.sub(r"\s+", r" ", title)
        albumartist = ar
        NB_ART = len(artist)
        if NB_ART > 1:
            albumartist = ", ".join(e for e in artist[1:])

        u = v["poster"]
        cover = requests.get(u)
        audio = ID3()
        cm = COMM(encoding=3, text=ID)
        audio["COMM"] = cm
        audio["TCON"] = TCON(encoding=3, text=genre)
        audio["TIT2"] = TIT2(encoding=3, text=f"{title} ({ID})")
        audio["TPE1"] = TPE1(encoding=3, text=ar)
        audio["TALB"] = TALB(encoding=3, text=album)
        audio["TPE2"] = TPE2(encoding=3, text=albumartist)
        year = v["release_date"].split("-")[0]
        audio["TDRC"] = TDRC(encoding=3, text=year)
        fn = dwn_jpeg(ID, u)
        with open(fn, "rb") as cover:
            audio["APIC"] = APIC(
                encoding=3,
                mime="image/jpeg",  # Replace with the appropriate MIME type if necessary
                type=3,  # 3 is for album cover
                desc="Cover",
                data=cover.read(),
            )
        audio.save(file_path)
        doc = f"Finals/{genre}/{ar}/{album}"
        os.makedirs(doc, exist_ok=True)
        os.rename(file_path, f"{doc}/{ar} - {title} ({ID}).mp3")
        print(":>", ID)
        return 1

    audios = []
    for c, _, files in os.walk(currentPath):
        audios += [(c, f) for f in files if f.endswith(".mp3")]

    sprint("Tagging Files !")

    with ThreadPoolExecutor(20) as executor:
        executor.map(tagging, audios)
    sprint("Last Tuning Files !")
    return 1


def restore(p, infos):
    print()
    print(" ================================================== ")
    print()
    for c, _, files in os.walk(p):
        for f in files:
            if f.endswith(".mp3"):
                *_, g, ar, al = c.split("/")
                if ar in infos:
                    g = infos[ar]
                    p = p.replace("Finals", "Dones")
                to = f"{p}/{g.title()}/{ar}/{al}"
                if to != c:
                    fn = f"{c}/{f}"
                    audio = ID3(fn)
                    # del audio['TCON']
                    audio["TCON"] = TCON(encoding=3, text=g.title())
                    audio.save()
                    print("^^", f)
                    os.makedirs(to, exist_ok=True)
                    os.rename(f"{c}/{f}", f"{to}/{f}")


def dwn_jpeg(k, u):
    fn = f"/home/mohamed/Pictures/.Covers/SPT_Covers/{k}.jpeg"
    if os.path.exists(fn):
        return fn
    with requests.get(u) as cover:
        with open(fn, "wb") as e:
            e.write(cover.content)
        return fn


def remove_empties(*paths):
    print()
    print(" ================================================== ")
    print()
    for p in paths:
        c = 1
        z = "download_list.log"
        while c > 0:
            c = 0
            for current, dirs, files in os.walk(p):
                current = re.sub(r"\\", r"/", current)
                if len(dirs) + len(files) == 0:
                    c += 1
                    print(">", current, "is an empty folder !")
                    os.rmdir(current)
                elif z in files:
                    os.remove(os.path.join(current, z))
                    c += 1
    print()
