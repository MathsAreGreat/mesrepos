import requests
import os
import re
import json
import sys
from bs4 import BeautifulSoup

agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
sess = requests.session()

with open("infos.json", "r") as e:
    stream_info = json.load(e)

DOM = "antenasport.ru"


def basic(k):
    url = stream_info["live"]
    u = url.replace("variable_here", k)
    sess.headers = {
        "referer": f"https://{DOM}/",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    print(u)
    match = re.search(r"return\((\[.+?\])", sess.get(u).text)
    if not match:
        return None
    url = "".join(json.loads(match[1]))
    return u, url.replace("////", "//")


def monhtml(k, ref):
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "Referer": ref,
    }
    r = sess.get(k)
    encoding = (
        r.encoding if "charset" in r.headers.get("content-type", "").lower() else None
    )
    parser = "html.parser"
    return BeautifulSoup(r.content, parser, from_encoding=encoding)


def prov(nb):
    ref, u = stream_info["feed"]
    referrer = ref.replace("variable_here", nb)
    u = u.replace("variable_here", nb)
    print(f"> {u}")
    print(f"> {referrer}")
    sess.headers = {
        "referer": referrer,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    url = sess.get(u, allow_redirects=True).url
    return referrer, url


def basics(nb):
    ref, u = stream_info["premium"]
    referrer = ref.replace("variable_here", f"{nb}")
    u = u.replace("variable_here", f"{nb}")
    print(f"> {u}")
    print(f"> {referrer}")
    sess.headers = {
        "referer": referrer,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    url = sess.get(u, allow_redirects=True).url
    return referrer, url


def bases(nb):
    ref, u = stream_info["prima"]
    referrer = ref.replace("variable_here", f"{nb}")
    u = u.replace("variable_here", f"{nb}")
    print(f"> {u}")
    print(f"> {referrer}")
    sess.headers = {
        "referer": referrer,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    url = sess.get(u, allow_redirects=True).url
    return referrer, url


def choose(nb):
    print("Searching ...")
    try:
        nbr = int(nb)
        if nbr > 0:
            return basics(nbr)
        d = nb[1:]
        return bases(d)
    except Exception as err:
        print(err)
        d = nb[1:]
        if nb.startswith("="):
            return prov(d)
        if nb.startswith("-"):
            return bases(d)
        return basic(nb)


def lienize(nbr):
    u = f"https://{DOM}/{nbr}.php"
    ref = "/".join(u.split("/")[:3])
    soup = monhtml(u, ref)
    iframe = soup.iframe
    while iframe:
        ref = "/".join(u.split("/")[:3])
        u = iframe["src"]
        soup = monhtml(u, ref)
        iframe = soup.iframe
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "Referer": ref,
    }
    ref = u
    r = sess.get(u)
    us = re.findall(r'[^\'"]+m3u8', r.text)
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "Referer": ref,
    }
    url = sess.get(us[0], allow_redirects=True).url
    return re


def liveit(nb):
    dd = choose(nb)
    if not dd:
        return 0
    referrer, url = dd
    url = url.replace("playlist", "tracks-v1a1/mono")
    url = url.replace("index", "tracks-v1a1/mono")
    print(url)
    cmd = f"""vlc --loop "{url}" --http-referrer="{referrer}
        " --http-user-agent="{agent}" --adaptive-use-access --ttl -1"""
    os.system(cmd)


nb = 116
liveit(nb)
