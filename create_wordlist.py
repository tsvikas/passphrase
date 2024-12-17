#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pooch",
#     "wordfreq",
# ]
# ///
import string
from pathlib import Path

import pooch
import wordfreq


def filter_by_prefix(wordlist: list[str], prefix_size: int) -> list[str]:
    output: dict[str, str] = {}
    for word in wordlist:
        if len(word) >= prefix_size and word[:prefix_size] not in output:
            output[word[:prefix_size]] = word
    return list(output.values())


def write_wordlist(fn: Path, wordlist: list[str]) -> None:
    fn.write_text("\n".join(sorted(wordlist)) + "\n")


if __name__ == "__main__":
    output_fn = Path("short_wordlist.txt")
    output_size = 6**4
    eff_large_fn = Path(
        pooch.retrieve(
            url="https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt",
            known_hash="addd35536511597a02fa0a9ff1e5284677b8883b83e986e43f15a3db996b903e",
        )
    )
    eff_large_wordlist = [
        line.split("\t")[1] for line in eff_large_fn.read_text().splitlines()
    ]
    eff_large_wordlist = [
        word
        for word in eff_large_wordlist
        if set(word).issubset(string.ascii_lowercase)
    ]
    eff_large_wordlist = sorted(
        eff_large_wordlist, key=lambda w: -wordfreq.word_frequency(w, "en")
    )
    write_wordlist(
        Path("eff_large_common_wordlist.txt"), eff_large_wordlist[:output_size]
    )
    prefix_wordlist = filter_by_prefix(eff_large_wordlist, 3)
    write_wordlist(Path("eff_large_prefix_wordlist.txt"), prefix_wordlist[:output_size])
