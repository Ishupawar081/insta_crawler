import asyncio
import time
import random
from datetime import datetime, timedelta
from main import crawl_urls
import config

RUN_HOURS = 24
NORMAL_SLEEP_RANGE = (60, 180)
BLOCK_SLEEP = 600

end_time = datetime.now() + timedelta(hours=RUN_HOURS)

run_count = 0
total_links = 0
last_tag = None

while datetime.now() < end_time:

    run_count += 1

    print("\n==============================")
    print(f" Run {run_count}")
    print("Time:", datetime.now().strftime("%H:%M:%S"))

    # pick hashtag safely
    while True:
        new_tag = random.choice(config.HASHTAGS)
        if new_tag != last_tag:
            break

    last_tag = new_tag

    print("Using hashtag:", new_tag)

    try:
        links_found = asyncio.run(crawl_urls(new_tag, run_count))
        total_links += links_found

        print(f" Found {links_found} links this run")
        print(f" Total collected: {total_links}")

    except Exception as e:
        print(" Error:", e)
        links_found = 0

    if links_found == 0:
        print(" Bad hashtag → quick switch\n")
        time.sleep(5)
    else:
        sleep_time = random.randint(*NORMAL_SLEEP_RANGE)
        print(f" Sleeping {sleep_time} sec...\n")
        time.sleep(sleep_time)

print("\n 24-hour crawling complete")
