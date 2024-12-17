#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "typer",
#     "wordfreq",
# ]
# ///
import math
import secrets
import string

import typer
import wordfreq


def get_wordlist() -> list[str]:
    prefix_size = 3
    wordlist_size = 1024
    short_words = {}
    for word in wordfreq.iter_wordlist("en"):
        if word != word.lower():
            continue
        if not set(word).issubset(string.ascii_lowercase):
            continue
        if len(word) >= prefix_size and word[:prefix_size] not in short_words:
            short_words[word[:prefix_size]] = word
            if len(short_words) >= wordlist_size:
                break
    return short_words


WORDLIST = list(get_wordlist().values())


def get_passphrase(wordlist: list[str], k: int = 6) -> list[str]:
    return [secrets.choice(wordlist) for _ in range(k)]


def main(k: int = 7, repeat: int = 10, *, hide_entropy: bool = False) -> None:
    n = len(WORDLIST)
    choices = n**k
    entropy = math.log2(choices)
    entropy10 = math.log10(choices)
    if not hide_entropy:
        print(f"naive {entropy = } bits, {entropy10:.2f} digits\n")
    for _ in range(repeat):
        words = get_passphrase(WORDLIST, k=k)
        print(" ".join(words))


if __name__ == "__main__":
    typer.run(main)
