import html
import json
import os
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup

sess = requests.session()


class DAILY:
    def __init__(self, k):
        self.ID = k
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
            "Referer": "https://www.dailymotion.com/",
        }

    def check_for_datas(self):
        doc = Path("/home/mohamed/Documents/datas/Daily/Vides")
        Path(doc).mkdir(parents=True, exist_ok=True)
        fn = doc / self.ID
        if Path(fn).exists():
            return None
        ok_url = f"https://www.dailymotion.com/video/{self.ID}"
        sess.headers = self.headers
        r = sess.get(ok_url)
        if "<h1" not in r.text:
            Path(fn).touch()
            return None
        return ok_url

    def geturl(self):
        ok_url = self.check_for_datas()
        # if not ok_url:
        #     print("Not found")
        #     return []
        fjson = f"/home/mohamed/Documents/datas/Daily/t{self.ID}.json"
        cmd = f'yt-dlp "{ok_url}" --flat-playlist --skip-download --dump-json > {fjson}'
        os.system(cmd)
        print(">>", fjson, end="\r")
        try:
            with Path(fjson).open("r") as e:
                data = json.load(e)
        except OSError:
            data = {}
        Path(fjson).unlink(missing_ok=True)
        if not data:
            return []
        for e in data["formats"]:
            if e.get("protocol") and e["protocol"] == "m3u8_native":
                return e["manifest_url"]
        return []


class OKRU:
    def __init__(self, k):
        self.ID = k
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
            "Referer": "https://ok.ru/",
        }

    def check_for_datas(self):
        doc = Path("/home/mohamed/Documents/datas/OKRU/Vides")
        Path(doc).mkdir(parents=True, exist_ok=True)
        fn = f"{doc}/{self.ID}"
        if Path(fn).exists():
            return None
        ok_url = f"https://ok.ru/videoembed/{self.ID}"
        sess.headers = self.headers
        r = sess.get(ok_url)
        txt = html.unescape(r.text)
        soup = BeautifulSoup(txt, "html.parser")
        msg = soup.find(class_="vp_video_stub_txt")
        if msg:
            Path(fn).touch()
            return None
        return ok_url

    def geturl(self):
        ok_url = self.check_for_datas()
        if not ok_url:
            print("Not found")
            return []
        fjson = f"/home/mohamed/Documents/datas/OKRU/t{self.ID}.json"
        cmd = f'yt-dlp "{ok_url}" --flat-playlist --skip-download --dump-json > {fjson}'
        os.system(cmd)
        print(">>", fjson, end="\r")
        try:
            with Path(fjson).open("r") as e:
                data = json.load(e)
        except OSError:
            data = {}
        if not data:
            return []
        for e in data["formats"]:
            if e.get("protocol") and e["protocol"] == "m3u8_native":
                return e["manifest_url"]
        return []


class MP4:
    def __init__(self, k):
        self.ID = k
        self.url = f"https://www.mp4upload.com/{self.ID}"
        self.fileName = None
        self.size = None

    def update(self):
        html = sess.get(self.url, verify=False).text
        sz = re.findall(r"[0-9\.]+ [GM]B", html)
        if sz:
            self.soup = BeautifulSoup(html, "html.parser")
            self.fileName = self.soup.find("h4").text.replace("Download File ", "")
            nb, unit = sz[0].split(" ")
            nb = float(nb)
            if "g" in unit.lower():
                nb = nb * 1000
            self.size = nb
        else:
            self.size = 0
            self.fileName = "File not found"
        return self

    def save(self):
        data = self.update()
        return data

    @property
    def press(self):
        params = {}
        inputs = self.soup.find_all("input")
        for item in inputs:
            params.update({item["name"]: item["value"]})
        response = sess.post(self.url, data=params, verify=False).text
        return response

    @property
    def lien(self):
        if not self.size:
            return None
        soup = BeautifulSoup(self.press, "html.parser")
        params = {}
        inputs = soup.find_all("input")
        for item in inputs:
            params.update({item["name"]: item["value"]})
        response = sess.post(
            self.url, data=params, verify=False, allow_redirects=False
        ).headers["Location"]
        return response


class SMOOTH:
    def __init__(self, k):
        self.ID = k
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
            "Referer": "https://smoothpre.com/",
        }

    def check_for_datas(self):
        doc = Path("/home/mohamed/Documents/datas/Smooth/Vides")
        Path(doc).mkdir(parents=True, exist_ok=True)
        fn = doc / self.ID
        if Path(fn).exists():
            return None
        ok_url = f"https://smoothpre.com/embed/{self.ID}"
        sess.headers = self.headers
        r = sess.get(ok_url)
        if "m3u8" not in r.text:
            Path(fn).touch()
            return None
        return ok_url
