from bs4 import BeautifulSoup
import re
import os
import requests
import pickle
from tqdm.auto import tqdm
from random import choice
from concurrent.futures import ThreadPoolExecutor

requests.packages.urllib3.disable_warnings()

sess = requests.session()
sess.headers = {
    'Referer': 'https://www.mp4upload.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
}

cols = [
    "#00ff00", 'red',
    'green', 'yellow',
    'blue', 'magenta',
    'cyan', 'white'
]


def run_tasks(fn, ds, nb=20):
    def your_function(args): return fn(*args)
    with ThreadPoolExecutor(nb) as executor:
        datas = executor.map(your_function, ds)
    return datas


def goo(eps):
    episodes = [
        (k, t, n)
        for t, n, k in eps
    ]
    run_tasks(vid_dwn, episodes, 5)


def vid_dwn(k, t, n):
    t = t.title()
    doc = f"Library/MixAnimes/Seasons/{t}"
    tn = f"{t} E{n}"
    tn = tn.replace(" ", ".")
    fn = f"{doc}/{tn}.mp4"
    if os.path.exists(fn):
        return None
    os.makedirs(doc, exist_ok=True)
    p_file = f"{doc}/{tn}.mp4.part"
    sess = requests.session()
    sess.headers = {
        'Referer': 'https://www.mp4upload.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
    }
    sess.verify = False
    os.makedirs(doc, exist_ok=True)
    u = MP4(k).save()
    url = u.lien
    response = sess.get(url, stream=True, allow_redirects=False, timeout=100)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(
        total=total_size_in_bytes,
        unit="iB",
        unit_scale=True,
        leave=False,
        desc=f"{tn} ",
        colour=choice(cols),
    )
    with open(p_file, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")
        return 0
    os.rename(p_file, fn)
    return 1


class MP4(object):
    def __init__(self, k):
        self.ID = k
        self.url = f"https://www.mp4upload.com/{self.ID}"
        self.fileName = None
        self.size = None

    def Update(self):
        html = sess.get(self.url, verify=False).text
        sz = re.findall(r"[0-9\.]+ [GM]B", html)
        if sz:
            self.soup = BeautifulSoup(html, 'html.parser')
            self.fileName = self.soup.find(
                'h4').text.replace('Download File ', '')
            nb, unit = sz[0].split(" ")
            nb = float(nb)
            if "g" in unit.lower():
                nb = nb*1000
            self.size = nb
        else:
            self.size = 0
            self.fileName = "File not found"
        return self

    def save(self):
        ID = self.ID
        doc = "datas/Mp4upload"
        os.makedirs(doc, exist_ok=True)
        fname = f"{doc}/{ID}.m4up"
        if os.path.exists(fname):
            with open(fname, "rb") as e:
                data = pickle.load(e)
        else:
            data = self.Update()
            with open(fname, "wb") as e:
                pickle.dump(data, e)
        return data

    @property
    def press(self):
        params = dict()
        inputs = self.soup.find_all('input')
        for item in inputs:
            params.update({item['name']: item['value']})
        response = sess.post(self.url, data=params, verify=False).text
        return response

    @property
    def lien(self):
        if not self.size:
            return None
        soup = BeautifulSoup(self.press, 'html.parser')
        params = dict()
        inputs = soup.find_all('input')
        for item in inputs:
            params.update({item['name']: item['value']})
        response = sess.post(
            self.url, data=params, verify=False, allow_redirects=False).headers['Location']
        return response


if __name__ == '__main__':
    k = "mcm6dwv0sn4y"
    p = MP4(k).save()
    print(p.lien)
