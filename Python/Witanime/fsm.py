import base64
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import requests
import subprocess

from Mido.variables import monhtml, print, sprint, get_m3u8

# Static framework hash parts
_m1 = "7350"
_m2 = "3d58-f228-"
_m3 = "425f-97f1-"
_m4 = "2d9512f5772c"
FRAMEWORK_HASH = ""

restricted_domains = ["www.yourupload.com", "www.mp4upload.com", "videa.hu"]

sess = requests.Session()


# This is your Base64 string
def initialize_resources(encoded_str: str):
    decoded_bytes = base64.b64decode(encoded_str)
    resources = decoded_bytes.decode("utf-8")
    return resources


def get_parameter_offset(config_settings):
    index_key = base64.b64decode(config_settings["k"]).decode()
    return config_settings["d"][int(index_key)]


def render_module_content(module_key, resource_registry, config_registry):
    global FRAMEWORK_HASH, _m1, _m2, _m3, _m4

    resource_data = resource_registry[module_key]
    config_settings = config_registry[module_key]

    if not (resource_data and config_settings):
        return None  # nothing to render

    if not FRAMEWORK_HASH:
        FRAMEWORK_HASH = _m1 + _m2 + _m3 + _m4
        _m1 = _m2 = _m3 = _m4 = None

    # Reverse string and clean
    resource_data = resource_data[::-1]
    resource_data = "".join(c for c in resource_data if c.isalnum() or c in "+/=")

    # Decode base64
    param_offset = get_parameter_offset(config_settings)
    decoded_resource = base64.b64decode(resource_data).decode()[:-param_offset]

    # Add API key if matches pattern
    if decoded_resource.startswith("https://yonaplay.org/embed.php?id="):
        resolved_resource = f"{decoded_resource}&apiKey={FRAMEWORK_HASH}"
    else:
        resolved_resource = decoded_resource

    return resolved_resource


def ep(u, nb=0):
    print("::", u.split("/episode/")[-1])
    session = requests.Session()
    session.headers.update(
        {
            "Referer": "https://witanime.red/",
        }
    )
    r = session.get(u)
    htext = r.text
    if nb:
        rel = [
            initialize_resources(u)
            for u in re.findall(r"'(aH[^'\"]+)", htext, flags=re.IGNORECASE)
        ]
        return rel
    nb = int(re.findall(r"p=([0-9]+)", htext)[0])
    tt = re.findall(r"<h3>([^<]+)", htext)[0]

    sv = [
        re.findall(r"[a-z0-9\s\-\.]+", e, flags=re.IGNORECASE)
        for e in re.findall(r"server-id([^/]+)<", htext, flags=re.IGNORECASE)
    ]
    sv = {k: v for k, *_, v in sv}
    ds = {
        k: v
        for k, v in re.findall(r"(_z[gh])[\"=\s]+([^\"]+)", htext, flags=re.IGNORECASE)
    }

    return nb, tt, sv, ds


def saves(sv, resourcey, configy):
    iframes = {}
    for k, v in sv.items():
        i = int(k)
        result = render_module_content(i, json.loads(resourcey), json.loads(configy))
        iframes[v] = result

        if (
            "ok.ru" not in result
            and "dailymotion" not in result
            and "videa.hu" not in result
            and "mp4upload" not in result
            and "streamwish" not in v
        ):
            continue

        if "streamwish" in v:
            kc = result.split("/")[-1]
            result = f"https://auvexiug.com/e/{kc}"
            p = get_m3u8(result)
            link, *_ = [e for e in re.findall(r"http[^\"']+", p) if ".m3u8" in e]
            iframes[v] = result

            cmd = ["ok_bash", link, kc]
        else:
            cmd = ["ok_bash", result]

        try:
            subprocess.run(cmd, check=True)
            print(">", result)
        except:
            print("> ERROR :", result)

    return iframes


def dsave(u):
    ID, tt, sv, ds = ep(u)
    configy = initialize_resources(ds["_zH"])
    resourcey = initialize_resources(ds["_zG"])

    info = {"titre": tt, "iframes": saves(sv, resourcey, configy)}

    fn = Path(f"/home/mohamed/Documents/datas/Witanimes/{ID}.json")
    with fn.open("w", encoding="utf-8") as fl:
        json.dump(info, fl)


if __name__ == "__main__":

    us = [
        "https://witanime.red/episode/grand-blue-season-2-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-11/",
    ]

    # with ThreadPoolExecutor(5) as executor:
    #     datas = executor.map(
    #         lambda u: monhtml(u).select(".episodes-card-title"),
    #         [f"https://witanime.red/episode/page/{nb+1}/" for nb in range(1)],
    #     )

    # us += [
    #     e.select_one("a").get("href")
    #     for arr in datas
    #     for e in arr
    #     if e.select_one("a").get("href")
    # ]

    us = [e for e in set(us) if "-conan-" not in e and "one-piece" not in e]

    urls = []

    for u in us:
        if u in urls:
            continue
        urls += ep(u, 1)
    sprint("Time to Save :")
    rel = list(dict.fromkeys(urls))
    with ThreadPoolExecutor(5) as executor:
        executor.map(dsave, rel)

    p_kru = Path("/home/mohamed/Documents/datas/Witanimes")

    for fn in p_kru.glob("*.json"):
        with fn.open("r") as fl:
            datas = json.load(fl)
        if "iframes" not in datas:
            continue

        iframes = [e for e in set(datas["iframes"].values())]

        if not iframes:
            continue

        for url in iframes:
            c = (
                url.split("/")[-1]
                .split("=")[-1]
                .split(
                    "embed-",
                )[-1]
                .split(".")[0]
            )
            vn = Path(f"/home/mohamed/Documents/Files/{c}.json")
            if not vn.exists():
                continue
            if vn.stat().st_size < 50:
                continue
            with vn.open("r") as fl:
                dt = json.load(fl)
            vn.unlink()
            vn = Path(f"/home/mohamed/Documents/Files/{c}.json")
            if not dt["tbr"]:
                print(">>", c)
                u = dt["url"]
                sess = requests.Session()
                if "mp4upload" in u:
                    sess.verify = False
                r = sess.get(u, stream=True)
                if not r.headers.get("Content-Length"):
                    nb = 0
                else:
                    nb = int(r.headers.get("Content-Length")) * 6 / (1024 * 1024)
                    nb = nb * 100 / 100
                dt["tbr"] = nb
            with vn.open("w") as fl:
                json.dump(dt, fl)
