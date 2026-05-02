#!/usr/bin/env python3
"""
MassTamilan Song Downloader  (anti-403 edition)
Downloads ZIP files (320kbps or 128kbps) for all movies in a year range.

Install:
    pip install cloudscraper beautifulsoup4

Usage:
    python masstamilan_downloader.py
"""

import os
import re
import time
import cloudscraper
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ── Config ──────────────────────────────────────────────────────────────────
BASE_URL     = "https://masstamilan.dev"
YEAR_FROM    = 2000        # ← Start year (inclusive) 1952 - 1957 (Completed)
YEAR_TO      = 2026        # ← End year (inclusive)
QUALITY      = "320"       # "320" or "128"
DOWNLOAD_DIR = "./downloads"   # Saves as ./downloads/{year}/
DELAY        = 3           # seconds between requests
# ────────────────────────────────────────────────────────────────────────────

scraper = cloudscraper.create_scraper(
    browser={"browser": "chrome", "platform": "windows", "mobile": False}
)
scraper.headers.update({
    "Accept-Language": "en-US,en;q=0.9,ta;q=0.8",
    "Accept":          "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer":         BASE_URL,
})


def get_soup(url: str) -> BeautifulSoup | None:
    try:
        r = scraper.get(url, timeout=30)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"  [ERROR] {url}\n         {e}")
        return None


def get_all_movies_for_year(year: int) -> list[dict]:
    movies = []
    page   = 1

    while True:
        url  = f"{BASE_URL}/browse-by-year/{year}?ref=mi&page={page}"
        print(f"  [*] Page {page}: {url}")
        soup = get_soup(url)
        if soup is None:
            break

        found = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if re.search(r"-songs/?$", href) and href not in found:
                found.append(href)
                # Derive clean title from the URL slug (e.g. "anbu-kattalai-songs" → "Anbu Kattalai")
                slug  = href.rstrip("/").split("/")[-1]
                slug  = re.sub(r"-songs$", "", slug)
                title = slug.replace("-", " ").title()
                movies.append({
                    "title": title,
                    "url":   urljoin(BASE_URL, href),
                })

        if not found:
            print(f"  No more movies on page {page} — done.")
            break

        print(f"  → {len(found)} movies found (running total: {len(movies)})")

        # Always try next page; stop only when a page returns nothing
        page += 1
        time.sleep(DELAY)

    # Deduplicate
    seen, unique = set(), []
    for m in movies:
        if m["url"] not in seen:
            seen.add(m["url"])
            unique.append(m)
    return unique


def get_zip_url(movie_url: str, quality: str = "320") -> str | None:
    soup = get_soup(movie_url)
    if soup is None:
        return None

    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True).lower()
        href = a["href"].lower()
        if quality in text and ("zip" in text or ".zip" in href):
            return urljoin(BASE_URL, a["href"])

    for a in soup.find_all("a", href=True):
        if quality in a["href"] and ".zip" in a["href"].lower():
            return urljoin(BASE_URL, a["href"])

    return None


def download_file(url: str, dest_path: str) -> bool:
    if os.path.exists(dest_path):
        print(f"  [SKIP] Already exists: {os.path.basename(dest_path)}")
        return True
    try:
        print(f"  [DL]   {url}")
        with scraper.get(url, stream=True, timeout=180) as r:
            r.raise_for_status()
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            total      = int(r.headers.get("content-length", 0))
            downloaded = 0
            with open(dest_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=65536):
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total:
                        pct = downloaded * 100 // total
                        print(f"\r  {pct:3d}%  {downloaded//1024//1024} MB / {total//1024//1024} MB",
                              end="", flush=True)
            print()
        print(f"  [OK]   → {dest_path}")
        return True
    except Exception as e:
        print(f"\n  [ERROR] {e}")
        if os.path.exists(dest_path):
            os.remove(dest_path)
        return False


def sanitize(name: str) -> str:
    return re.sub(r'[\\/*?:"<>|]', "_", name).strip()


def process_year(year: int) -> tuple[int, int, int]:
    """Download all movies for a single year. Returns (ok, skip, fail)."""
    movies = get_all_movies_for_year(year)

    if not movies:
        return 0, 0, 0

    year_dir = os.path.join(DOWNLOAD_DIR, str(year))
    os.makedirs(year_dir, exist_ok=True)
    print(f"  Total unique movies: {len(movies)}\n")

    ok = skip = fail = 0

    for i, movie in enumerate(movies, 1):
        title = movie["title"] or f"movie_{i}"
        print(f"  [{i}/{len(movies)}] {title}")
        time.sleep(DELAY)

        zip_url = get_zip_url(movie["url"], quality=QUALITY)
        if not zip_url:
            print(f"    [WARN] No {QUALITY}kbps ZIP found — skipping.")
            fail += 1
            continue

        filename  = f"{sanitize(title)}_{QUALITY}kbps.zip"
        dest_path = os.path.join(year_dir, filename)

        if os.path.exists(dest_path):
            skip += 1
        elif download_file(zip_url, dest_path):
            ok += 1
        else:
            fail += 1

    return ok, skip, fail


def main():
    years = list(range(YEAR_FROM, YEAR_TO + 1))

    print(f"\n{'='*55}")
    print(f"  MassTamilan Downloader")
    print(f"  Years : {YEAR_FROM} → {YEAR_TO}  ({len(years)} years)")
    print(f"  Quality: {QUALITY}kbps ZIP")
    print(f"  Output : {os.path.abspath(DOWNLOAD_DIR)}/{{year}}/")
    print(f"{'='*55}\n")

    grand_ok = grand_skip = grand_fail = 0

    for year in years:
        print(f"\n{'─'*55}")
        print(f"  📅  Processing year: {year}")
        print(f"{'─'*55}")

        ok, skip, fail = process_year(year)
        grand_ok   += ok
        grand_skip += skip
        grand_fail += fail

        if ok + skip + fail == 0:
            print(f"  [SKIP] No movies found for {year} — ignoring.")
        else:
            print(f"\n  Year {year} done → ✓ {ok}  ⏭ {skip}  ✗ {fail}")

    print(f"\n{'='*55}")
    print(f"  ALL DONE!")
    print(f"  Years processed : {YEAR_FROM} – {YEAR_TO}")
    print(f"  ✓ Downloaded : {grand_ok}")
    print(f"  ⏭ Skipped    : {grand_skip}")
    print(f"  ✗ Failed     : {grand_fail}")
    print(f"  Folder: {os.path.abspath(DOWNLOAD_DIR)}/")
    print(f"{'='*55}\n")


if __name__ == "__main__":
    main()