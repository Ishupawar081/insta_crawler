# Instagram Hashtag Crawler

A Instagram hashtag crawler built using Python, AsyncIO, and Playwright.  
The crawler automatically visits Instagram hashtag pages, scrolls dynamically, extracts post/reel URLs, rotates hashtags and user agents, and stores collected links into text files.

This project is designed for long-running crawling sessions with simple anti-detection techniques such as randomized delays, scrolling patterns, and hashtag rotation.

---

# Features

- Async Playwright-based crawling
- Dynamic hashtag rotation
- Randomized user-agent selection
- Human-like scrolling behavior
- Retry handling for failed page loads
- Redirect detection
- Continuous long-duration crawling support
- Automatic URL extraction
- Lightweight and fast
- Saves collected URLs into text files
- Blocks images/media/fonts for faster execution

---


# Requirements

- Python 3.10+
- Playwright
- Chromium browser

---

# System Architecture

```text
                    +-------------------+
                    |   run_24h.py      |
                    |-------------------|
                    | Controls 24h loop |
                    | Picks hashtags    |
                    | Handles sleeping  |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |     main.py       |
                    |-------------------|
                    | Starts crawler    |
                    | Launches browser  |
                    | Extracts links    |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |   Playwright      |
                    |-------------------|
                    | Chromium Browser  |
                    | Page Navigation   |
                    | Dynamic Scrolling |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | Instagram Hashtag |
                    |       Pages       |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    | URL Extraction    |
                    |-------------------|
                    | /p/ posts         |
                    | /reel/ reels      |
                    | /tv/ videos       |
                    +---------+---------+
                              |
                              v
                    +-------------------+
                    |   Data Storage    |
                    |-------------------|
                    | run_<id>_<tag>.txt
                    | all_links.txt     |
                    +-------------------+
```

---
# Installation

## Clone Repository

```bash
[git clone https://github.com/Ishupawar081/insta_crawler]

cd insta-crawler
```

---

## Create Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install playwright
```

Install browser binaries:

```bash
playwright install
```

---

# Configuration

Edit `config.py` to customize hashtags and user agents.

## Example Hashtags

```python
HASHTAGS = [
    "ai",
    "machinelearning",
    "coding",
    "python"
]
```

---

## Example User Agents

```python
USER_AGENTS = [
    "Mozilla/5.0 ...",
    "Mozilla/5.0 ..."
]
```

---

# Usage

## Run Single Crawl

```bash
python main.py
```

This will:

- Open a hashtag page
- Scroll multiple times
- Extract post/reel URLs
- Save links into the `data/` directory

---

## Run Continuous Crawling

```bash
python run_24h.py
```

The crawler will:

- Randomly select hashtags
- Avoid repeating the previous hashtag
- Crawl continuously for 24 hours
- Save collected links into files

---

# How It Works

## Browser Launch

The crawler launches Chromium using Playwright:

```python
browser = await p.chromium.launch(
    channel="chrome",
    headless=False,
    slow_mo=50
)
```

---

## Resource Blocking

Images, media, and fonts are blocked to improve speed and reduce bandwidth usage.

```python
await page.route("**/*", lambda route: (
    route.abort() if route.request.resource_type in ["image", "media", "font"]
    else route.continue_()
))
```

---

## Human-Like Delays

Randomized delays simulate real browsing behavior.

```python
await asyncio.sleep(random.uniform(a, b))
```

---

## URL Extraction

The crawler extracts URLs containing:

- `/p/`
- `/reel/`
- `/tv/`

Example:

```python
if link and any(x in link for x in ["/p/", "/reel/", "/tv/"]):
```

---

# Output

## Individual Run Files

```text
data/run_1_ai.txt
data/run_2_python.txt
```

---

## Combined Dataset

```text
data/all_links.txt
```

---

# Example Output

```text
==============================
 Run 3
Time: 14:52:11

Using hashtag: machinelearning

 Scroll 1: 24 links
 Scroll 2: 51 links
 Scroll 3: 73 links

 Found 73 URLs
 Total collected: 211

 Sleeping 142 sec...
```

---

# Anti-Detection Techniques

The crawler includes several lightweight anti-detection strategies:

- Random delays
- User-agent rotation
- Dynamic scrolling
- Retry logic
- Redirect detection
- Random hashtag switching

---

# Future Improvements

Possible future enhancements:

- Proxy rotation
- Session/cookie handling
- Database storage
- Docker support
- Cloud deployment
- Headless stealth mode
- Parallel crawling
- Analytics dashboard

---

# Disclaimer

This project is intended for educational and research purposes only.

Users are responsible for complying with Instagram's Terms of Service and all applicable laws.

Use responsibly.

---

# License

MIT License
