import os
import re
from time import sleep
from playwright.sync_api import sync_playwright

from urllib.parse import unquote

import requests

playwright = sync_playwright().start()
browser = playwright.firefox.launch(
    timeout=300000,
    args=["--disable-blink-features=AutomationControlled"]
)
page = browser.new_page()

mobarats = []

nbr = 1

agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"

mts = []


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


while nbr > 0:
    nbr = 0
    # 👉 Navigate to your target page
    # Replace with your actual URL
    page.goto("https://www.shoot4live.com/", wait_until="domcontentloaded")
    for link in page.query_selector_all(".AY_Match a"):
        if not link.get_attribute("title"):
            continue
        if "http" not in link.get_attribute("href"):
            continue
        tt = link.get_attribute("title")
        if tt in mobarats:
            continue
        print(tt)
        mobarats.append(tt)
        nbr += 1
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
            i = 0
            content = scripts[0]
            ct = content.strip()
            urs = re.findall(r"url = [\"']([^\s]+)[\"']", ct)
            ks = re.findall(r"key: [\"']([^\s]+)[\"']", ct)
            mts.append((*urs, *ks))
            for u in urs:
                print("---", u, "---")
            for k in ks:
                print("---", k, "---")
            print()
            break
        break

browser.close()
playwright.stop()


nb = int(input("Select Your match number please ! ")) - 1


uri, tk, key = mts[nb]

referrer, url = b_url(tk, uri, key)

cmd = f"""vlc --loop "{url}" --http-referrer="{referrer}" --http-user-agent="{agent}" --adaptive-use-access"""
os.system(cmd)
