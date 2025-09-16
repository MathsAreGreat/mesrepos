import re
from Mido.my_streams import MP4
from Mido.variables import monhtml


headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}


def saves(u, anime=None, nb=0):
    """Extracts episode details and updates animeup.json."""
    info = {"url": u}
    soup = monhtml(u)

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
    z = "END" if "اخيرة" in t else None

    shortlink = soup.find(rel="shortlink")
    ID = shortlink.get("href").split("=")[-1] if shortlink else None

    mal_link = soup.find(class_="anime-mal")
    mal = re.findall(r"[0-9]+", mal_link.get("href"))[-1] if mal_link else 0

    info.update({"ID": ID, "mal": mal, "ep": ep, "anime": anime, "z": z, "links": {}})

    monform = soup.find("form", method="POST")
    if monform:
        infoz = {
            e["name"]: e["value"]
            for e in monform.find_all("input")
            if "name" in e.attrs and "value" in e.attrs
        }
        action = "/".join(
            e for e in monform["action"].strip().split("/") if "\\" not in e
        )
        headers["Referer"] = action
        print(action)
        sp = monhtml(action, infoz, headers)

        monform = sp.find("form", method="POST")
        if monform:
            infoz = {
                e["name"]: e["value"]
                for e in monform.find_all("input")
                if "name" in e.attrs and "value" in e.attrs
            }
            action = "/".join(
                e for e in monform["action"].strip().split("/") if "\\" not in e
            )
            headers["Referer"] = action
            print(action)
            sp = monhtml(action, infoz)

            server_list = sp.find(id="server-list")
            if server_list:
                links = [
                    [link.get("data-ep-url"), link.text.lower().strip()]
                    for link in server_list.find_all("a")
                    if link.get("data-ep-url")
                ]

                mps = [
                    u.split("/")[-1].split("-")[-1].split(".")[0]
                    for u, t in links
                    if "mp4upload" in u
                ]
                oks = [
                    u.split("/")[-1].split("-")[-1].split(".")[0]
                    for u, t in links
                    if "ok.ru" in u
                ]

                info["links"] = {"mps": mps, "oks": oks}
    return info


p = saves(
    "https://anime4up.rest/episode/grand-blue-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1/"
)
print(p)
