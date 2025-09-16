from pathlib import Path

parent = Path("Music/Songs")
for f in parent.rglob('*mp3'):
    k = f.stem.split("(")[-1].split(")")[0]
    to = f.with_stem(k)
    f.rename(to)
