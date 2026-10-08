# Slug Generator

A function (plus CLI) that turns an article title into a clean URL slug.
Built for TechAbout task 7 (ZR-26-00754).

## What it does

`slugify(title)` applies these rules in order:

1. Unicode characters are transliterated to ASCII (`Café` -> `cafe`)
2. Everything is lowercased
3. Any run of non-letters/digits becomes a single hyphen
4. Leading/trailing hyphens removed, repeats collapsed
5. Optional `--max-length` truncates at a word boundary (never mid-word)
6. Empty results fall back to `"untitled"`

Example: `"10 AI Trends to Watch in 2026!"` -> `"10-ai-trends-to-watch-in-2026"`

## Usage

```python
from slug_generator import slugify
slugify("Hello, World!")   # "hello-world"
slugify("A Very Long Title ...", max_length=40)
```

```bash
python slug_generator.py "My Article Title"
python slug_generator.py --file titles.txt --output slugs.txt
python slug_generator.py "A Very Long Title ..." --max-length 40
```

## Sample output

`sample/titles.txt` holds 10 article titles; `sample/slugs.txt` holds the
generated slugs, one `title -> slug` line each.

## Tests

```bash
python test_slug_generator.py
```

14 tests (the task asked for 10) covering punctuation, collapsing,
stripping, underscores, unicode, numbers, empty input, custom fallback,
max-length word-boundary cuts, and idempotence.

## Files

| File | Purpose |
|---|---|
| `slug_generator.py` | The `slugify` function + CLI |
| `test_slug_generator.py` | 14 unit tests |
| `sample/titles.txt` | 10 sample article titles |
| `sample/slugs.txt` | Generated slugs |
