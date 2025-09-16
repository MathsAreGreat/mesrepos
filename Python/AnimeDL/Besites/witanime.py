import base64
import json
import re
import requests
from bs4 import BeautifulSoup

# Create a session for all requests
sess = requests.session()
sess.headers = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
}

# Load witanimes data from JSON
try:
    with open("Backups/witanimes.json", "r") as f:
        witanimes = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as err:
    print("Error loading witanimes.json:", err)
    witanimes = {}


def get_links(soup, str_id):
    """
    Extracts and decodes base64-encoded links from a given element ID in the soup.
    """
    element = soup.find(id=str_id)
    if not element:
        return []

    try:
        raw_data = re.findall(r"\[.+\]", element.text)[0]
        urls = json.loads(raw_data)
        return [base64.b64decode(u).decode("utf-8")[:-10] for u in urls]
    except (IndexError, json.JSONDecodeError, base64.binascii.Error):
        return []


def monhtml(url, ref=None, data=None):
    """
    Fetches and parses an HTML page using requests and BeautifulSoup.
    """
    if not ref:
        ref = "/".join(url.split("/")[:3])

    try:
        response = sess.post(url, data=data) if data else sess.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Request error: {e}")
        return BeautifulSoup("", "html.parser")

    encoding = (
        response.encoding
        if "charset" in response.headers.get("content-type", "").lower()
        else None
    )
    return BeautifulSoup(response.content, "html.parser", from_encoding=encoding)


def wits(url, anime, eps=False):
    """
    Extracts episode links and video host details for a given anime.
    """
    soup = monhtml(url)
    if eps:
        episodes_list = soup.find(id="ULEpisodesList")
        if not episodes_list:
            return []

        episodes = []
        for link in episodes_list.find_all("a"):
            onclick_text = link.get("onclick", "")
            episode_numbers = re.findall(r"[0-9]+", link.text)
            episode_id = re.findall(r"[a-z0-9]+", onclick_text, flags=re.IGNORECASE)

            if not episode_numbers or not episode_id:
                continue

            ep_number = int(episode_numbers[-1])
            encoded_link = base64.b64decode(f"{episode_id[-1]}=====").decode("utf-8")
            episodes.append((f"{ep_number:02}", wits(encoded_link, anime)))

        return [
            (ep, data) for ep, data in episodes if not witanimes.get(f"{anime}-{ep}")
        ]

    links = {}
    dlinks = get_links(soup, "t-odc-js-extra") + get_links(soup, "d-l-js-extra")

    for url in sorted(set(dlinks)):  # Remove duplicate links
        if not url.strip():
            continue

        url = url.replace("//https", "")
        try:
            domain = url.split("/")[2].split(".")[-2]
            key = re.findall(r"[0-9a-z]+", url, flags=re.IGNORECASE)[-1]
            links[key] = domain
        except IndexError:
            continue  # Skip invalid links

    return {
        "oks": [k for k, v in links.items() if v == "ok"],
        "mps": [k for k, v in links.items() if v == "mp4upload"],
        "dms": [k for k, v in links.items() if v == "dailymotion"],
        "vds": [k for k, v in links.items() if v == "videa"],
    }


def witing(okanime, name):
    """
    Extracts and saves episode links for a given anime.
    """
    print("Witanimes :")
    episode_data = wits(okanime, name, True)

    for ep, links in episode_data:
        code = f"{name}-{ep}"
        witanimes[code] = {"links": links}
        print("Witanime :", code)

    with open("Backups/witanimes.json", "w") as f:
        json.dump(witanimes, f, indent=4)

    return witanimes


if __name__ == "__main__":
    p0 = [
        "550d0c16",
        "5e161543425e1a491640111f0f5d500c57040841544a56090c1800580e5d1b1407045045415d591c56000a5d56401b400320365a45055b0f0c5248",
        "1904085f54",
        "03264a6062206c4d24674d005113672118180843",
    ]
    u = "W3siZCI6WzEwLDY4LDY2LDI4LDQwLDgzLDY0LDE1LDc1LDMxXSwiayI6Ik1BPT0iLCJ2IjoiTnpZME5BPT0iLCJ4IjpbMzAsMjA0LDE5OCw4NCwxMjAsMjQ5LDE5Miw0NSwyMjUsOTNdfSx7ImQiOls2NywyMSw0MSwyOSwyNyw2Nyw1NiwyMywxMCwxOV0sImsiOiJPQT09IiwidiI6Ik5UZzFOdz09IiwieCI6WzIwMSw2MywxMjMsODcsODEsMjAxLDE2OCw2OSwzMCw1N119LHsiZCI6WzQzLDI5LDMwLDE1LDIzLDMyLDEwLDQyLDI5LDg0XSwiayI6Ik5nPT0iLCJ2IjoiTnpJMU1RPT0iLCJ4IjpbMTI5LDg3LDkwLDQ1LDY5LDk2LDMwLDEyNiw4NywyNTJdfSx7ImQiOls3Miw1OCw0MywzOSw2MCwxMCw2Nyw3NiwzMSw1Nl0sImsiOiJOUT09IiwidiI6Ik16Y3dOUT09IiwieCI6WzIxNiwxNzQsMTI5LDExNywxODAsMzAsMjAxLDIyOCw5MywxNjhdfSx7ImQiOls4MSwzNyw2OSwyOSw0Miw2NCw1NywxMCw1Miw1M10sImsiOiJOdz09IiwidiI6Ik5EY3dPUT09IiwieCI6WzI0MywxMTEsMjA3LDg3LDEyNiwxOTIsMTcxLDMwLDE1NiwxNTldfV0="
    print(base64.b64decode(f"{u}========").decode("utf-8"))
