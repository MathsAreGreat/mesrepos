import os
import re
from time import sleep
from playwright.sync_api import sync_playwright

from urllib.parse import unquote, urljoin

import requests

from Crypto.Cipher import AES
import m3u8

playwright = sync_playwright().start()
browser = playwright.firefox.launch(
    timeout=300000,
    args=["--disable-blink-features=AutomationControlled"]
)
page = browser.new_page()

mobarats = []

nbr = 1

agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"
agent = "Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0"

mts = []

sess = requests.session()
referrer = ""

OUTPUT_DIR = "/home/mohamed/Videos/Ts"

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def download(uri, referrer):
    sess.headers = {
        "user-agent": agent,
        "Referer": referrer
    }
    print("!!", referrer)
    response = sess.get(uri, stream=True)
    if response.status_code == 200:
        return response.content
    else:
        return None


def online_stream(url, referrer):
    cmd = f"""vlc --loop "{url}" --http-referrer="{referrer}" --http-user-agent="{agent}" """
    os.system(cmd)


def live_stream(url, referrer, titre="Live"):
    kayn = []
    key = None
    output_file = f"{OUTPUT_DIR}/{titre}.ts"
    print(url)
    sess.headers = {
        "user-agent": agent,
        "Referer": referrer
    }
    with open(output_file, "wb") as m3f:

        while True:
            rs = sess.get(url, stream=True)
            r = m3u8.loads(rs.text)

            stream_info = r.data["segments"]
            for element in stream_info:
                stream_key = element.get("key")
                uri = urljoin(url, element["uri"])
                k = element["uri"].rsplit(".", 1)[0]
                ks = re.findall(r"[0-9]+", k)
                k = "-".join(f"{int(e):04}" for e in ks)
                if k in kayn:
                    continue
                uri = urljoin(url, uri)
                data = download(uri, referrer)
                if not data:
                    break
                if stream_key:
                    key_uri = stream_key["uri"]
                    iv = stream_key["iv"]
                    uri = urljoin(url, key_uri)
                    key = download(uri, referrer)
                    if not key:
                        break
                data = decrypt_aes128(key, iv, data)
                m3f.write(data)
                kayn.append(k)
                print(uri.split("/")[-1].split("?")[0])


def decrypt_aes128(key, iv, encrypted_data):
    # Remove '0x' prefix and convert to bytes
    iv_bytes = bytes.fromhex(iv[2:])
    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data


def b_url(token_url, lastSegment="bein1", key="key001"):
    sess = requests.session()
    ref = token_url.rsplit("/", 1)[0]
    sess.headers = {
        "user-agent": agent,
        "Referer": ref
    }
    data = {
        "ch": lastSegment,
        "key": key
    }
    r = sess.post(token_url, data=data)
    streamUrl = r.json()
    streamUrl = unquote(re.sub(r"(.{1,2})", r"%\1", streamUrl["url"]))
    return ref, streamUrl


nbr = 1
page.goto("https://www.shoot4live.com/", wait_until="domcontentloaded")
for link in page.query_selector_all(".AY_Match a"):
    if not link.get_attribute("title"):
        continue
    if "http" not in link.get_attribute("href"):
        continue
    tt = link.get_attribute("title")
    if tt in mobarats:
        continue
    print(nbr, "|", tt)
    mobarats.append(link)
    nbr += 1
nb = int(input("Select Your match number please ! ")) - 1
link = mobarats[nb]
tt = " ".join(e for e in link.get_attribute("title").split(" ")[2:] if e)
tt = tt.split("تاريخ")[0].strip()
tt = tt.rsplit(" ", 1)[0].replace(' ', '.')
parent = link.evaluate_handle("el => el.parentElement")
parent.click()
iframe_element = page.wait_for_selector("iframe")
iframe = iframe_element.content_frame()
while True:
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    scripts = iframe.evaluate("""
        () => Array.from(document.scripts).map(s => s.textContent.trim() || "").filter(s => s.includes("token.php"))
    """)

    if not scripts:
        sleep(0.6)
        continue
    content = scripts[0]
    ct = content.strip()
    urs = re.findall(r"url = [\"']([^\s]+)[\"']", ct)
    ks = re.findall(r"key: [\"']([^\s]+)[\"']", ct)
    uri, tk, key = [*urs, *ks]
    break

browser.close()
playwright.stop()

referrer, url = b_url(tk, uri, key)
live_stream(url, referrer, tt)
