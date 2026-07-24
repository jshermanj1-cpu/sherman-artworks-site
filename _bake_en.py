# -*- coding: utf-8 -*-
"""
_bake_en.py — bake the English [data-t] copy into the static English pages.

Why this exists
---------------
Most [data-t] elements ship with their English text inline, but 108 of them
across 8 pages ship EMPTY and are filled only at runtime by setLang(). The
whole visible FAQ on contact.html and the whole process section on
custom-orders.html are in that group, which is why those pages measure 135 and
166 visible words in the raw HTML.

Anything that only exists after JS runs is invisible to crawlers that do not
execute it — the same GPTBot/ClaudeBot/PerplexityBot blind spot that
_he_pages.py was written to fix for Hebrew. It also breaks the rule that
structured data must correspond to content on the page: contact.html declares
six FAQPage entries whose text is nowhere in the delivered markup.

This script is the English mirror of _he_pages.py: it resolves each empty
[data-t] element against T_SITE/T_PAGE and writes the English string inline, so
the served HTML carries the copy that setLang() would have produced. setLang()
still runs and simply rewrites the same text, so runtime behaviour is unchanged.

Edits are surgical raw-text substitutions (no bs4 re-serialization) so diffs
stay reviewable. Idempotent: only elements that are literally empty are filled.
"""

import os
import re

import _he_pages as H

ROOT = os.path.dirname(os.path.abspath(__file__))

# Elements whose value is HTML rather than plain text (mirrors _he_pages.RICH_KEYS).
RICH_KEYS = H.RICH_KEYS

# <tag ... data-t="key" ...></tag>  — matches ONLY already-empty elements, so a
# page that already carries its English copy is left untouched.
EMPTY_EL = re.compile(r'(<(\w+)\b[^>]*\bdata-t="(\w+)"[^>]*>)(</\2>)')


def parse_dict(text, obj_marker, lang):
    """Extract the `<lang>: { ... }` sub-block of obj_marker. Mirrors
    _he_pages.parse_he_dict, which is hardcoded to the Hebrew branch."""
    start = text.find(obj_marker)
    if start < 0:
        return {}
    obj_open = text.find("{", start)
    if obj_open < 0:
        return {}
    obj_body = H._match_brace_block(text, obj_open)
    m = re.search(r"\b%s\s*:\s*\{" % lang, obj_body)
    if not m:
        return {}
    lang_open = obj_body.find("{", m.start())
    lang_body = H._match_brace_block(obj_body, lang_open)
    pairs = re.findall(
        r"(\w+)\s*:\s*(?:'((?:[^'\\]|\\.)*)'"
        r"|\"((?:[^\"\\]|\\.)*)\""
        r"|`((?:[^`\\]|\\.)*)`)",
        lang_body,
        re.S,
    )
    return {k: H._unescape(sq or dq or bt) for k, sq, dq, bt in pairs}


def site_en():
    with open(os.path.join(ROOT, "js", "site.js"), "r", encoding="utf-8") as f:
        return parse_dict(f.read(), "const T_SITE", "en")


T_SITE_EN = site_en()


def page_dict(src):
    """Merged English dictionary for one page: T_SITE first, page's own T_PAGE
    wins, plus the hero_<PAGE_KEY>_* aliases the shofar pages resolve at runtime."""
    d = dict(T_SITE_EN)
    d.update(parse_dict(src, "T_PAGE", "en"))
    mkey = re.search(r"const PAGE_KEY\s*=\s*'(\w+)'", src)
    if mkey:
        pk = mkey.group(1)
        for base in ("hero_headline", "hero_subtitle", "hero_body"):
            alias = base.replace("hero_", "hero_%s_" % pk)
            if d.get(alias):
                d[base] = d[alias]
        if d.get("bc_%s" % pk):
            d["bc_current"] = d["bc_%s" % pk]
    return d


def bake_page(page, dry_run=False):
    path = os.path.join(ROOT, page)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    d = page_dict(src)
    filled, skipped = [], []

    def repl(m):
        open_tag, _tag, key, close_tag = m.groups()
        val = d.get(key)
        if not val:
            skipped.append(key)
            return m.group(0)
        filled.append(key)
        body = val if key in RICH_KEYS else H.esc_html(val)
        return open_tag + body + close_tag

    # Only touch markup, never the inline <script> dictionaries themselves.
    parts = re.split(r"(<script\b.*?</script>)", src, flags=re.S)
    for i in range(0, len(parts), 2):
        parts[i] = EMPTY_EL.sub(repl, parts[i])
    out = "".join(parts)

    if out != src and not dry_run:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(out)
    return filled, skipped


def sync_howto(page="custom-orders.html", dry_run=False):
    """Rebuild the HowTo step[] from the same T_PAGE keys that render the visible
    step cards.

    The two had drifted badly: the markup declared five steps whose names
    ("Describe your vision", "Confirm the order", …) matched none of the four
    steps actually on the page ("Tell Us Your Vision", "We Design Together", …),
    so the structured data described a process the reader never sees. Generating
    the steps from step<N>_title/step<N>_body makes that drift impossible —
    the visible cards and the markup now have a single source.

    The HowTo name/description are left alone: they are page-level metadata, not
    step content, and the existing wording is better for search than the visible
    "How It Works" heading."""
    path = os.path.join(ROOT, page)
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    d = page_dict(src)

    steps = []
    i = 1
    while d.get("step%d_title" % i) and d.get("step%d_body" % i):
        steps.append({
            "@type": "HowToStep",
            "position": i,
            "name": d["step%d_title" % i],
            "text": d["step%d_body" % i],
        })
        i += 1
    if not steps:
        print("%s: no step<N>_title/body keys found, HowTo left untouched" % page)
        return 0

    def repl(m):
        import json
        block = m.group(2)
        if '"HowTo"' not in block:
            return m.group(0)
        obj = json.loads(block)
        obj["step"] = steps
        return m.group(1) + json.dumps(obj, ensure_ascii=False,
                                       separators=(",", ":")) + m.group(3)

    out = re.sub(r'(<script[^>]*ld\+json[^>]*>)(.*?)(</script>)', repl, src, flags=re.S)
    if out != src and not dry_run:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(out)
    print("%-24s HowTo synced to %d visible step(s)" % (page, len(steps)))
    return len(steps)


def main(dry_run=False):
    total_f = total_s = 0
    for page in H.PAGES:
        filled, skipped = bake_page(page, dry_run)
        total_f += len(filled)
        total_s += len(skipped)
        if filled or skipped:
            note = "filled %d" % len(filled)
            if skipped:
                note += ", no string for %d (%s)" % (
                    len(skipped), ", ".join(sorted(set(skipped))[:5]))
            print("%-24s %s" % (page, note))
    print("\n%s: %d element(s) baked, %d left empty (no dictionary entry)"
          % ("DRY RUN" if dry_run else "DONE", total_f, total_s))
    print()
    sync_howto(dry_run=dry_run)


if __name__ == "__main__":
    import sys
    main(dry_run="--dry-run" in sys.argv)
