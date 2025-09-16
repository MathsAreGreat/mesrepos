import json
import os
import asyncio
import requests
from playwright.async_api import async_playwright
from functools import wraps
from time import sleep


PARENT = "/home/mohamed/Documents/.Socials"

cursor_up = "\033[1A"
clear = "\x1b[2K"
upclear = cursor_up + clear

# with open("info.json", "r") as file:
#     infos = json.load(file)


def retry_on_exception(wait_seconds=1):
    """
    A decorator to retry a function if an exception is raised.

    Args:
        wait_seconds (int): Number of seconds to wait before retrying.
    Returns:
        function: A wrapped function with retry logic.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while True:
                try:
                    # Attempt to execute the function
                    result = func(*args, **kwargs)
                    return result
                except Exception:
                    attempts += 1
                    print(f"> Attempt {attempts} failed !")
                    sleep(wait_seconds)

        return wrapper

    return decorator

# Load all IDs from files


def load_ids():
    ids = []
    pt = "/home/mohamed/Documents/Stuff/Jups"
    for f in os.listdir(pt):
        with open(f"{pt}/{f}", "r") as file:
            data = json.load(file)
            ids += [e[1:] for e in data["IDs"] if e[0] not in "0123456789"]
    return ids

# Function to process a single ID


async def fetch_data(page, ID):
    fn = f'Files/{ID}.json'
    if os.path.isfile(fn):
        print(f"> {ID} already exists. Skipping.", " "*20, end='\r')
        return 1

    url = f"https://www.facebook.com/photo/?fbid={ID}"
    print(f"> Checking {ID:<50} .", end='\r')

    try:
        # Faster load
        await page.goto(url, wait_until="domcontentloaded")

        procced = True
        nb = 100
        uri = None
        while procced and nb > 0:
            # Extract scripts efficiently
            if url != page.url:
                break
            body_text = await page.text_content("body")
            if body_text and "isn't available" in body_text.lower():
                break
            scripts = await page.evaluate("Array.from(document.scripts).map(s => s.textContent)")

            # Find the target script
            for script in scripts:
                if "accessibility_caption" in script:
                    uri = [e.split('[')[0] for e in script.split(
                        '"owner":') if "accessibility_caption" in e]
                    procced = False
                    break
            else:
                nb -= 1

        if uri:
            u = uri[0]
            while not u.endswith('}'):
                u = u[:-1]
            data = json.loads('{"owner":' + u + "}")
        else:
            data = {}

        # Save JSON data
        with open(fn, 'w') as f:
            json.dump(data, f)

    except Exception as e:
        print(f"Error processing {ID}: {e}")
        return 0


@retry_on_exception(1)
def download_image(u, fn):
    r = requests.get(u)
    with open(fn, 'wb') as f:
        f.write(r.content)
# Main function (processes in chunks of 10)


async def main(nb=10):
    ids = get_pending_ids()
    print(f"{upclear}:: {len(ids)} items.", ' '*50, end='\n\n\n')
    # ids = ids[:1000]
    nbr = 0
    while ids:
        print(f"{upclear}> Processing {len(ids)} items.", ' '*50)
        sleep(1)
        batch = ids[:nb]  # Process 10 at a time
        ids = ids[nb:]

        async with async_playwright() as p:
            browser = await p.firefox.launch(
                headless=True,
                args=["--disable-blink-features=AutomationControlled"]
            )
            # 5 concurrent tabs
            pages = [await browser.new_page() for _ in range(nb)]

            tasks = [fetch_data(pages[i % len(pages)], ID)
                     for i, ID in enumerate(batch)]
            await asyncio.gather(*tasks)  # Run the batch

            await browser.close()
        files = 16
        while files:
            files = [f for f in os.listdir("Files") if f.endswith(".json")]
            sleep(0.3)
        nbr += nb
        if nbr > 1000:
            sleep(300)
            # ids = get_pending_ids()
            nbr = 0

# Load IDs and filter already downloaded ones


def get_pending_ids():
    uns = [f.split(".")[0] for f in os.listdir("Files") if f.endswith(".json")]
    for *_, files in os.walk(PARENT):
        uns += [
            e.split("_")[1].split(".")[0]
            for e in files
            if "_" in e
        ]

    all_ids = load_ids()
    return [e for e in set(all_ids) if e not in uns]


if __name__ == "__main__":
    print("Begin to process !")
    asyncio.run(main())  # Process in chunks of 10
