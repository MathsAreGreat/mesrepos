import json
import requests
import os
from playwright.sync_api import sync_playwright


ids = []
pt = "/home/mohamed/Documents/Stuff/Jups"


def main_single(ids):
    with sync_playwright() as p:
        # Launch Firefox browser
        # Set to False to see the browser
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()

        # Navigate to a webpage
        for ID in ids:
            fn = f'Files/{ID}.json'
            if os.path.isfile(fn):
                print(f"{ID} already exists. Skipping.", " "*20, end='\r')
                continue
            url = f"https://www.facebook.com/photo/?fbid={ID}"
            print(f"Checking {ID} .", " "*30, end='\r')
            page.goto(url)

            nb = 10
            while nb:
                uri = None
                for script in page.locator("script").all():
                    t = script.text_content()
                    if "additional_profile_has_taggable_products" in t:
                        uri = [
                            e.split('[')[0]
                            for e in t.split('"owner":')
                            if "additional_profile_has_taggable_products" in e
                        ]
                        nb = 0
                        break
                else:
                    nb -= 1
                    continue
            if not uri:
                uri = {}
            else:
                u = uri[0]
                while not u.endswith('}'):
                    u = u[:-1]
                uri = '{"owner":'+u+"}"
                uri = json.loads(uri)
            with open(fn, 'w') as f:
                json.dump(uri, f)
        # Close the browser
        browser.close()


uns = []

IDs = 1
while IDs:
    ids = []
    for f in os.listdir(pt):
        with open(f"{pt}/{f}", "r") as file:
            data = json.load(file)
            ids += [e[1:] for e in data["IDs"] if e[0] not in "0123456789"]

    for *_, files in os.walk('Images'):
        uns += [e.split("_")[1] for e in files if e.endswith('.jpg')]

    IDs = [e for e in set(ids) if e not in uns]

    print(len(IDs), "items !")
    main_single(IDs[:10])
    for f in os.listdir("Files"):
        ID, ex = f.rsplit('.', 1)
        if ex != "json":
            continue
        print("Featch", f)
        fnc = f'Files/{f}'
        with open(fnc, 'r') as fr:
            data = json.load(fr)
        try:
            created_time = data.get("created_time")
            if not created_time:
                doc = 'Images/Bucks'
                os.makedirs(doc, exist_ok=True)
                fn = f'{doc}/createdtime_{ID}_tk.jpg'
                with open(fn, 'wb') as fl:
                    fl.write(b"")
                os.remove(fnc)
                continue
            ar = data['owner']['user_id']
            u = data['image']['uri']
            tn = u.split('/')[-1].split('?')[0]
            doc = f'Images/{ar}'
            fn = f'{doc}/{created_time}_{ID}_{tn}'
            if not os.path.exists(fn):
                os.makedirs(doc, exist_ok=True)
                with open(fn, 'wb') as fl:
                    r = requests.get(u)
                    fl.write(r.content)
        except Exception as err:
            print("ERR :", f)
            print(err)
        os.remove(fnc)

    # IDs = IDs[10:]
