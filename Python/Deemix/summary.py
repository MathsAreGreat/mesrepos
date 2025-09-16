import hashlib
import json
import pickle
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import chardet
from mutagen.id3 import ID3
from mutagen.id3._frames import APIC, COMM, TALB, TCON, TIT2, TPE1, TPE2, USLT

try:
    with open("art_genra.json") as f:
        arts_genra = json.load(f)
except Exception as e:
    print("Error art_genra.json", e)
    arts_genra = {}


def remove_empty_dirs(root_path):
    root = Path(root_path)
    while True:
        empty_dirs = [
            d
            for d in sorted(root.rglob("*"), reverse=True)
            if d.is_dir() and not any(d.iterdir())
        ]
        if not empty_dirs:
            break  # Stop when no empty directories remain

        for doc in empty_dirs:
            try:
                doc.rmdir()
            except OSError:
                # Ignore directories that cannot be removed (e.g., permission issues)
                continue


def cryypt(file_name):
    with open(file_name, "rb") as file_obj:
        file_contents = file_obj.read()
        md5_hash = hashlib.md5(file_contents).hexdigest()
    return f"=={md5_hash}"


def gad(f):
    ID = f.stem.split("(")[-1].split(")")[0]
    with open(f"/home/mohamed/Documents/datas/Deemix/{ID}.dmx", "rb") as e:
        audio = pickle.load(e)
    parts = list(f.parent.parts)
    parts[parts.index("tmp")] = "Songs"
    otr = Path(*parts)
    otr.mkdir(parents=True, exist_ok=True)
    to = otr / f"{ID}.mp3"
    if to.exists():
        return 0
    dic = "/home/mohamed/Pictures/.Covers/Deemix_Covers"
    image_filename = Path(f"{dic}/{ID}.jpg")
    if image_filename.exists():
        if "APIC:" not in audio:
            with open(image_filename, "rb") as img:
                artwork = img.read()
            audio["APIC"] = APIC(3, "image/jpeg", 3, "Front cover", artwork)
    l = Path("/home/mohamed/Documents/Projects/Backups/Lyrics") / f"{ID}.lrc"
    if l.exists():
        with open(l, "r", encoding="utf-8") as z:
            t = z.read()
        try:
            del audio["USLT:"]
        except:
            print(">", ID, "No comment !", end="\r")

        audio.add(USLT(encoding=3, text=t.strip()))
    title_text = audio.getall("TIT2")[0].text[0]
    audio["TIT2"] = TIT2(encoding=3, text=f"{title_text} ({ID})")
    audio.save(f)
    f.rename(to)
    print(">", f.stem)
    return 1


def gad_files():
    print("Moving Files !", end="\r")
    ranger_files()
    print("Update Keys !", end="\r")
    gad_keys("/home/mohamed/Music/tmp")
    p = Path("/home/mohamed/Music/tmp")
    last_gad()
    files = list(p.rglob("*.mp3"))
    print("Update Files !", end="\r")
    with ThreadPoolExecutor(10) as executor:
        executor.map(gad, files)


def last_gad():
    assemble_arts("/home/mohamed/Music/Songs")
    assemble_arts("/home/mohamed/Music/MesSongs")
    for f in Path("/home/mohamed/Music/Songs").rglob("*.lrc"):
        f.rename(Path("/home/mohamed/Documents/Lyrics/Deemix_utf") / f.name)

    for f in Path("/home/mohamed/Music/Songs").rglob("*.mp3"):
        lrc_file = Path("/home/mohamed/Documents/Lyrics/Deemix_utf") / f"{f.stem}.lrc"
        if not lrc_file.exists():
            continue
        print(":)", f.stem)
        *parts, name = f.parts
        parts[parts.index("Songs")] = "MesSongs"
        doc = Path(*parts)
        doc.mkdir(parents=True, exist_ok=True)
        f.rename(doc / name)

    for f in Path("/home/mohamed/Music/MesSongs").rglob("*.mp3"):
        lrc_file = Path("/home/mohamed/Documents/Lyrics/Deemix_utf") / f"{f.stem}.lrc"
        if not lrc_file.exists():
            continue
        with open(f"/home/mohamed/Documents/datas/Deemix/{f.stem}.dmx", "rb") as e:
            audio = pickle.load(e)
        t = audio.getall("TIT2")[0].text[0]
        datas = [
            f"[ID: {f.stem}]",
            f"[Artist: {f.parent.name}]",
            f"[Genre: {f.parent.parent.name}]",
            f"[Title: {t}]",
        ]
        with lrc_file.open("r") as fl:
            data = [e.strip() for e in fl.readlines() if e.strip()]
        if "[00:00.0" not in data[0]:
            datas.append("[00:00.00]")

        datas += data
        lrc_file = (
            Path("/home/mohamed/Documents/Projects/Backups/Lyrics") / f"{f.stem}.lrc"
        )
        lyrics = "\n".join(datas)
        with lrc_file.open("w") as fl:
            fl.write(lyrics)


def gad_keys(s_path):
    p = Path(s_path)
    keys_dir = Path("/home/mohamed/Documents/datas/Deemix")
    keys_dir.mkdir(parents=True, exist_ok=True)

    for f in sorted(p.glob("*/*/*.mp3")):
        *_, g, art, _ = f.parts
        ID = f.stem.split(" ")[-1][1:-1] if " " in f.stem else f.stem
        dee_file = keys_dir / f"{ID}.dmx"
        print("::", dee_file)

        if dee_file.exists():
            with open(dee_file, "rb") as e:
                audio = pickle.load(e)
        else:
            audio = ID3(f)
            with open(dee_file, "wb") as z:
                pickle.dump(audio, z)

            cover_dir = Path("/home/mohamed/Pictures/.Covers/Deemix_Covers")
            cover_dir.mkdir(parents=True, exist_ok=True)
            image_filename = cover_dir / f"{ID}.jpg"

            if not image_filename.exists():
                try:
                    image_data = audio.getall("APIC")[0].data
                    with open(image_filename, "wb") as img_file:
                        img_file.write(image_data)
                    del audio["APIC"]
                except KeyError:
                    print(f"Warning: No APIC frame found for {f}")

            print(ID)

            # Handle Artist fields
            arts = {str(audio.getall("TPE1")[0])} if audio.getall("TPE1") else {art}

            try:
                tpe2_value = str(audio["TPE2"])
                arts.add(tpe2_value)
            except KeyError:
                pass  # No TPE2 found

            arr = [e.strip() for e in arts if art not in e]
            if arr:
                audio["TPE2"] = TPE2(encoding=3, text=", ".join(arr))

        # Update Title field
        title_text = (
            str(audio.getall("TIT2")[0].text[0]) if audio.getall("TIT2") else ""
        )
        title_text = " ".join(e for e in title_text.split(" ") if e and ID not in e)
        audio["TIT2"] = TIT2(encoding=3, text=title_text)

        # Update Metadata Fields
        audio["TPE1"] = TPE1(encoding=3, text=art)
        audio["TPE2"] = TPE2(encoding=3, text=art)
        audio["TCON"] = TCON(encoding=3, text=g)
        audio["COMM"] = COMM(encoding=3, text=f"{ID}{cryypt(f)}")
        # Save Updates
        audio.save(f)
        with open(dee_file, "wb") as z:
            pickle.dump(audio, z)


def ranger_files():
    p = Path("/home/mohamed/Music/deemix Music")
    to = Path("/home/mohamed/Documents/Lyrics/Deemix")
    to.mkdir(parents=True, exist_ok=True)
    for f in p.glob("*.mp3"):
        art = f.stem.split("-")[0].strip()
        gr = arts_genra.get(art, "Arabic")
        print(f)
        doc = f.parent.parent / f"tmp/{gr}" / art
        doc.mkdir(parents=True, exist_ok=True)
        f.rename(doc / f.name)
    for f in p.rglob("*.lrc"):
        k = f.stem.split(" ")[-1][1:-1]
        fto = to / f"{k}.lrc"
        if fto.exists():
            f.unlink()
            print("Remove", f)
        else:
            f.rename(fto)
    p = Path("/home/mohamed/Documents/Lyrics/Deemix")
    to = Path("/home/mohamed/Documents/Lyrics/Deemix_utf")
    to.mkdir(parents=True, exist_ok=True)
    for f in sorted(p.glob("*.lrc")):
        name = f.stem.split("(")[-1].split(")")[0]
        with open(f, "rb") as file:
            # Use chardet to automatically detect the file encoding
            result = chardet.detect(file.read())
            detected_encoding = result["encoding"]
        try:
            with open(f, "r", encoding=detected_encoding) as z:
                t = z.read()
        except UnicodeDecodeError as e:
            print(
                "Error decoding", f, "with detected encoding", detected_encoding, ":", e
            )
            continue
        fn = to / f"{name}.lrc"
        with open(fn, "w", encoding="utf-8") as z:
            z.write(t)
    for f in sorted(to.glob("*.lrc.lrc")):
        otr = f.with_name(f.stem)
        if otr.exists():
            otr.unlink()
        f.rename(otr)


def assemble_arts(root_path):
    root = Path(root_path)
    for f in root.rglob("*.mp3"):
        *_, gr, ar, _ = f.parts
        arts_genra[ar] = gr
    with open("art_genra.json", "w") as f:
        json.dump(arts_genra, f)


if __name__ == "__main__":
    import shutil

    mdx_path = Path("/home/mohamed/Documents/datas/Deemix")
    lrc_path = Path("/home/mohamed/Documents/Lyrics/Deemix_utf")
    mp3_path = Path("/home/mohamed/Music")
    infos = {}
    uniques = {}
    for f in mdx_path.glob("*"):
        k = f.stem
        with f.open("rb") as e:
            audio = pickle.load(e)
        t = audio.getall("TIT2")[0].text[0]
        if t not in infos:
            infos[t] = []
        infos[t].append(k)

    mp3_files = {f.stem: f for f in mp3_path.rglob("*.mp3")}

    for k, v in infos.items():
        if len(v) != 2:
            continue
        c, ID = sorted(v, key=len, reverse=True)
        if len(c) < 15:
            continue
        if ID in mp3_files and c in mp3_files:
            print("X", c, ID)
            mp3_files[c].unlink()
        lrc_file = lrc_path / f"{c}.lrc"
        dee_file = lrc_path / f"{ID}.lrc"
        if not lrc_file.exists() or dee_file.exists():
            continue
        shutil.copy(lrc_file, dee_file)
        print("=>", ID)

    for k, v in mp3_files.items():
        if len(k) < 15:
            continue
        print("=>", v)
