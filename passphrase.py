#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "typer>=0.9.0",
#     "wordfreq>=1.0",
# ]
# ///

# MIT License
#
# Copyright (c) 2024 Tsvika Shapira
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Passphrase Generator with Memorable Word Selection.

This module helps create secure passphrases.
See [this XKCD comic](https://xkcd.com/936/) about passphrases.
To correctly use a passphrase, you need to make sure your selections are
chosen at random (i.e. don't pick them yourself) and that you use enough
bits of entropy.

This module draws from the most frequent words in the English language.
This ensures memorability by choosing common, easily recognized words.

It also limits the wordlist to words with unique 3-letter prefixes.
This enables users to shorten their passphrase while maintaining
readability, as each prefix corresponds to a distinct word.

This is instead of using the
[eff_large wordlist](https://www.eff.org/document/passphrase-wordlists)
which contains many obscure or hard to spell words.

Note that this means that the wordlist is shorter, and a longer phrase is
needed to reach the same entropy.

# Usage
If you have [uv installed](https://docs.astral.sh/uv/getting-started/installation/):
    $ ./passphrase_generator.py --help

Or:
    $ uv run passphrase_generator.py --help

Alternatively, install the dependencies and run:
    $ python passphrase_generator.py --help
"""

import math
import secrets
import string
from typing import Annotated

import typer
import wordfreq

PREFIX_SIZE = 3
RATES = {
    "online_throttling": 0.1,
    "keepass_default_decryption_time": 1,
    "online_no_throttling": 10,
    "offline_slow_hashing": int(1e4),
    "offline_medium_hashing": int((1e4 * 1e10) ** 0.5),
    "offline_fast_hashing": int(1e10),
    "kraxx": int(1.4e12),
}


def get_wordlist(wordlist_size: int) -> list[str]:
    """
    Generate a list of unique words from the English language.

    Words have unique 3-letter prefixes
    """
    short_words = {}
    for word in wordfreq.iter_wordlist("en"):
        if not set(word).issubset(string.ascii_lowercase):
            continue
        if len(word) >= PREFIX_SIZE and word[:PREFIX_SIZE] not in short_words:
            short_words[word[:PREFIX_SIZE]] = word
            if len(short_words) >= wordlist_size:
                break
    return short_words.values()


def to_base_n(
    num: int, b: int, numerals: str = "0123456789abcdefghijklmnopqrstuvwxyz"
) -> str:
    """Convert a number to an arbitrery base."""
    return (
        numerals[0]
        if num == 0
        else (to_base_n(num // b, b, numerals) + numerals[num % b]).lstrip(numerals[0])
    )


def print_diceware(dice: int = 6, rolls: int = 4) -> None:
    """
    Print a table for manually rolling a random word.

    This is not the exact wordlist used for this script.
    """
    wordlist = sorted(get_wordlist(dice**rolls))
    for i, word in enumerate(wordlist):
        numerals = "1234567890ET"[:dice]
        number = to_base_n(i, dice, numerals).rjust(rolls, numerals[0])
        print(number, word)


def get_passphrase(wordlist: list[str], k: int = 6) -> list[str]:
    """Generate a random passphrase by selecting k words from the wordlist."""
    return [secrets.choice(wordlist) for _ in range(k)]


def concat_words(words: list[str]) -> str:
    """Concat word prefixes in passphrase."""
    return "".join([word[:PREFIX_SIZE] for word in words])


def print_entropy_data(choices: int) -> None:
    """Print the entropy and time to crack for a number of choices."""
    entropy = math.log2(choices)
    entropy10 = math.log10(choices)
    print(f"naive {entropy = :.1f} bits, {entropy10:.2f} digits")
    rate_name_len = max(len(name) for name in RATES)
    for rate_name, rate in RATES.items():
        rate_name_justified = f"[{rate_name}]".ljust(rate_name_len + 2)
        seconds_to_guess = choices / rate
        last_size = seconds_to_guess
        last_unit = "seconds"
        for unit, unit_size in [
            ("minutes", 60),
            ("hours", 60),
            ("days", 24),
            ("months", 364.527 / 12),
            ("years", 12),
            ("thousand years", 1000),
            ("million years", 1000),
            ("billion years", 1000),
            ("trillion years", 1000),
        ]:
            if last_size / unit_size < 1:
                break
            last_size /= unit_size
            last_unit = unit
        print(
            f"at {rate:>13} guesses/sec {rate_name_justified}: "
            f"{last_size:.3n} {last_unit}"
        )


def main(
    k: Annotated[
        int,
        typer.Option(
            "-w", "--words", help="Number of words in each generated passphrase"
        ),
    ] = 7,
    repeat: Annotated[
        int,
        typer.Option("-p", "--phrases", help="Number of passphrases to generate"),
    ] = 8,
    *,
    show_entropy: Annotated[
        bool,
        typer.Option(
            "--entropy/--no-entropy",
            "-e/-E",
            help="Hide entropy calculation information",
        ),
    ] = True,
    show_short_version: Annotated[
        bool,
        typer.Option(
            "--short/--no-short",
            "-s/-S",
            help="Show the concatenated short version of the passphrase",
        ),
    ] = False,
    wordlist_bits: Annotated[
        int,
        typer.Option(
            "-b",
            "--wordlist_bits",
            help="Size of the wordlist, in bits",
        ),
    ] = 10,
) -> None:
    """Generate multiple passphrases and optionally display entropy information."""
    wordlist = sorted(get_wordlist(2**wordlist_bits))
    choices = len(wordlist) ** k
    if show_entropy:
        print_entropy_data(choices)
        print()
    for _ in range(repeat):
        words = get_passphrase(wordlist, k=k)
        if show_short_version:
            print(concat_words(words), end="\t")
        print(" ".join(words))


if __name__ == "__main__":
    typer.run(main)
