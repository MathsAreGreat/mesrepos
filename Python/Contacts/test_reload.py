from datetime import datetime
import hashlib
from pathlib import Path

parent = Path("/home/mohamed/Pictures/.Covers/Perso")
to = Path(parent, "WhatsApp", "Solo")


def convert_time_to_readable(st):
    mt = st.st_mtime
    ct = st.st_ctime
    at = st.st_atime
    arr = [ct, at, mt]
    arr = [e for e in arr if e > 0]
    dt = min(arr)
    ctime_datetime = datetime.fromtimestamp(dt)
    readable_ctime = ctime_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    return readable_ctime


def mdfy(f):
    ext = f.suffix[1:]
    s = "4"
    if ext == "jpg":
        s = "1"
    elif ext == "jpeg":
        s = "2"
    with open(f, "rb") as fl:
        data = fl.read()
    crypt = hashlib.md5(data).hexdigest()
    sz = f.stat().st_size
    return f"{crypt}{sz}{s}.{ext}"


# while True:

#     for doc in parent.rglob("*"):
#         try:
#             doc.rmdir()
#             doc.stat
#             print(">", doc.stem)
#         except:
#             if not doc.suffix:
#                 continue
#             if "kol" not in str(doc.parent):
#                 continue
#             if "Solo" in str(doc.parent):
#                 continue
#             parts = doc.parts[:-2]
#             to = Path(parent, "WhatsApp", "Solo")
#             to.mkdir(parents=True, exist_ok=True)
#             fn = to / mdfy(doc)
#             doc.rename(fn)
#     sleep(1)

for f in to.rglob("*"):
    if f.is_file() and "_" not in f.stem:
        st = f.stat()
        stem = convert_time_to_readable(st)
        fn = f.with_stem(stem)
        f.rename(fn)
