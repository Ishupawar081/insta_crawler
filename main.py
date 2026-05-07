import asyncio
import random
import os
from playwright.async_api import async_playwright
import config


async def human_delay(a=2, b=4):
    await asyncio.sleep(random.uniform(a, b))


async def crawl_urls(hashtag, run_id=None):
    print(f"Crawling hashtag: {hashtag}")

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            channel="chrome",
            headless=False,
            slow_mo=50
        )

        context = await browser.new_context(
            user_agent=random.choice(config.USER_AGENTS),
            viewport={"width": 1280, "height": 800}
        )

        page = await context.new_page()

        await page.route("**/*", lambda route: (
            route.abort() if route.request.resource_type in ["image", "media", "font"]
            else route.continue_()
        ))

        # retry logic
        for attempt in range(2):
            try:
                await page.goto(
                    f"https://www.instagram.com/explore/tags/{hashtag}/",
                    wait_until="domcontentloaded",
                    timeout=60000
                )
                break
            except:
                print(f" Retry {attempt+1} for {hashtag}")
                await asyncio.sleep(5)
        else:
            print(" Could not load page")
            await browser.close()
            return 0

        await human_delay(4, 6)

        print(" Current URL:", page.url)

        # detect redirect
        if hashtag not in page.url:
            print("Redirect detected → skipping")
            await browser.close()
            return 0

        post_links = set()

        for i in range(6):
            await page.mouse.wheel(0, random.randint(600, 1200))
            await asyncio.sleep(random.uniform(1.5, 2.5))

            links = await page.eval_on_selector_all(
                "a",
                "els => els.map(e => e.href)"
            )

            for link in links:
                if link and any(x in link for x in ["/p/", "/reel/", "/tv/"]):
                    post_links.add(link)

            print(f" Scroll {i+1}: {len(post_links)} links")

        print(f" Found {len(post_links)} URLs")

        os.makedirs("data", exist_ok=True)

        file_path = f"data/run_{run_id}_{hashtag}.txt"

        with open(file_path, "w") as f:
            for link in post_links:
                f.write(link + "\n")

        with open("data/all_links.txt", "a") as f:
            for link in post_links:
                f.write(link + "\n")

        await browser.close()

        return len(post_links)


if __name__ == "__main__":
    asyncio.run(crawl_urls("ai", 1))
