import os
import re
import sys

import requests
from bs4 import BeautifulSoup
from numpy import base_repr

agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
sess = requests.session()
sess.headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
}

DOM = "sportzonline.si"

chs = [f"https://{DOM}/channels/pt/btv.php"]
chs += [f"https://{DOM}/channels/pt/sporttv{i + 1}.php" for i in range(5)]
chs += [f"https://{DOM}/channels/pt/eleven{i + 1}.php" for i in range(3)]
chs += [f"https://{DOM}/channels/hd/hd{i + 1}.php" for i in range(11)]
chs += [f"https://{DOM}/channels/bra/br{i + 1}.php" for i in range(4)]

chs = {u.split("/")[-1].split(".")[0]: u for u in chs}


def monhtml(k, ref=None):
    if ref:
        sess.headers["Referer"] = ref
    r = sess.get(k)
    encoding = (
        r.encoding if "charset" in r.headers.get("content-type", "").lower() else None
    )
    parser = "html.parser"
    return BeautifulSoup(r.content, parser, from_encoding=encoding)


def decode_string(p, a, c, k, e, d):
    def e_func(c):
        return (e_func(c // a) if c >= a else "") + (
            chr(c + 29) if (c := c % a) > 35 else base_repr(c, 36).lower()
        )

    while c > 0:
        c -= 1
        d[e_func(c)] = k[c] or e_func(c)

    p = re.sub(r"\b\w+\b", lambda m: d.get(m.group(0), ""), p)

    return p


def uparse(tt):
    tt = tt.split("clappr.min.js")[-1]
    tt = tt.replace("\\'", "<&>")
    datas = tt.split("'")
    ind = datas.index(".split(")
    exp, tnb, wst = datas[ind - 3 : ind]
    tnb = [int(e) for e in tnb.split(",") if e.strip()]
    r = decode_string(
        exp.replace("<&>", "'"), *tnb, wst.replace("<&>", "'").split("|"), 0, {}
    )
    return r


def urlize(tt):
    r = uparse(tt)
    return r.split('src="')[1].split('"')[0]


def jdid(u):
    ref = "/".join(u.split("/")[:3])
    soup = monhtml(u, ref)
    iframe = soup.iframe
    while iframe:
        ht = u.split("/")[2]
        ref = f"https://{ht}/"
        u = iframe["src"].replace(" ", ".")
        if not u.startswith("http"):
            u = "https:" + u
        soup = monhtml(u)
        iframe = soup.iframe
    sess.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
        "Referer": ref,
    }

    ht = u.split("/")[2]
    ref = f"https://{ht}/"
    r = sess.get(u)
    try:
        return ref, urlize(r.text)
    except Exception as err:
        print("**", err)
        return None


def liveit(k):
    link = chs[k]
    dd = None
    while not dd:
        dd = jdid(link)
    referrer, url = dd
    print(f"> {url}")
    print(f"> {referrer}")
    cmd = f"""vlc "{url}" --http-referrer="{referrer}
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
#             nb = values[int(nb) - 1]
#         if nb in chs:
#             break
# liveit(nb)
if __name__ == "__main__":
    from Mido.variables import download_m3u8_with_aria2c

    u = "https://0vg9r.com/bkg/71to1s3yt7z6"
    u = "https://0vg9r.com/bkg/2vly7etat4x9"
    u = "https://smoothpre.com/embed/8a5g73vjnalb"
    r = sess.get(u)
    tt = r.text
    p = uparse(tt)
    # urls = [e for e in re.findall(r"https?://[^\s'\"]+", p) if ".m3u8" in e]
    # link = urls[-1]
    # download_m3u8_with_aria2c(
    #     link,
    #     "/home/mohamed/Videos/Vid.%(ext)s",
    # )
    print(p)
