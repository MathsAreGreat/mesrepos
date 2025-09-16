import os
import requests
import json
import m3u8

agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
sess = requests.Session()
# os.chdir("/home/mohamed/Documents/datas/LIves")

ref = ""

links = {
    "shtv34": "https://svs.itworkscdn.net/alwoustalive/alwoustatv.smil/playlist.m3u8",
    "shsprt": "https://svs.itworkscdn.net/smc4sportslive/smc4.smil/playlist.m3u8",
    "shtv37": "https://svs.itworkscdn.net/kablatvlive/kabtv1.smil/playlist.m3u8",
    "shtv38": "https://svs.itworkscdn.net/smc1live/smc1tv.smil/playlist.m3u8",
    "shtv36": "https://svs.itworkscdn.net/smc2live/smc2tv.smil/playlist.m3u8",
    # "shra13": "https://svs.itworkscdn.net/smcradiolive/smcradiolive/playlist.m3u8",
    # "shra12": "https://svs.itworkscdn.net/smcquranlive/quranradiolive/playlist.m3u8",
    # "shra20": "https://svs.itworkscdn.net/smcwatarlive/smcwatar/playlist.m3u8",
    # "shra21": "https://svs.itworkscdn.net/pulse95live/pulse96/playlist.m3u8"
}


def snrt(k):
    return f"https://cdnamd-hls-globecast.akamaized.net/live/ramdisk/{k}/hls_snrt/index.m3u8"


keys = [
    "arridia",
    "arrabiaa",
    "assadissa",
    "al_maghribia_snrt",
    "al_aoula_laayoune",
    "al_aoula_inter"
]
for k in keys:
    links[f"sn_{k}"] = snrt(k)

refs = {
    "ar": "https://arryadia.snrt.ma/",
    "sh": "https://sba.net.ae/"
}


def liens(url, ref):
    sess.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Referer': ref
    }
    r = sess.get(url, stream=True)
    obj = m3u8.loads(r.text)
    return obj.data["playlists"]


def save(key):
    p = links[key]
    fn = f"{key}.json"
    ref = refs.get(key[:2])
    fr, s = p.rsplit('/', 1)
    info = {
        "url": ref,
        "seg": fr
    }
    els = liens(p, ref)
    arr = []
    for el in els:
        u = el["uri"]
        ks = el['stream_info']
        r1 = ks['bandwidth']
        r2 = int(ks['resolution'].split("x")[-1])
        r = f"{r1+r2:07}"
        arr.append([r, u])
    arrs = [e[-1] for e in sorted(arr, key=lambda e: e[0])]
    arrs.append(s)
    info["segs"] = arrs
    with open(fn, "w", encoding="utf-8") as f:
        json.dump(info, f)

# for k in links:
#     save(k)


url = "https://vd296.okcdn.ru/expires/1729397085563/srcIp/160.178.100.227/pr/10/srcAg/SAFARI_IPHONE_OTHER/ms/185.226.53.5/type/5/sig/vzvcXwTlsms/ct/8/urls/45.136.21.26/clientType/0/id/6843628390960/video/"
referrer = "https://ok.ru"

settings = f'--http-referrer="{referrer}" --http-user-agent="{agent}"'
cmd = f"""vlc "{url}" {settings}"""
os.system(cmd)
