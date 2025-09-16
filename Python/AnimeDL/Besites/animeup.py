import json
import re
import requests
from Besites.variables import monhtml

# Create a single session for all requests
sess = requests.session()
sess.headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}

# Load animeup data from JSON
try:
    with open("Backups/animeup.json", "r") as f:
        animeup = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    animeup = {}


def saves(u, anime=None, nb=0):
    """Extracts episode details and updates animeup.json."""
    info = {"url": u}
    soup = monhtml(sess, u)

    title_element = soup.find("h3")
    if not title_element:
        return None

    t = title_element.text

    anime_link = soup.find(class_="anime-page-link")
    if not anime and anime_link and anime_link.a:
        anime = anime_link.a.get("href").split("/")[-2]

    episode_numbers = re.findall(r"([0-9]+)", t)
    if not episode_numbers:
        return None

    number = int(episode_numbers[-1]) + nb
    ep = str(number).zfill(2)
    code = f"{anime}-{ep}"

    if code in animeup:
        return animeup[code]

    z = "END" if "اخيرة" in t else None

    shortlink = soup.find(rel="shortlink")
    ID = shortlink.get("href").split("=")[-1] if shortlink else None

    mal_link = soup.find(class_="anime-mal")
    mal = re.findall(r"[0-9]+", mal_link.get("href"))[-1] if mal_link else 0

    info.update({"ID": ID, "mal": mal, "ep": ep,
                "anime": anime, "z": z, "links": {}})

    monform = soup.find("form", method="POST")
    if monform:
        infoz = {e["name"]: e["value"] for e in monform.find_all(
            "input") if "name" in e.attrs and "value" in e.attrs}
        action = "/".join(
            e for e in monform["action"].strip().split('/') if "\\" not in e)
        sp = monhtml(sess, action, action, infoz)

        monform = sp.find("form", method="POST")
        if monform:
            infoz = {e["name"]: e["value"] for e in monform.find_all(
                "input") if "name" in e.attrs and "value" in e.attrs}
            action = "/".join(
                e for e in monform["action"].strip().split('/') if "\\" not in e)
            sp = monhtml(sess, action, action, infoz)

            server_list = sp.find(id="server-list")
            if server_list:
                links = [
                    [link.get("data-ep-url"), link.text.lower().strip()]
                    for link in server_list.find_all("a")
                    if link.get("data-ep-url")
                ]

                mps = [u.split("/")[-1].split("-")[-1].split(".")[0]
                       for u, t in links if "mp4upload" in u]
                oks = [u.split("/")[-1].split("-")[-1].split(".")[0]
                       for u, t in links if "ok.ru" in u]

                info["links"] = {"mps": mps, "oks": oks}

    animeup[code] = info

    # Save to file with better readability
    with open("Backups/animeup.json", "w") as f:
        json.dump(animeup, f, indent=4)

    return info


# Mapping for specific anime corrections
infos = {
    "kami-no-tou-koubou-sen": ["kami-no-tou-ouji-no-kikan", 13],
    "%d8%b7%d9%88%d9%83%d9%8a%d9%88-%d8%b1%d9%8a%d9%81%d9%86%d8%ac%d8%b1%d8%b2-%d9%85%d8%aa%d8%b1%d8%ac%d9%85": [
        "tokyo-revengers-season-1",
        0,
    ],
}


def uping(anime4up):
    """Processes episodes from a given anime4up page and updates animeup.json."""
    if "http" not in anime4up:
        return anime4up, {}

    soup = monhtml(sess, anime4up)
    name = anime4up.split("/")[-2]
    nb = infos.get(name, [name, 0])[1]

    print("Anime4ups :")
    for e in soup.find_all(class_="episodes-card-title"):
        LINK = e.find("a")
        if not LINK or not LINK.get("href"):
            continue

        url = LINK.get("href")
        print(">", url)

        episode_numbers = re.findall(r"([0-9]+)", LINK.text)
        if not episode_numbers:
            continue

        number = int(episode_numbers[-1]) + nb
        ep = str(number).zfill(2)
        code = f"{name}-{ep}"

        if code in animeup:
            continue

        saves(url, name, nb)

    return name, animeup
