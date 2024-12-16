#!/usr/bin/env python3
import string
import random
import math

import typer
import wordfreq


def get_wordlist() -> list[str]:
    short_words = {}
    for word in wordfreq.iter_wordlist("en"):
        assert word == word.lower()
        if not set(word).issubset(string.ascii_lowercase):
            continue
        if len(word) >= 3 and word[:3] not in short_words:
            short_words[word[:3]] = word
            if len(short_words) >= 1024:
                break
    return short_words


WORDLIST = list(get_wordlist().values())


def get_passphrase(wordlist: list[str], k=6):
    return random.choices(WORDLIST, k=k)


def main(k: int = 7, repeat: int = 10, hide_entropy: bool = False):
    n = len(WORDLIST)
    entropy = math.log2(n**k)
    entropy10 = math.log10(n**k)
    if not hide_entropy:
        print(f"naive {entropy = } bits, {entropy10:.2f} digits")
    for _ in range(repeat):
        words = get_passphrase(WORDLIST, k=k)
        print(" ".join(words))


if __name__ == "__main__":
    typer.run(main)
