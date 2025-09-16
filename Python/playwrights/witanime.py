from playwright.async_api import async_playwright
import asyncio
import json
from pathlib import Path


async def main(*urls):
    async with async_playwright() as p:
        browser = await p.firefox.launch(slow_mo=3000)

        context = await browser.new_context()
        page = await context.new_page()
        for url in urls:
            print("="*30)
            await page.goto(url, wait_until="domcontentloaded")
            servers = await page.evaluate("""() => {
                    const footer = document.querySelector('#ULEpisodesList').querySelectorAll('li');
                    return footer;
                }""")

            jj = 0
            while jj < len(servers):

                # Click element via evaluate
                await page.evaluate("""(index) => {
                        const footer = document.querySelector('#ULEpisodesList').querySelectorAll('a');
                        footer[index].click();
                    }""", jj)
                jj += 1
                await asyncio.sleep(1)  # Prefer asyncio.sleep in async code
                await fetch_data(page, context)

        # Create context first
        await browser.close()


async def fetch_data(page, context):

    pages = context.pages

    # Close all tabs but the first one
    for p in pages[1:]:
        await p.close()
    # Click element via evaluate
    shortlink = await page.evaluate("""() => {
            const footer = document.querySelector("link[rel='shortlink']");
            p = footer.href.split('=').pop();
            return p;
        }""")

    if Path(f"/home/mohamed/Documents/datas/Witanimes/{shortlink}.json").exists():
        return 0

    titre = await page.evaluate("""() => {
            const footer = document.querySelector('h3');
            p = footer.textContent;
            return p;
        }""")

    # Click element via evaluate
    servers = await page.evaluate("""() => {
            const footer = document.querySelectorAll('.server-link');
            return footer;
        }""")

    i = 0

    iframe = ""
    iframes = {}

    while i < len(servers):

        # Click element via evaluate
        key = await page.evaluate("""(index) => {
                const footer = document.querySelectorAll('.server-link');
                footer[index].click();
                return footer[index].textContent.trim();
            }""", i)

        i += 1

        # Wait for iframe or whatever needs to load
        await asyncio.sleep(1)  # Prefer asyncio.sleep in async code

        # Now get all pages in the same context (including your original page + new tabs if any)
        pages = context.pages

        # Close all tabs but the first one
        for p in pages[1:]:
            await p.close()
        while True:
            # Get iframe src on the first page
            iframe_src = await page.evaluate("""() => {
                    const iframe = document.querySelector('#iframe-container').querySelector('iframe');
                    return iframe.src;
                }""")
            if iframe != iframe_src:
                iframe = iframe_src
                break
            await asyncio.sleep(0.5)
        print(">", key)
        iframes[key] = iframe_src

    # Keep browser open for a while to observe

    with open(f"/home/mohamed/Documents/datas/Witanimes/{shortlink}.json", "w") as fl:
        json.dump({"iframes": iframes, "titre": titre}, fl)
    return 1

urls = [
    "https://witanime.cyou/episode/kusuriya-no-hitorigoto-2nd-season-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-1/",
    "https://witanime.cyou/episode/a-rank-party-wo-ridatsu-shita-ore-wa-moto-oshiego-tachi-to-meikyuu-shinbu-wo-mezasu-%d8%a7%d9%84%d8%ad%d9%84%d9%82%d8%a9-18/"
]
asyncio.run(main(*urls))
