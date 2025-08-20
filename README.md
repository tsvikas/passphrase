# Passphrase Generation Tools

A Python toolkit for generating secure, memorable passphrases using common English words instead of obscure dictionary terms. Inspired by [XKCD 936](https://xkcd.com/936/), this creates passphrases like "happy mountain garden silver ocean" that are both secure and easy to remember.

## Why Not Use EFF's Wordlist Directly?

The [EFF large wordlist](https://www.eff.org/document/passphrase-wordlists) contains many problematic words:

- **Unfamiliar terms**: "vexingly", "astute"
- **Hard to spell**: "extenuate", "plethora"
- **Similar words**: "vivid"/"vividly", "climate"/"climatic"

This is especially problematic for non-English speakers. Our approach prioritizes **memorability** by using frequency-ranked common words, even though it requires longer phrases for equivalent security.

## Tools

### `passphrase.py` - Main Generator

Generate secure passphrases with entropy analysis:

```bash
# Basic usage (requires uv)
./passphrase.py

# Generate 6-word passphrases with unique prefixes
./passphrase.py --words 6 --prefix

# Generate 10 passphrases, show shortened versions
./passphrase.py --phrases 10 --short
```

**Two wordlist modes:**

- `--prefix`: Words with unique 3-letter prefixes (enables "subject" → "sub" shortcuts)
- `--no-prefix`: Distinct words filtered by similarity to avoid confusion

### `create_wordlist.py` - Wordlist Builder

Download and process wordlists from EFF data:

```bash
./create_wordlist.py
```

Creates filtered wordlists in `output/`:

- `eff_large_common_wordlist.txt`: Full EFF list sorted by frequency
- `eff_short_common_wordlist.txt`: Top 1296 most common words
- `eff_short_prefix_wordlist.txt`: Words with unique 3-letter prefixes
- `eff_short_distinct_wordlist.txt`: Words filtered for similarity

### `entropy.py` - Security Calculator

Calculate entropy and crack times for any number of choices:

```bash
./entropy.py "6**4"        # 1296 choices (6^4)
./entropy.py "2048"        # 2048 choices
./entropy.py "10**6"       # 1 million choices
```

Shows crack times across attack scenarios from online throttled to GPU clusters.

## Alternative: Using xkcdpass

If you prefer the popular `xkcdpass` tool, you can use our processed wordlists:

```bash
# Install xkcdpass
pip install xkcdpass

# Use our frequency-ranked wordlists
xkcdpass -w output/eff_short_common_wordlist.txt
xkcdpass -w output/eff_short_distinct_wordlist.txt

# Compare with original EFF
xkcdpass  # uses built-in EFF wordlist
```

## Installation

**With uv (recommended):**

```bash
# Scripts include inline dependencies - just run them
./passphrase.py --help
```

**Manual installation:**

```bash
pip install typer wordfreq pooch tqdm
python passphrase.py --help
```
