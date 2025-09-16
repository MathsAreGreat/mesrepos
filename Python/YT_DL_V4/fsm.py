from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from converts import alreadyexist, gad_all
from fnc import channelize, stablize, thumbnaudio

Path("Files").mkdir(parents=True, exist_ok=True)


cs = {
    "PLMF0Z3Vm69Ze2MrCAZ4xY1AIItTfqrUfo": "charho",
    "PLdDw-NyVFhQNTEtUJ0liL9DvxUrMrtC7T": "Azraq",
    "PLZxRWV0g4J7-kb5kQofee8kJk0fiT0-Sv": "Shoatt",
    "PLqjTpVm4mC2ZZLls_mfeRHe3NkJIUsR6I": "karakib",
    "PLIE9FB6PjOw0gmw3SapabStgNCUj2gB-c": "Studio 2",
    "PL6J_QBkhNBQhfWVR8g4Zo-yoahLbtESd-": "Review 2",
}

mx = 5

ds = [
    ("abdullatif1", mx, "|قصص"),
    ("7akawi-AA", 0, "|قصص"),
    ("AbulSadiq", mx),
    ("DarkSideHimself", mx),
    ("Badr3", mx),
    ("islam_sobhi", mx, "سورة|سور"),
    ("9li9", mx, "سورة|سور"),
    ("FahmyProductions", mx, "علينا|جت علينا"),
    ("m3kamele7trami", mx, "احترامي|مع كامل احترامي"),
    ("Alaraby-Tube", mx, "حضارة|في الحضارة"),
    ("Filmolokhia", mx, "فيلملوخية"),
    ("TheYahyaAzzam", mx, "قصة|قــــصة|قصة مش مهم تسمعها"),
    ("EslamAdel", mx, "كريستي|أجاثا كريستي", "شيرلوك|شيرلوك هولمز"),
    (
        "storiesbelaraby",
        mx,
        "كريستي|أجاثا كريستي",
        "شيرلوك|شيرلوك هولمز",
        "توفيق|أحمد خالد توفيق",
        "نجيب|نجيب محفوظ",
    ),
]

zds = [(c, *el.split("|")) for c, _, *d in ds if d for el in d]

ds += [(k, 0) for k in cs]


with ThreadPoolExecutor(2) as executor:
    executor.map(channelize, ds)


zs = {}

for c, *el in zds:
    if len(el) == 1:
        el = el[0]
        zs[f"{c}=={el}"] = el
        continue
    *ks, v = el
    for k in ks:
        zs[f"{c}=={k}"] = v

stablize(zs)

datas = alreadyexist()

with ThreadPoolExecutor(2) as executor:
    executor.map(thumbnaudio, datas)

to = Path("/home/mohamed/Documents/Youtube/IDs")
for f in Path("Files").glob("*.json"):
    fn = to / f.name
    if fn.exists():
        f.unlink()
        continue
    fn.parent.mkdir(parents=True, exist_ok=True)
    f.rename(fn)


for fn in Path("/home/mohamed/Documents/datas").glob("*"):
    if not fn.is_file():
        continue
    if fn.stat().st_size > 10:
        continue
    fn.unlink()

gad_all()
