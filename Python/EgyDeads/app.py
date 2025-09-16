from pathlib import Path
import re
from Mido.variables import get_m3u8, get_segments, monhtml, vid_dwn, run_tasks, combine_vids
import redis

seasons = {
    "الاول": "01",
    "الاول": "01",
    "الثاني": "02",
    "الثالث": "03",
    "الرابع": "04",
    "الخامس": "05",
    "السادس": "06",
    "السابع": "07",
    "الثامن": "08",
    "التاسع": "09",
    "العاشر": "10"
}

try:
    rds = redis.Redis(host='localhost', port=6379, decode_responses=True)
except:
    exit()


def my_segs(link):
    ml = get_m3u8(link)
    uri = re.findall(r"http[^\"']+", ml)[0]
    return get_segments(uri)


def egybest(c, name, site="EgyDead"):
    chemin = f"Library/{site}/Seasons"
    zed = f"({c})"
    ova = "E"
    name = name.replace("حقلة", "حلقة").replace(":", " ").replace("-", " ")
    if "الحلقة" in name:
        if "الخاصة" in name:
            ova = "OVA"
        if "خيرة" in name:
            zed = f"END.({c})"
        test = name.split("الحلقة")[0].split("الموسم")[0]
        doc = test.strip().title()

        for k, v in seasons.items():
            name = name.replace(k, v)
        ep = re.findall(r"الحلقة [^0-9]*[0-9\.]+", name)
        sn = re.findall(r"الموسم [^0-9]*[0-9]+", name)
        if ep:
            doc = re.sub(r"[^0-9a-z&\.]+", r" ", doc, flags=re.IGNORECASE)
            enb = re.sub(r"[^0-9\.]", r"", ep[0]).zfill(2)
            try:
                snb = re.sub(r"[^0-9]", r"", sn[0]).zfill(2)
                snb = f"S{snb}"
            except:
                snb = "S01"
            doc = doc.strip().title()
            name = doc.replace(":", "")
            name = re.sub(r"\s+", r" ", name)
            name = name.replace(" ", ".")
            doc = doc.replace(" ", ".")
            doc = f"{chemin}/{doc}/{snb}"
            fn = f"[{site}].{name}.{snb}.{ova}{enb}.{zed}"
            return doc, fn
    chemin = f"Library/{site}/Movies"
    name = re.sub(r"[^a-z0-9]", r" ", name, flags=re.IGNORECASE)
    ns = name.split(' ')
    name = ".".join(e for e in ns if e).title()
    return chemin, f"[{site}].{name}.{zed}"


headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://egydead.fyi/",
}


def saves(u):
    soup = monhtml(u, {"View": "1"}, headers)
    uri = soup.select_one("[rel='shortlink']")
    c = uri.get("href").split("=").pop()
    if rds.sismember("backup:egydead", c):
        return []
    name = soup.select_one("title").text
    ds, dt = egybest(c, name)
    doc = f"{ds}/{dt}"
    uri = soup.select_one("a.ser-link")
    link = uri.get("href")

    segs = my_segs(link)
    return [
        (doc, uri, tn, headers)
        for uri, tn in segs
    ]


u = "https://egydead.fyi/%d9%85%d8%b4%d8%a7%d9%87%d8%af%d8%a9-%d9%81%d9%8a%d9%84%d9%85-escape-room-2-2021-%d9%85%d8%aa%d8%b1%d8%ac%d9%85/"
u = "https://egydead.fyi/%d9%85%d8%b4%d8%a7%d9%87%d8%af%d8%a9-%d9%81%d9%8a%d9%84%d9%85-snatch-2000-%d9%85%d8%aa%d8%b1%d8%ac%d9%85/"
u = "https://egydead.fyi/%d9%85%d8%b4%d8%a7%d9%87%d8%af%d8%a9-%d9%81%d9%8a%d9%84%d9%85-sound-of-metal-2019-%d9%85%d8%aa%d8%b1%d8%ac%d9%85/"
datas = saves(u)
nb = 1

print(len(datas), "items !")
while nb:
    run_tasks(vid_dwn, datas, 25)
    nb = combine_vids("Library")

for f in Path("Library").rglob("*.mp4"):
    c = f.stem.split(".")[-1][1:-1]
    rds.sadd("backup:egydead", c)
    fn = Path("/home/mohamed/Downloads", *f.parts)
    fn.parent.mkdir(parents=True, exist_ok=True)
    f.rename(fn)

nb = 1
while nb:
    nb = 0
    for doc in Path("Library").rglob("*"):
        try:
            doc.rmdir()
            nb += 1
        except:
            pass
