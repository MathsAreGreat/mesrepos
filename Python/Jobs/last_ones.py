from pathlib import Path
from datetime import datetime
import sys

cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up+clear


def convert_ctime_to_readable(st):
    mt = st.st_mtime
    ct = st.st_ctime
    at = st.st_atime
    arr = [ct, at, mt]
    arr = [e for e in arr if e > 0]
    dt = min(arr)
    ctime_datetime = datetime.fromtimestamp(dt)
    readable_ctime = ctime_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return readable_ctime


def last_update(p, ext="*"):
    items = [
        (f, convert_ctime_to_readable(f.stat()))
        for f in p.glob(f"*.{ext}")
        if f.is_file()
    ]
    try:
        return max(items, key=lambda e: e[-1])
    except:
        return None


try:
    nb = int(sys.argv[1])
except:
    nb = 5
doc = "./"
parent = Path(doc)

files = [
    last_update(p)
    for p in parent.rglob('*')
    if not p.is_file()
]

files = [
    p
    for p in files
    if p
]

if files:
    files = sorted(
        files,
        key=lambda e: e[-1],
        reverse=True
    )
    for i, (f, t) in enumerate(files, start=1):
        if i > nb:
            break
        name = f.name.rsplit('.', 3)[0]
        print(">", t, ":", name)
