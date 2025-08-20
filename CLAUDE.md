# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based passphrase generation toolkit with three main utilities:

- `passphrase.py`: Main passphrase generator using common English words
- `create_wordlist.py`: Wordlist creation and preprocessing tool
- `entropy.py`: Entropy calculator for password strength analysis

## Core Architecture

### passphrase.py:222 (Main Generator)

- Uses `wordfreq` library to source common English words for memorability
- Supports two wordlist modes:
  - **unique_prefix**: Words with distinct 3-letter prefixes (enables shortened passphrases like "subject" → "sub")
  - **distinct**: Words filtered by similarity (avoids confusing similar words)
- Generates cryptographically secure passphrases using Python's `secrets` module
- Calculates entropy and crack time estimates across multiple attack scenarios

### create_wordlist.py:98 (Wordlist Builder)

- Downloads and processes the EFF large wordlist as source material
- Creates multiple filtered versions: common, prefix-unique, and distinct wordlists
- Outputs processed wordlists to `output/` directory
- Generates comparative analysis in CSV format

### entropy.py:90 (Security Calculator)

- Standalone entropy calculation tool
- Supports mathematical expressions (e.g., "6\*\*4", "2^10\*3")
- Shows crack time estimates across different attack rates (online throttled to offline GPU clusters)

## Running Scripts

All scripts use `uv` (Python package manager) with inline dependency declarations:

```bash
# Run main passphrase generator
./passphrase.py --help
uv run passphrase.py --words 6 --phrases 5 --prefix

# Generate wordlists (creates output/ directory)
./create_wordlist.py
uv run create_wordlist.py

# Calculate entropy for given number of choices
./entropy.py "6**4"  # 1296 choices
uv run entropy.py "2048"
```

### Alternative: xkcdpass Integration

Users can use the processed wordlists with the popular `xkcdpass` tool:

```bash
# After running create_wordlist.py
xkcdpass -w output/eff_short_common_wordlist.txt
xkcdpass -w output/eff_short_distinct_wordlist.txt
```

Alternative without uv (requires manual dependency installation):

```bash
python passphrase.py --help
python entropy.py "1000"
```

## Key Dependencies

Scripts use PEP 723 inline dependency specs:

- `typer`: CLI interface framework
- `wordfreq`: English word frequency data
- `pooch`: Secure file downloading (create_wordlist.py)
- `tqdm`: Progress bars (create_wordlist.py)

## Important Constants

- `PREFIX_SIZE = 3`: Length of unique prefixes for shortened passphrases
- Attack rate scenarios defined in `RATES` dict (both passphrase.py:54 and entropy.py:27)
- Default wordlist size: 2^10 (1024) words

## Security Model

The toolkit prioritizes:

1. **Cryptographic randomness**: Uses `secrets.choice()` for word selection
1. **Memorability**: Common English words vs. obscure dictionary terms
1. **Flexibility**: Multiple wordlist strategies for different use cases
1. **Transparency**: Detailed entropy calculations and attack time estimates
