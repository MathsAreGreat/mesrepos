import redis
from pathlib import Path

rds = redis.Redis(host='localhost', port=6379, decode_responses=True)


ps = [
    "/home/mohamed/Music",
    "/home/mohamed/Downloads/Library",
]
for p in ps:
    for f in Path(p).rglob("*"):
        if f.is_file() and f.suffix != "part":
            c = f.stem.split("(")[-1].split(")")[0]
            if not rds.sismember("all_backups", c):
                rds.sadd("all_backups", c)

doc = Path("/home/mohamed/Downloads")
for f in doc.glob("*"):
    if f.is_file() and f.stem.startswith("tampermonkey-"):
        to = doc / "Files"
        to.mkdir(parents=True, exist_ok=True)
        f.rename(to / f.name)

doc = Path("/home/mohamed/Downloads/Files")
for f in doc.glob("*"):
    if f.is_file():
        ext = f.suffix[1:].title()
        to = doc / f"{ext}s"
        to.mkdir(parents=True, exist_ok=True)
        f.rename(to / f.name)

