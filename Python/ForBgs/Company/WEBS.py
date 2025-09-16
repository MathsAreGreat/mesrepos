import ast
import json
import re
from pathlib import Path
from shutil import rmtree
from time import sleep

import cloudscraper
import requests
from Mido.variables import aria_dwn, download_m3u8_with_aria2c, run_tasks

scraper = cloudscraper.create_scraper()

parent_path = "/home/mohamed/.Kindas"

rmtree("temps", True)
info_dir = Path("/home/mohamed/.Kindas/Files")

uns = [f.stem.split(".")[-1][1:-1] for f in Path(parent_path).rglob("*.mp4")]

keys = {"name", "author", "uploadDate", "thumbnailUrl", "duration"}


class HC:
    def __init__(self, k):
        self.ID = k
        self.content = None
        self.filname = info_dir / f"{k}.json"

    def vids(self, nb=0):
        url = f"https://www.hentaicity.com/search/video/{self.ID}"
        if nb > 0:
            url += f"/{nb+1}/"
        print(url)
        r = scraper.get(url)
        content = r.text
        pages = re.findall(rf"{url}/([0-9]+)/", content)
        if pages:
            ns = max(pages, key=int)
        else:
            ns = 1
        return ns, [
            t.split("-")[-1].rsplit(".", 1)[0]
            for t in re.findall(r"http[^'\"]+\.html", content)
        ]

    def save(self):
        url = f"https://www.hentaicity.com/video/vid-{self.ID}.html"
        r = scraper.get(url)
        content = r.text
        if not self.filname.exists():
            info_dir.mkdir(parents=True, exist_ok=True)
            ct = content.split("@context", 1)[-1].split(",", 1)[-1].split("<")[0]
            infos = {k: v for k, v in json.loads("{" + ct).items() if k in keys}
            infos["related"] = re.findall(
                r"http[^'\"]+-([^\-]+)\.html.+>Episode[^<]+", content
            )
            infos["thumbnailUrl"] = re.findall(r"posterImage[^a-z]+([^\"]+)", content)
            with self.filname.open("w") as fl:
                json.dump(infos, fl)

        t = re.findall(r"http[^'\"]+\.m3u8[^'\"]+", content)
        ts = r.url.split("/")[-1].split("-")
        tl = ".".join(ts[:-1])
        print(self.ID, ":", tl)
        return (
            "https://www.hentaicity.com/",
            f"{parent_path}/HCs/{tl[:60]}.({self.ID})",
            t[0],
        )

    def autres(self):
        if not self.filname.exists():
            url = f"https://www.hentaicity.com/video/vid-{self.ID}.html"
            r = scraper.get(url)
            content = r.text
            return re.findall(r"http[^'\"]+-([^\-]+)\.html.+>Episode[^<]+", content)
        with self.filname.open("r") as fl:
            infos = json.load(fl)
        return infos["related"]


class MT6TB:
    def __init__(self, k):
        self.ID = k

    def save(self):
        url = f"https://mat6tube.com/watch/-{self.ID}"
        sess = requests.Session()
        sess.headers = {
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Referer": "https://mat6tube.com/",
        }
        r = sess.get(url)
        info = re.findall(r"application/ld\+json\">([^<]+)", r.text)
        data = json.loads(info[0])
        info = re.findall(r"window.playlist = ([^;]+)", r.text)
        data.update(json.loads(info[0]))
        ts = re.findall(r"[0-9a-z]+", data["name"].lower())
        name = ".".join(e.title() for e in ts)
        info = max(data["sources"], key=lambda x: int(x["label"]))

        doc = "/home/mohamed/.Kindas/MT6tube"
        return sess.headers["Referer"], doc, info["file"], f"{name}.({self.ID}).mp4"


class MSAV:
    def __init__(self, k):
        self.ID = k.lower()
        self.filname = info_dir / f"{k}.json"

    def save(self):
        url = f"https://missav123.com/en/{self.ID}"
        r = scraper.get(url)
        content = r.text
        infos = {}
        dts = re.findall(f">404<", content)
        if dts:
            with self.filname.open("w") as fl:
                json.dump(infos, fl)
            return None
        name = re.findall(f"<title>([^<]+)", content)[0]
        print(name)
        dts = re.findall(f"og:video:([^>]+)", content)
        if dts:
            dts = [e.split('"') for e in dts]
            img = re.findall(f'https://fourhoi.com[^"]+', content)[0]
            sc = re.findall(f"eval.+split[^a-z]+", content)[0]
            print(dts)
            for e in dts:
                k = e[0]
                v = e[2]
                if k not in infos:
                    infos[k] = []
                infos[k].append(v)
            infos = {k: v[0] if len(v) < 2 else v for k, v in infos.items()}
            links = extract_links_from_eval(sc)
            infos["name"] = name
            infos["thumbnailUrl"] = img
            infos["dlink"] = links
            if not self.filname.exists():
                info_dir.mkdir(parents=True, exist_ok=True)
            with self.filname.open("w") as fl:
                json.dump(infos, fl)
            return (
                "https://missav123.com/",
                f"{parent_path}/MSAVs/{name}.({self.ID})",
                links[-1],
            )
        return None


class SPNK:
    def __init__(self, k):
        self.ID = k
        self.filname = info_dir / f"{k}.json"

    def save(self):
        url = f"https://spankbang.party/{self.ID}/video/"
        print(url)
        while True:
            r = scraper.get(url)
            content = r.text
            tl = re.findall(rf"/{self.ID}/video/[^\"]+", content)
            if tl:
                break
            print("Waiting !")
            sleep(0.3)

        if not self.filname.exists():
            info_dir.mkdir(parents=True, exist_ok=True)
            ct = content.split("@context", 1)[-1].split(",", 1)[-1].split("<")[0]
            infos = {k: v for k, v in json.loads("{" + ct).items() if k in keys}
            with self.filname.open("w") as fl:
                json.dump(infos, fl)

        tl = re.sub(
            r"[^0-9a-z]+", r".", tl[0].split("/")[-1], flags=re.IGNORECASE
        ).title()
        t = content.split("stream_data = ")[1].split(";")[0].replace("'", '"')
        js = json.loads(t)
        wanted = {k: v for k, v in js.items() if v and "m3u8" in k}
        key = list(wanted)[-1]
        uri = wanted[key][0]
        return "https://spankbang.com", f"{parent_path}/SPNKs/{tl}.({self.ID})", uri


# Function to get class by name
def use_class_by_name(name: str, k):
    if k in uns:
        return 0
    theclass = globals().get(name)
    r, f, u = theclass(k).save()
    download_m3u8_with_aria2c(u, Path(f"{f}.mp4"), r)
    return 1


# Function to get class by name
def use_direct_class_by_name(*ks):
    datas = [MT6TB(k).save() for k in ks]
    run_tasks(aria_dwn, datas)
    return 1


def extract_links_from_eval(eval_string):
    """
    Parses a JavaScript eval string, deobfuscates it, and extracts URLs.

    Args:
        eval_string: The full JavaScript "eval(function(p,a,c,k,e,d){...})" string.

    Returns:
        A list of URLs found in the deobfuscated code, or an empty list if parsing fails.
    """
    try:
        # Regex to capture the arguments of the packed function
        match = re.search(
            r"}\('(.+)',(\d+),(\d+),'([^']+)'\.split\('\|'\)", eval_string, re.DOTALL
        )
        if not match:
            return []

        p, a, c, k_str = match.groups()
        a = int(a)
        c = int(c)
        k = k_str.split("|")

    except (AttributeError, ValueError):
        # Fallback for slightly different but common formats
        try:
            # This regex is an alternative for different quoting or spacing
            match = re.search(r"}\((.+),(\d+),(\d+),(.+)\)\)", eval_string, re.DOTALL)
            if not match:
                return []

            p, a, c, k_str = match.groups()
            p = ast.literal_eval(p)  # Safely evaluate string literal
            a = int(a)
            c = int(c)
            k = ast.literal_eval(k_str)  # Safely evaluate list literal
        except (AttributeError, ValueError, SyntaxError):
            return []  # Return empty list if parsing fails

    def to_base(num, base):
        """Converts a number to a string in a given base."""
        if num < base:
            return str(hex(num)).replace("0x", "")

        # Fallback for handling alphanumeric encoding in JS
        base_chars = "0123456789abcdefghijklmnopqrstuvwxyz"
        if num < 0 or base < 2 or base > len(base_chars):
            return ""

        if num == 0:
            return "0"

        res = ""
        while num > 0:
            res = base_chars[num % base] + res
            num = num // base
        return res

    # Perform the substitution to deobfuscate the string
    # We iterate downwards as per the original JS logic
    for i in range(c - 1, -1, -1):
        if i < len(k) and k[i]:
            # Generate the token to be replaced
            token = to_base(i, a)
            # Replace all occurrences of this token as a whole word
            p = re.sub(r"\b" + re.escape(token) + r"\b", k[i], p)

    # Use a regex to find all URL-like strings in the result
    return sorted(set(re.findall(r'https?://[^\'"]+m3u8', p)))


def dwn_img(f):
    pi = Path("/home/mohamed/.Kindas/IMGs")
    pi.mkdir(parents=True, exist_ok=True)
    with f.open("r") as fl:
        info = json.load(fl)
    thumbnailUrl = info.get("thumbnailUrl")
    if not thumbnailUrl:
        return 0

    while isinstance(thumbnailUrl, list):
        thumbnailUrl = thumbnailUrl[0]
    info["thumbnailUrl"] = thumbnailUrl

    with f.open("w") as fl:
        json.dump(info, fl, indent=4)
    print(f)
    ex = thumbnailUrl.split(".")[-1]
    ts = re.findall(r"[0-9a-z]+", info["name"], flags=re.IGNORECASE)
    name = ".".join(ts)
    fr = pi / f"{name}.{f.stem}.{ex}"
    if fr.exists():
        return 1
    with fr.open("wb") as im:
        r = requests.get(thumbnailUrl, stream=True)
        im.write(r.content)
    print(info["name"])
    return 1


def thumbin():
    pu = Path("/home/mohamed/.Kindas/Files")
    pu.mkdir(parents=True, exist_ok=True)

    run_tasks(dwn_img, [(f,) for f in pu.glob("*")], 1)


if __name__ == "__main__":
    uns = [
        f.stem.split(".")[-1][1:-1]
        for f in Path("/home/mohamed/.Kindas/HCs").rglob("*mp4")
    ]
    for k in uns:
        HC(k).save()
    thumbin()
