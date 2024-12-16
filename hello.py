import string
import random

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


def main():
    for _ in range(8):
        words = random.choices(WORDLIST, k=6)
        print(" ".join(words))


if __name__ == "__main__":
    main()
