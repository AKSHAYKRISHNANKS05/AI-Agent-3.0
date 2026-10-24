import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from urllib.parse import urlencode


def search_web(query):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        search_url = "https://www.duckduckgo.com/?" + urlencode({"q": query})

        try:
            page.goto(
                search_url,
                wait_until="domcontentloaded",
                timeout=30000
            )

            page.locator("h2").first.wait_for(timeout=15000)

            headings = page.locator("h2")

            for i in range(min(headings.count(), 5)):
                heading = headings.nth(i)
                link_element = heading.locator("a").first

                if link_element.count() == 0:
                    continue

                results.append({
                    "title": heading.inner_text(),
                    "link": link_element.get_attribute("href")
                })

        except PlaywrightTimeoutError:
            print("Search results could not be loaded.")



        finally:

            print("Browser will close in 5 seconds...")

            page.wait_for_timeout(5000)

            browser.close()

    return results


if __name__ == "__main__":
    data = search_web("What is Python programming?")

    print("\nReturned Search Results:")

    for number, item in enumerate(data, start=1):
        print(f"\n{number}. {item['title']}")
        print(f"Link: {item['link']}")
