import webbrowser
from pathlib import Path
from time import sleep

parent = Path("/home/mohamed/Downloads/Library")


for f in parent.rglob("*.aria2"):
    brand = f.with_name(f.stem.rsplit(".part", 1)[0])
    f.rename(brand)

for f in parent.rglob("*.part"):
    brand = f.with_name(f.stem)
    if brand.exists():
        f.unlink()
