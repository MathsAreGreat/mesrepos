import base64
import re
from pathlib import Path

from Mido.variables import download_m3u8_with_aria2c, monhtml

u = "https://www.fullreplays.com/friendly/club-friendlies/seoul-vs-barcelona-31-jul-2025/"


soup = monhtml(u)

title = soup.find("h1").text

titles = [hr.text for hr in soup.select(".vc_tta-panel-title")]
divs = soup.select(".linktable")

mesdatas = []
i = 1
for tt, div in zip(titles, divs):
    for tr in div.select("tr"):
        if tr.find("th"):
            continue
        if "Bet" in tr.text:
            continue
        titre, _, lang, site, wlink, *_ = tr.select("td")
        if "ok" not in site.text.lower():
            continue
        if not (link := wlink.find("a", href=True)):
            continue
        dc = re.findall(r"aH[a-z0-9]+", link.get("href"), flags=re.IGNORECASE)[-1]
        link = base64.b64decode(f"{dc}====").decode("utf-8")
        dd = (tt, titre.text, lang.text, link)
        print(i, ":", *dd, sep=" | ")
        i += 1
        mesdatas.append(dd)

pt = Path("/home/mohamed/Videos/Matches/SoccerFull")
nb = int(input("Choose : ")) - 1

ch, half, lang, url = mesdatas[nb]
t = f"[{title}].[{half}].[{ch} - {lang}].[%(height)sp].mp4"
download_m3u8_with_aria2c(url, pt / t, "https://ok.ru/")
