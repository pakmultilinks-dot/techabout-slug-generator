#!/usr/bin/env python3
"""
Slug Generator
==============

Turns an article title into a clean URL slug.

A slug is the URL-friendly form of a title, for example:

    "10 AI Trends to Watch in 2026!"  ->  "10-ai-trends-to-watch-in-2026"

Rules applied, in order:
  1. Unicode characters are transliterated to ASCII (Cafe -> cafe,
     naive -> naive, German sharp s -> ss).
  2. Everything is lowercased.
  3. Any run of characters that is not a letter or digit becomes a single
     hyphen (spaces, punctuation, symbols, underscores...).
  4. Leading and trailing hyphens are removed; repeated hyphens collapse.
  5. Optionally truncated to --max-length characters without cutting a
     word in half (the cut happens at the last hyphen inside the limit).
  6. An empty result falls back to "untitled" (configurable).

Usage as a function:
    from slug_generator import slugify
    slugify("Hello, World!")   # -> "hello-world"

Usage as a script:
    python slug_generator.py "My Article Title"
    python slug_generator.py --file titles.txt --output slugs.txt
    python slug_generator.py "A Very Long Title ..." --max-length 40

TechAbout Python Developer task 7 - Slug Generator (ZR-26-00754).
"""

import argparse
import sys
import unicodedata
import re

NON_ALNUM_RE = re.compile(r"[^a-z0-9]+")
MULTI_HYPHEN_RE = re.compile(r"-{2,}")


def transliterate(text):
    """Rough ASCII transliteration: decompose unicode, drop what is left."""
    decomposed = unicodedata.normalize("NFKD", text)
    ascii_only = decomposed.encode("ascii", "ignore").decode("ascii")
    return ascii_only


def slugify(title, max_length=0, fallback="untitled"):
    """Turn an article title into a clean URL slug."""
    if title is None:
        title = ""
    slug = transliterate(str(title)).lower()
    slug = NON_ALNUM_RE.sub("-", slug)
    slug = MULTI_HYPHEN_RE.sub("-", slug).strip("-")

    if max_length and len(slug) > max_length:
        cut = slug[:max_length]
        hyphen = cut.rfind("-")
        slug = (cut[:hyphen] if hyphen > 0 else cut).rstrip("-")

    return slug if slug else fallback


def slugify_file(input_path, output_path=None, max_length=0):
    """Slugify every non-empty line of a titles file. Returns the slugs."""
    with open(input_path, "r", encoding="utf-8") as fh:
        titles = [line.rstrip("\n") for line in fh]
    slugs = [slugify(t, max_length=max_length) for t in titles if t.strip()]
    if output_path:
        with open(output_path, "w", encoding="utf-8") as fh:
            for title, slug in zip([t for t in titles if t.strip()], slugs):
                fh.write("%s -> %s\n" % (title, slug))
    return slugs


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Turn article titles into clean URL slugs.")
    parser.add_argument("titles", nargs="*",
                        help="One or more article titles")
    parser.add_argument("--file", default="",
                        help="File with one title per line")
    parser.add_argument("--output", default="",
                        help="Write 'title -> slug' lines to this file")
    parser.add_argument("--max-length", type=int, default=0,
                        help="Max slug length; cuts at a word boundary (default: no limit)")
    args = parser.parse_args(argv)

    titles = list(args.titles)
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as fh:
                titles.extend(line.rstrip("\n") for line in fh if line.strip())
        except FileNotFoundError:
            print("Error: file not found: %s" % args.file, file=sys.stderr)
            return 1

    if not titles:
        print("Error: no titles given", file=sys.stderr)
        return 1

    lines = ["%s -> %s" % (t, slugify(t, max_length=args.max_length))
             for t in titles]
    out = "\n".join(lines)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(out + "\n")
        print("Wrote %d slugs to %s" % (len(lines), args.output))
    else:
        print(out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
