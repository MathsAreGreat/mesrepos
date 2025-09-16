import requests
import os
import json
import re
import m3u8

os.chdir("/home/mohamed/Documents/datas/LIves")

agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
sess = requests.session()
ref="https://www.alkass.net/"
sess.headers = {
    "user-agent": agent,
    "Referer": ref
}

def choose(u):
    r=sess.get(u)
    us=re.findall(r'[^"]*\.m3u8[^"]*', r.text)[0].strip()
    return us

def liens(url):
    r = sess.get(url, stream=True,timeout=100)
    obj = m3u8.loads(r.text)
    print("**",ref,end="\n")
    return obj.data["playlists"]

def save(u,fn=""):
    p=choose(u)
    fr,s = p.rsplit('/', 1)
    info={
        "url":u,
        "seg":fr
    }
    els=liens(p)
    arr=[]
    arrs=[]
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

arr=["one","two","three","four","five"]
for i,r in enumerate(arr,start=1):
    fn=f"KS{i}.json"
    nb=arr[i-1]
    u=f"https://www.alkass.net/alkass/live.aspx?ch={nb}"
    save(u,fn)