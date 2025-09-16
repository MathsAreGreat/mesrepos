import chardet
from pathlib import Path
parent = Path("/home/mohamed/Videos/Torrents")


def decodes(f, k):
    print(">", f.stem)
    if k.lower() not in f.stem.lower():
        return 0
    with open(f, 'rb') as file:
        # Use chardet to automatically detect the file encoding
        result = chardet.detect(file.read())
        detected_encoding = result['encoding']
    try:
        with open(f, "r", encoding=detected_encoding) as z:
            srt = z.read()
    except UnicodeDecodeError as e:
        print("Error decoding", f, "with detected encoding",
              detected_encoding, ":", e)
    with open(f, "w", encoding="utf-8") as z:
        z.write(srt)
    return 1


for f in sorted(parent.rglob("*.srt")):
    if decodes(f, "dunki"):
        break
