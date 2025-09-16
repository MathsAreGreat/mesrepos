import re
from time import sleep
from playwright.sync_api import sync_playwright
playwright = sync_playwright().start()
browser = playwright.firefox.launch(timeout=300000,                args=["--disable-blink-features=AutomationControlled"]
                                    )
page = browser.new_page()

mobarats = []

nbr = 1

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
            for u in urs:
                print("---", u, "---")
            for k in ks:
                print("---", k, "---")
            print()
            break
        break

browser.close()
playwright.stop()
