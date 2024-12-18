#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pooch",
#     "tqdm",
#     "wordfreq",
# ]
# ///
"""
alternative to the [method][eff-method] that is used to create EFF short wordlist.

[eff-method]: https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases
"""

import csv
import difflib
import string
from pathlib import Path

import pooch
import tqdm
import wordfreq


def filter_by_prefix(wordlist: list[str], prefix_size: int) -> list[str]:
    """Filter wordlist to only have distinct prefixes."""
    output: dict[str, str] = {}
    for word in wordlist:
        if len(word) >= prefix_size and word[:prefix_size] not in output:
            output[word[:prefix_size]] = word
    return list(output.values())


def write_wordlist(fn: Path, wordlist: list[str]) -> None:
    """Write the wordlist to a file."""
    fn.write_text("\n".join(wordlist) + "\n")


if __name__ == "__main__":
    output_size = 6**4
    max_similarity = 0.75
    # load eff_large_fn
    eff_large_fn = Path(
        pooch.retrieve(
            url="https://www.eff.org/files/2016/07/18/eff_large_wordlist.txt",
            known_hash="addd35536511597a02fa0a9ff1e5284677b8883b83e986e43f15a3db996b903e",
        )
    )
    eff_large_wordlist = [
        line.split("\t")[1] for line in eff_large_fn.read_text().splitlines()
    ]
    # filter non-lowercase
    eff_large_wordlist = [
        word
        for word in eff_large_wordlist
        if set(word).issubset(string.ascii_lowercase)
    ]
    # sort by freq
    eff_large_wordlist = sorted(
        eff_large_wordlist, key=lambda w: -wordfreq.word_frequency(w, "en")
    )
    write_wordlist(Path("output/eff_large_common_wordlist.txt"), eff_large_wordlist)
    write_wordlist(
        Path("output/eff_short_common_wordlist.txt"), eff_large_wordlist[:output_size]
    )
    # filter by prefix
    prefix_wordlist = filter_by_prefix(eff_large_wordlist, 3)
    write_wordlist(
        Path("output/eff_short_prefix_wordlist.txt"), prefix_wordlist[:output_size]
    )
    # filter by distance
    distinct_wordlist = []
    for word in tqdm.tqdm(eff_large_wordlist):
        similar = difflib.get_close_matches(word, distinct_wordlist, 1, max_similarity)
        if len(similar) > 0:
            continue
        distinct_wordlist.append(word)
    write_wordlist(
        Path("output/eff_short_distinct_wordlist.txt"), distinct_wordlist[:output_size]
    )
    # create a csv of all files
    common = {w: i for i, w in enumerate(eff_large_wordlist)}
    prefix = {w: i for i, w in enumerate(prefix_wordlist)}
    distinct = {w: i for i, w in enumerate(distinct_wordlist)}
    with Path("output/all_lists.csv").open("w", newline="", encoding="utf8") as csvfile:
        writer = csv.writer(csvfile, lineterminator="\n")
        writer.writerow(["word", "common", "prefix", "distinct"])
        for word in sorted(eff_large_wordlist):
            writer.writerow(
                [
                    word,
                    common.get(word, -1),
                    prefix.get(word, -1),
                    distinct.get(word, -1),
                ]
            )
