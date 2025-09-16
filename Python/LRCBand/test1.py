import re
from pathlib import Path

from mutagen.id3 import ID3, USLT, ID3NoHeaderError

mp3_dir = Path("/home/mohamed/Music")
bk_dir = Path("/home/mohamed/Documents/datas/LRCBand")
lrc_dir = Path("/home/mohamed/Documents/Lyrics/OSDLyrics")


def update_lrcs():
    for fl in bk_dir.rglob("*.lrc"):
        base_name = fl.stem
        if re.match(r"[^0-9]", base_name):
            continue
        fl.rename(lrc_dir / fl.name)


def embed_lyrics(mp3_path: Path, lyrics_text: str):
    try:
        audio = ID3(mp3_path)
    except ID3NoHeaderError:
        audio = ID3()

    audio.delall("USLT")
    audio.add(USLT(encoding=3, lang="eng", desc="desc", text=lyrics_text))
    audio.save(mp3_path)
    print(f"✅ Lyrics embedded into {mp3_path.name}")


def check_and_add_lyrics():
    exeps = []
    for mp3_file in mp3_dir.rglob("*.mp3"):
        base_name = mp3_file.stem
        try:
            audio = ID3(mp3_file)
            # if any(frame for frame in audio.getall("USLT")):
            #     # print(f"✔️ {mp3_file.name} already has lyrics.")
            #     continue
        except ID3NoHeaderError:
            pass  # proceed to add lyrics

        lrc_file = lrc_dir / f"{base_name}.lrc"
        if lrc_file.exists() and lrc_file.stat().st_size > 2000:
            lyrics_text = lrc_file.read_text(encoding="utf-8")
            embed_lyrics(mp3_file, lyrics_text)
        elif "" in mp3_file.parent.name:
            # print(f"⚠️ No lyrics {mp3_file}.")
            t = f"{audio.getall('TIT2')[0]}"
            p = mp3_file.parent.name
            exeps.append((p, t))

    for p, t in sorted(exeps):
        print(f"⚠️ {p} : {t} .")
        print("===========================================")


def is_hindi(text):
    return any("\u0900" <= ch <= "\u097f" for ch in text)


if __name__ == "__main__":
    mp3_dir = Path("/home/mohamed/Music/Songs")
    to_dir = Path("/home/mohamed/Music/MesSongs")
    lrc_dir = Path("/home/mohamed/Documents/Lyrics/Deemix_utf")
    for mp3_path in mp3_dir.rglob("*.mp3"):
        move = True
        lrc_path = mp3_path.with_suffix(".lrc")
        if not lrc_path.exists():
            move = False
            lrc_path = lrc_dir / lrc_path.name
        if not lrc_path.exists():
            continue
        if lrc_path.stat().st_size < 200:
            continue
        lyrics_text = lrc_path.read_text(encoding="utf-8")
        if is_hindi(lyrics_text):
            continue
        embed_lyrics(mp3_path, lyrics_text)
        *_, g, ar, fl = mp3_path.parts
        doc = to_dir / f"{g}/{ar}"
        doc.mkdir(exist_ok=True, parents=True)
        mp3_path.rename(doc / fl)
        if move:
            lrc_path.rename(lrc_dir / lrc_path.name)