import requests
import os
import re
from bs4 import BeautifulSoup
import m3u8
import json

os.chdir("/home/mohamed/Documents/datas/LIves")
ref="https://player.mangomolo.com"
agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
sess = requests.session()
links=[
    "144",
    "145",
    "148"
]


def monhtml(k, ref=None):
    if ref:
        sess.headers['Referer'] = ref
    r = sess.get(k)
    encoding = r.encoding if 'charset' in r.headers.get(
        'content-type', '').lower() else None
    parser = 'html.parser'  # or lxml or html5lib
    return BeautifulSoup(r.content, parser, from_encoding=encoding)

def choose(u):
    print(f"{u}...",end="\r")
    ref="/".join(u.split("/")[:3])
    soup=monhtml(u, ref)
    iframe=[ifr for ifr in soup.findAll("iframe") if "player" in ifr["src"]]
    ref="/".join(u.split("/")[:3])
    u="https:"+iframe[0]["src"]
    print(u,end="\r")
    soup=monhtml(u,ref)
    iframe=soup.iframe
    sess.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Referer': ref
    }
    ref=u
    r = sess.get(u)
    us = re.findall(r'[^\'"]+m3u8[^\'"]*',r.text)
    return us[0]

def liens(url):
    sess.headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Referer': ref
    }
    r = sess.get(url, stream=True)
    obj = m3u8.loads(r.text)
    return obj.data["playlists"]

def save(u,fn):
    p=choose(u)
    print(p,"="*60)
    fr,s = p.rsplit('/', 1)
    info={
        "url":u,
        "seg":fr
    }
    els=liens(p)
    arr=[]
    for el in els:
        u=el["uri"]
        ks=el['stream_info']
        r1=ks['bandwidth']
        r2=int(ks['resolution'].split("x")[-1])
        r=f"{r1+r2:07}"
        arr.append([r,u])
    arrs=[e[-1] for e in sorted(arr,key=lambda e:e[0])]
    arrs.append(s.split('?')[0])
    info["segs"]=arrs

    with open(fn, "w",encoding="utf-8") as f:
        json.dump(info,f)

links=[
    "144",
    "145",
    "148"
]
for i,r in enumerate(links,start=1):
    fn=f"AD{i}.json"
    if not os.path.exists(fn):
        nb=links[i-1]
        u=f"https://adsports.ae/live/{nb}"
        save(u,fn)

for i in range(2):
    nb=i+1
    fn=f"Dubai{nb}.json"
    if not os.path.exists(fn):
        u=f"https://www.dubaisports.ae/content/dubaisports/livestreaming/channel-{nb}.html"
        save(u,fn)
