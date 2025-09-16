import requests
import os
import re
from bs4 import BeautifulSoup

agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'
sess = requests.session()
sess.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
}

chs = ["https://sportsonline.so/channels/pt/btv.php"]
chs += [
    f"https://sportsonline.so/channels/pt/sporttv{i+1}.php"
    for i in range(5)
]
chs += [
    f"https://sportsonline.so/channels/pt/eleven{i+1}.php"
    for i in range(3)
]
chs += [
    f"https://sportsonline.so/channels/hd/hd{i+1}.php"
    for i in range(10)
]
chs += [
    f"https://sportsonline.so/channels/bra/br{i+1}.php"
    for i in range(4)
]

chs = {
    u.split("/")[-1].split('.')[0]: u
    for u in chs
}


def monhtml(k, ref=None):
    if ref:
        sess.headers['Referer'] = ref
    r = sess.get(k)
    encoding = r.encoding if 'charset' in r.headers.get(
        'content-type', '').lower() else None
    parser = 'html.parser'
    return BeautifulSoup(r.content, parser, from_encoding=encoding)


def jdid(url):
    ref = "/".join(url.split("/")[:3])
    soup = monhtml(url, ref)
    url = soup.iframe["src"]
    r = sess.get(url)
    val = [e for e in r.text.split(
        '|') if re.search(r"^[0-9a-z]+$", e.lower())]
    v = url.split("/")
    m3u = v[-1]
    ref = "/".join(v[:3])
    _, e, s, ht, wst, *_ = [e for e in val if len(e) > 9 and not e.startswith(
        "set") and "start" not in e.lower() and "max" not in e.lower()]
    if wst.startswith('cdn'):
        return ref, f"https://{ht}.{wst}.net:8443/hls/{m3u}.m3u8?s={s}&e={e}"
    print(f"https://{ht}.{wst}.net:8443/hls/{m3u}.m3u8?s={s}&e={e}")
    return None


def jdids(url):
    ref = "/".join(url.split("/")[:3])
    soup = monhtml(url, ref)
    iframe = soup.iframe
    while iframe:
        u = iframe["src"]
        soup = monhtml(u, ref)
        iframe = soup.iframe
    sess.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Referer': ref
    }
    v = u.split("/")
    m3u = v[-1]
    ref = "/".join(v[:3])
    while True:
        try:
            r = sess.get(u)
            val = [e for e in r.text.split(
                '|') if re.search(r"^[0-9a-z]+$", e.lower())]
            _, e, s, ht, wst, *_ = [e for e in val if len(e) > 9 and not e.startswith(
                "set") and "start" not in e.lower() and "max" not in e.lower()]
            if not re.search(r"[^0-9]", e):
                return ref, f"https://{ht}.{wst}.net:8443/hls/{m3u}.m3u8?s={s}&e={e}"
        except:
            print("Reload !")


def liveit(k):
    link = chs[k]
    dd = None
    while not dd:
        dd = jdid(link)
    referrer, url = dd
    print(f"> {url}")
    print(f"> {referrer}")
    cmd = f"""vlc --loop "{url}" --http-referrer="{referrer}
        " --http-user-agent="{agent}" --adaptive-use-access"""
    os.system(cmd)


# args = sys.argv
# values = []
# if len(args) > 1:
#     nb = args[1]
# else:
#     p = None
#     values = list(chs)
#     while True:
#         if p:
#             print(p)
#         t = " Channels List "
#         print(f"{t:=^60}")
#         for i, c in enumerate(values, start=1):
#             print(f"{i:02}.", c)
#         nb = input("Choose You Preffered Channel : ")
#         if re.search(r"^[0-9]+$", nb):
#             nb = values[int(nb)-1]
#         if nb in chs:
#             break
# k="hd3"
# liveit(k)
