import base64
import json
import re
import requests
from Besites.variables import monhtml

# Create a single session for all requests
sess = requests.session()
sess.headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}

# Load animercos data from JSON
try:
    with open("Backups/animercos.json", "r") as f:
        animercos = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    animercos = {}


def ddlink(u):
    soup = monhtml(sess, u)
    link_element = soup.find(id="link")
    return base64.b64decode(link_element["data-url"]).decode("utf-8").split("/")[-1].split("-")[-1].split(".")[0]


def okify(u):
    """Extracts mp4upload IDs and OK.ru keys from the given URL."""
    soup = monhtml(sess, u)
    d_item = soup.find(id="download")
    if not d_item:
        return [], []

    # Extract links
    links = [
        (tr.find("a")["href"], tr.find("div", class_="favicon")["data-src"])
        for tr in d_item.find_all("tr")
        if tr.find("td") and tr.find("a") and tr.find("div", class_="favicon")
    ]

    # Extract MP4 upload IDs
    mps = [
        ddlink(u)
        for u, t in links
        if "mp4upload" in t
    ]

    # Extract OK.ru keys
    form = soup.find("form", action=True)
    if not form:
        return mps, []

    lts = [
        (e.attrs, e.find(class_="server").text)
        for e in soup.find_all("a", class_="option")
        if e.find(class_="server") and "ok" in e.find(class_="server").text
    ]

    infos = [dfo(e) for e, _ in lts]
    dm = form["action"]
    keys = [
        lienize(dt, dm).split("/")[-1].split("-")[-1].split(".")[0]
        for dt in infos if lienize(dt, dm)
    ]

    return mps, keys


def dfo(e):
    """Extracts required data fields from an element."""
    datas = ["type", "post", "nume"]
    return {k: e.get(f"data-{k}", "") for k in datas} | {"action": "player_ajax"}


def lienize(dt, dm):
    """Sends a POST request to fetch the embed URL from OK.ru."""
    r = sess.post(f"{dm}/wp-admin/admin-ajax.php", data=dt)
    try:
        v = r.json().get("embed_url", "")
        if "ok.ru" in v:
            return re.findall(r"http[^'\"]+", v)[-1]
    except (json.JSONDecodeError, IndexError):
        pass
    return None


def ercoing(animerco, name):
    """Processes episodes from a given anime page and updates animercos.json."""
    print("Animercos :")
    soup = monhtml(sess, animerco)

    eps = []
    for link in soup.find_all("a", class_="read-btn"):
        title = link.get("title")
        if not title:
            continue
        numbers = re.findall(r"[0-9]+", title)
        if numbers:
            eps.append([numbers[0], link["href"]])

    episodes = {k.zfill(2): u for k, u in eps}

    for ep, u in episodes.items():
        code = f"{name}-{ep}"
        if code in animercos:
            continue

        animercos[code] = {"links": {}}
        mps, oks = okify(u)

        print("animerco :", code)
        animercos[code]["links"]["mps"] = sorted(set(mps))
        animercos[code]["links"]["oks"] = sorted(set(oks))

    # Save to file with better readability
    with open("Backups/animercos.json", "w") as f:
        json.dump(animercos, f, indent=4)

    return animercos
