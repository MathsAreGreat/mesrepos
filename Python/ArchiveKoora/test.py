from playwright.sync_api import sync_playwright

urls = ["https://example.com", "https://example.org", "https://example.net"]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    all_links = {}

    for url in urls:
        page.goto(url)
        page.wait_for_selector(".hd_btn")

        buttons = page.query_selector_all(".hd_btn")
        links = [
            btn.get_attribute("data-url")
            for btn in buttons
            if btn.get_attribute("data-url")
        ]

        all_links[url] = links

    browser.close()

# Print results
for site, links in all_links.items():
    print(f"\nLinks from {site}:")
    for link in links:
        print("  ", link)
