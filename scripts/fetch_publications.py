"""Fetch the lab's publication list and cache it as src/data/publications.json.

Primary source:  Google Scholar profile (scraped — Scholar has no official API).
Fallback source: OpenAlex (official free API).

If both sources fail but a previous publications.json exists, the script exits
successfully without touching it, so the website always keeps the last good data.

Run manually:  python scripts/fetch_publications.py
Run on CI:     .github/workflows/refresh-publications.yml (weekly + manual button)
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

SCHOLAR_USER_ID = "AU79cbgAAAAJ"  # Dr. Philippe Gray
OPENALEX_AUTHOR_ID = "A5018395052"  # Dr. Philippe Gray (University of Calgary)
CONTACT_EMAIL = "philippe.gray@ucalgary.ca"  # polite-pool contact for OpenAlex

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "src" / "data" / "publications.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch_google_scholar() -> list[dict]:
    """Scrape all publications from the Google Scholar profile (100 per page)."""
    pubs: list[dict] = []
    start = 0
    page_size = 100
    while True:
        url = (
            "https://scholar.google.com/citations"
            f"?user={SCHOLAR_USER_ID}&hl=en&cstart={start}&pagesize={page_size}&view_op=list_works"
        )
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code != 200:
            raise RuntimeError(f"Scholar returned HTTP {resp.status_code}")
        if "gs_captcha" in resp.text or "unusual traffic" in resp.text:
            raise RuntimeError("Scholar served a CAPTCHA page")

        soup = BeautifulSoup(resp.text, "html.parser")
        rows = soup.select("tr.gsc_a_tr")
        if start == 0 and not rows:
            raise RuntimeError("Scholar page had no publication rows (layout change or block)")

        for row in rows:
            title_el = row.select_one("a.gsc_a_at")
            if title_el is None:
                continue
            gray = row.select(".gs_gray")
            authors = gray[0].get_text(" ", strip=True) if len(gray) > 0 else ""
            venue = ""
            if len(gray) > 1:
                venue_el = gray[1]
                # The venue line ends with a ", 2020"-style year span — drop it.
                for span in venue_el.select(".gs_oph"):
                    span.decompose()
                venue = venue_el.get_text(" ", strip=True).rstrip(",").strip()
                # Scholar truncates long venue names with "<nbsp>…" — drop the marker
                venue = venue.rstrip(chr(8230) + chr(160) + chr(32)).strip()

            cites_el = row.select_one(".gsc_a_ac")
            cites_text = cites_el.get_text(strip=True) if cites_el else ""
            citations = int(cites_text) if cites_text.isdigit() else 0

            year_el = row.select_one(".gsc_a_h, td.gsc_a_y span")
            year_text = year_el.get_text(strip=True) if year_el else ""
            year = int(year_text) if re.fullmatch(r"\d{4}", year_text) else None

            href = title_el.get("href") or ""
            url_abs = f"https://scholar.google.com{href}" if href.startswith("/") else href

            pubs.append(
                {
                    "title": title_el.get_text(" ", strip=True),
                    "authors": authors,
                    "venue": venue,
                    "year": year,
                    "citations": citations,
                    "url": url_abs or None,
                }
            )

        if len(rows) < page_size:
            break
        start += page_size

    if not pubs:
        raise RuntimeError("Scholar scrape produced zero publications")
    return pubs


def fetch_openalex() -> list[dict]:
    """Fetch publications from the OpenAlex API (official, no scraping)."""
    pubs: list[dict] = []
    cursor = "*"
    while cursor:
        url = (
            "https://api.openalex.org/works"
            f"?filter=author.id:{OPENALEX_AUTHOR_ID}"
            f"&per-page=200&cursor={cursor}&mailto={CONTACT_EMAIL}"
        )
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        for work in data.get("results", []):
            authors = ", ".join(
                a.get("author", {}).get("display_name", "")
                for a in work.get("authorships", [])
                if a.get("author", {}).get("display_name")
            )
            source = (work.get("primary_location") or {}).get("source") or {}
            venue = source.get("display_name") or ""
            url_best = (
                work.get("doi")
                or (work.get("primary_location") or {}).get("landing_page_url")
                or work.get("id")
            )
            pubs.append(
                {
                    "title": work.get("display_name") or "Untitled",
                    "authors": authors,
                    "venue": venue,
                    "year": work.get("publication_year"),
                    "citations": work.get("cited_by_count", 0),
                    "url": url_best,
                }
            )

        cursor = data.get("meta", {}).get("next_cursor")
        if not data.get("results"):
            break

    if not pubs:
        raise RuntimeError("OpenAlex returned zero publications")
    return pubs


def main() -> int:
    source = None
    pubs: list[dict] = []

    try:
        print("Fetching from Google Scholar...")
        pubs = fetch_google_scholar()
        source = "google-scholar"
        print(f"  OK - {len(pubs)} publications")
    except Exception as exc:  # noqa: BLE001 - any failure falls back to OpenAlex
        print(f"  Google Scholar failed: {exc}")
        try:
            print("Falling back to OpenAlex...")
            pubs = fetch_openalex()
            source = "openalex"
            print(f"  OK - {len(pubs)} publications")
        except Exception as exc2:  # noqa: BLE001
            print(f"  OpenAlex failed: {exc2}")

    if not pubs:
        if OUTPUT_PATH.exists():
            print("Both sources failed - keeping existing publications.json unchanged.")
            return 0
        print("Both sources failed and no cached data exists.")
        return 1

    pubs.sort(key=lambda p: (-(p["year"] or 0), -p["citations"]))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(
            {
                "source": source,
                "updated": datetime.now(timezone.utc).isoformat(),
                "publications": pubs,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {OUTPUT_PATH} ({len(pubs)} publications, source: {source})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
