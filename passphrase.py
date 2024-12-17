#!/usr/bin/env python3

# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "typer",
#     "wordfreq",
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

It draws from the most frequent words in the English language.
This ensures memorability by choosing common, easily recognized words.

It limits the wordlist to words with unique 3-letter prefixes.
The unique prefix approach enables users to potentially shorten the passphrase
while maintaining readability, as each prefix corresponds to a distinct word.

Usage:
    $ uv run passphrase_generator.py --help
"""

import math
import secrets
import string
from typing import Annotated

import typer
import wordfreq

PREFIX_SIZE = 3
WORDLIST_SIZE = 1024


def get_wordlist() -> list[str]:
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
            if len(short_words) >= WORDLIST_SIZE:
                break
    return short_words


# Global wordlist for passphrase generation
WORDLIST = sorted(get_wordlist().values())


def get_passphrase(wordlist: list[str], k: int = 6) -> list[str]:
    """Generate a random passphrase by selecting k words from the wordlist."""
    return [secrets.choice(wordlist) for _ in range(k)]


def concat_words(words: list[str]) -> str:
    """Concat word prefixes in passphrase."""
    return "".join([word[:PREFIX_SIZE] for word in words])


def main(
    k: Annotated[
        int,
        typer.Option(
            "-k", "--num-wrods", help="Number of words in each generated passphrase"
        ),
    ] = 7,
    repeat: Annotated[
        int,
        typer.Option("-r", "--num-phrases", help="Number of passphrases to generate"),
    ] = 10,
    *,
    hide_entropy: Annotated[
        bool,
        typer.Option(
            "--hide-entropy/--show-entropy", help="Hide entropy calculation information"
        ),
    ] = False,
    show_short_version: Annotated[
        bool,
        typer.Option(help="Show the concatenated short version of the passphrase"),
    ] = False,
) -> None:
    """Generate multiple passphrases and optionally display entropy information."""
    n = len(WORDLIST)
    choices = n**k
    entropy = math.log2(choices)
    entropy10 = math.log10(choices)
    if not hide_entropy:
        print(f"naive {entropy = :.1f} bits, {entropy10:.2f} digits\n")
    for _ in range(repeat):
        words = get_passphrase(WORDLIST, k=k)
        if show_short_version:
            print(concat_words(words), end="\t")
        print(" ".join(words))


if __name__ == "__main__":
    typer.run(main)
