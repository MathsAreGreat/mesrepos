from datetime import datetime, timedelta
from pathlib import Path
from time import sleep
from bs4 import BeautifulSoup
import requests
import m3u8
import re
from concurrent.futures import ThreadPoolExecutor
import os
import json
from Crypto.Cipher import AES

sess = requests.session()
sess.headers = {
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
}


def concatize(*files, o="output", ex="ts"):
    filenames = "|".join(files[:])
    cmd = f'ffmpeg -i "concat:{filenames}" -c copy "{o}.{ex}"'
    os.system(cmd)
    msg = f"* {o}.{ex} Created !"
    print(upclear, f"{msg:<40}")


def combine_vids(pt):
    p = Path(pt)
    for v_out in p.glob("*"):
        if v_out.is_file():
            continue
        fn = v_out.with_suffix(f"{v_out.suffix}.mp4")
        print(fn)
        if not fn.exists():
            fs = [
                f"{f}"
                for f in v_out.glob("*.ts")
            ]
            fs = sorted(fs, key=lambda e: re.sub(
                r"[^0-9]", r"", e.rsplit(".", 1)[0]).zfill(20))
            ph = 0
            j = 1
            while len(fs) > 100:
                i = 0
                ph += 1
                while fs:
                    i += 1
                    concatize(*fs[:100], o=f"{v_out}_{j}_{i}")
                    fs = fs[100:]
                fs = [
                    f"{v_out}_{j}_{n+1}.ts"
                    for n in range(i)
                ]
                j += 1
            concatize(*fs, o=v_out, ex="mp4")
            if ph:
                for f in fs:
                    os.remove(f)
                    msg = f"** Removing {f}"
                    print(upclear, f"{msg:<40}")
        # if fn.exists():
        #     rmtree(f"{v_out}")
        #     doc = to / fn.parent.name
        #     name = fn.name
        #     if fn.parent.name != "Movies":
        #         ds, r = name.rsplit(".E", 1)
        #         *ds, s = [e.capitalize() for e in ds.split(".")]
        #         doc = " ".join(ds)
        #         doc = to / fn.parent.name / doc / s
        #         name = ".".join(ds)
        #         name = f"{name}.{s}.E{r}"
        #     doc.mkdir(parents=True, exist_ok=True)
        #     nf = doc / name
        #     fn.rename(nf)

    msg = "> All is Done !"
    print(upclear, f"{msg:<40}")
    return 1


def choose(nb):
    r = "https://viwlivehdplay.ru/"
    sess.headers["Referer"] = r
    if not re.search(r"[a-z]", nb):
        nb = int(nb)
        return r, basics(nb)
    if re.search(r"^-", nb):
        return r, prima(nb[1:])
    r = "https://antenasport.ru"
    sess.headers["Referer"] = r
    u = basic(nb)
    return r, u


def basic(k):
    u = f"https://aradsport.live/max.php?player=desktop&live={k}"
    match = re.search(r"return\((\[.+?\])", sess.get(u).text)
    if not match:
        return None
    url = "".join(json.loads(match[1]))
    sess.headers["Referer"] = u
    return url.replace("////", "//")


def basics(nb):
    u = f"https://salamus2023.onlinehdhls.ru/lb/premium{nb}/playlist.m3u8"
    urls = sess.get(u, allow_redirects=True).url.split('/')
    urls[-1] = "tracks-v1a1/mono.m3u8"
    return "/".join(urls)


def prima(nb):
    u = f"https://salamus2023.onlinehdhls.ru/lb/prima{nb}/index.m3u8"
    urls = sess.get(u, allow_redirects=True).url.split('/')
    urls[-1] = "tracks-v1a1/mono.m3u8"
    return "/".join(urls)


def dwn(v, ref, url, e, dd):
    cipher = None
    if dd:
        key, iv = dd
        cipher = AES.new(key, AES.MODE_CBC, iv)
    sess.headers = {
        "Referer": ref,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    if e:
        item = "-".join(e.split("/"))
        doc = f"/home/mohamed/Videos/Ts/{v}"
        lefile = f"{doc}/{item}"
        if not os.path.exists(lefile):
            os.makedirs(doc, exist_ok=True)
            us = f"{url}/{e}"
            rz = sess.get(us, timeout=10)
            cx = rz.status_code
            if cx == 200:
                c = rz.content
                if cipher:
                    c = cipher.decrypt(c)
                print(">", item)
                with open(lefile, "wb") as f:
                    f.write(c)


def dwns(ref, url, e, dd):
    cipher = None
    if dd:
        key, iv = dd
        cipher = AES.new(key, AES.MODE_CBC, iv)
    sess.headers = {
        "Referer": ref,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
    }
    if e:
        us = f"{url}/{e}"
        rz = sess.get(us, timeout=5)
        cx = rz.status_code
        if cx == 200:
            c = rz.content
            if cipher:
                c = cipher.decrypt(c)
            return c
        return None


def saves(a, ks):
    t, *_, l = infos(a[:8])
    ds = []
    for k in ks:
        v = f"{t} [{k}][{l.split('-')[0].strip()}]"
        try:
            referer, base_url = choose(k)
            base, _ = base_url.rsplit("/", 1)
            rs = sess.get(base_url, stream=True, timeout=10)
            mm = rs.text
            segments = m3u8.loads(mm).segments
            try:
                segment = segments[0]
                k = segment.key.uri
                resp = sess.get(k)
                vv = segment.key.iv
                iv = int(vv, 16).to_bytes(16, "big")
                key = resp.content
                dd = (key, iv)
            except Exception as e:
                print("Segment :", e)
                dd = None
            ds += [
                (v, referer, base, seg.uri, dd)
                for seg in segments
            ]
        except Exception as e:
            print("choose :", e)
    return ds


cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear


doc = "/home/mohamed/Videos/Ts"
os.makedirs(doc, exist_ok=True)

lesdatas = []


def monhtml(r):
    rs = sess.get(r)
    txt = rs.text
    return BeautifulSoup(txt, "html.parser")


def infos(k):
    u = f"http://www.livescore.cz/match/{k}"
    soup = monhtml(u)
    teams = soup.h3.text
    cs = soup.findAll("div", class_="detail")
    lives = [e for e in cs if e.findChildren("span", class_="live")]
    nos = [e.text for e in cs if not e.findChildren()]
    live = nos[0]
    if lives:
        live = lives[-1].text
    star = nos[-1]
    start_object = datetime.strptime(star, "%d.%m.%Y %H:%M")
    end_object = start_object + timedelta(hours=3)
    s_date = start_object.strftime("%Y-%m-%d_%H:%M") + ":00"
    e_date = end_object.strftime("%Y-%m-%d_%H:%M") + ":00"
    return teams, s_date, e_date, live


def save(t, kv):
    try:
        referer, base_url = choose(kv)
        base, _ = base_url.rsplit("/", 1)
        rs = sess.get(base_url, stream=True, timeout=3)
        mm = rs.text
        segments = m3u8.loads(mm).segments
        try:
            segment = segments[0]
            k = segment.key.uri
            resp = sess.get(k)
            vv = segment.key.iv
            iv = int(vv, 16).to_bytes(16, "big")
            key = resp.content
            dd = (key, iv)
        except Exception as e:
            print("Segment :", e)
            dd = None
        return [
            (f"{t} [{kv}]", referer, base, seg.uri, dd)
            for seg in segments
        ]
    except Exception as e:
        print("choose :", e)
        return []


def sauver(v):
    lefile = f"{doc}/Live-{v}.ts"
    garbage = []
    with open(lefile, "wb") as f:
        while True:
            datas = save(v)
            d = datetime.now().strftime("%H:%M:%S")
            print()
            print(f"{upclear*12}::", d, len(datas), "items !")
            print()
            for ref, base, uri, dd in datas:
                if uri in garbage:
                    continue
                cs = None
                nb = 5
                while not cs and nb:
                    try:
                        cs = dwns(ref, base, uri, dd)
                    except:
                        nb -= 1
                if not cs:
                    break

                print(f"{upclear}>", uri, ":", len(cs), " "*10)
                garbage.append(uri)
                f.write(cs)
            sleep(.3)


ks = ["-fox1", "116"]
# for k in ks:
#     sauver(k)

with ThreadPoolExecutor() as executor:
    executor.map(
        sauver,
        ks
    )

# ks = {"tKytNkCg": ['do11', '91', 'do22', '93']}
# temps = datetime.now().strftime("%H:%M:%S")
# while temps < "21:50":
#     os.system("clear")
#     print("Reolads at", temps)
#     try:
#         with ThreadPoolExecutor(10) as executor:
#             datas = executor.map(lambda args: save(*args), ks.items())
#         lesdatas = [e for data in datas for e in data]
#         print(len(lesdatas))
#         with ThreadPoolExecutor(10) as executor:
#             executor.map(lambda args: dwn(*args), lesdatas)
#         temps = datetime.now().strftime("%H:%M:%S")
#     except:
#         pass

# ks = ['-bein1max']
# temps = datetime.now().strftime("%H:%M:%S")
# while temps < "19:00":
#     os.system("clear")
#     print("Reolads at", temps)
#     t = "Material"
#     try:
#         with ThreadPoolExecutor(10) as executor:
#             datas = executor.map(lambda k: save(t, k), ks)
#         lesdatas = [e for data in datas for e in data]
#         print(len(lesdatas))
#         with ThreadPoolExecutor(3) as executor:
#             executor.map(lambda args: dwn(*args), lesdatas)
#         temps = datetime.now().strftime("%H:%M:%S")
#         print()
#         print(f"{upclear*{len(lesdatas)}}")
#         print()
#     except:
#         pass

# pt = "/home/mohamed/Videos/Ts"
# combine_vids(pt)
