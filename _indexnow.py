# -*- coding: utf-8 -*-
"""
_indexnow.py - tell Bing (and the other IndexNow engines) which pages changed.

Why this exists
---------------
ChatGPT search leans on Bing, and on 9 Oct 2026 Bing's image index held no
photos from this site at all, so ChatGPT illustrated our listing with a
competitor's kiddush cup. IndexNow lets a site announce a changed URL the
moment it goes live instead of waiting for Bingbot's next visit. One POST to
api.indexnow.org is shared with Yandex, Seznam, Naver and Yep as well.

How it works
------------
The key below is public by design: the engines confirm ownership by fetching
https://shermanartworks.com/<KEY>.txt and checking it holds the same string.
Only URLs listed in sitemap.xml are ever submitted, so the blocked internal
tools and quote.html can never go out, and every URL is the canonical form.

The IndexNow workflow (.github/workflows/indexnow.yml) runs this after each
deploy to main with --since, and by hand with --all.
  python _indexnow.py --since <sha>            pages changed since that commit
  python _indexnow.py --all                    every URL in sitemap.xml
  add --dry-run to print the URLs without submitting them
"""

import argparse
import io
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

SITE = Path(__file__).resolve().parent
HOST = "shermanartworks.com"
BASE = "https://" + HOST
KEY = "eaed818c027d7bb8e791c15e141d7751"
ENDPOINT = "https://api.indexnow.org/indexnow"


def sitemap_urls():
    """Map each sitemap URL's source file (index.html, he/faq.html...) to the URL."""
    xml = io.open(SITE / "sitemap.xml", encoding="utf-8").read()
    urls = {}
    for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml):
        if not loc.startswith(BASE + "/"):
            continue
        path = loc[len(BASE) + 1:]
        if path == "" or path.endswith("/"):
            path += "index.html"
        urls[path] = loc
    return urls


def changed_files(since):
    """Files added, modified or renamed between `since` and HEAD, or None if
    `since` is not in this history (a force push, or the all-zero sha GitHub
    sends for a new branch)."""
    known = subprocess.run(["git", "cat-file", "-e", since + "^{commit}"],
                           cwd=str(SITE), capture_output=True)
    if known.returncode != 0:
        return None
    out = subprocess.run(["git", "diff", "--name-only", "--diff-filter=AMR",
                          since, "HEAD"],
                         cwd=str(SITE), capture_output=True, text=True, check=True)
    return out.stdout.split()


def submit(urls):
    body = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": "%s/%s.txt" % (BASE, KEY),
        "urlList": urls,
    }).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as err:
        return err.code, err.read().decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    which = ap.add_mutually_exclusive_group(required=True)
    which.add_argument("--since", metavar="SHA", help="submit pages changed since this commit")
    which.add_argument("--all", action="store_true", help="submit every URL in sitemap.xml")
    ap.add_argument("--dry-run", action="store_true", help="print the URLs, do not submit")
    args = ap.parse_args()

    key_file = SITE / (KEY + ".txt")
    if not key_file.exists() or io.open(key_file, encoding="utf-8").read().strip() != KEY:
        sys.exit("%s is missing or does not hold the key, so the engines would reject us." % key_file.name)

    pages = sitemap_urls()
    if args.all:
        urls = list(pages.values())
    else:
        files = changed_files(args.since)
        if files is None:
            print("%s is not in this history, so submitting every sitemap URL." % args.since)
            urls = list(pages.values())
        else:
            urls = [pages[f] for f in files if f in pages]

    if not urls:
        print("No sitemap pages changed, nothing to submit.")
        return
    print("%d URL(s):" % len(urls))
    for url in urls:
        print("  " + url)
    if args.dry_run:
        return

    status, text = submit(urls)
    # 200 means accepted, 202 means accepted while the key file is still being
    # checked. Anything else (400 bad request, 403 key not valid, 422 URL not on
    # this host, 429 too many requests) is a failure worth a red run.
    print("IndexNow answered %d %s" % (status, text.strip()[:300]))
    if status not in (200, 202):
        sys.exit(1)


if __name__ == "__main__":
    main()
