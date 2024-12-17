#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "typer>=0.9.0",
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
Calculate entropy of choosing repeatly from a list.

# Usage
If you have [uv installed](https://docs.astral.sh/uv/getting-started/installation/):
    $ ./entropy.py --help

Or:
    $ uv run entropy.py --help

Alternatively, install the dependencies and run:
    $ python entropy.py --help
"""

import math

import typer

RATES = {
    "online_throttling": 0.1,
    "keepass_default_decryption_time": 1,
    "online_no_throttling": 10,
    # "rate_from_xkcd_comic": 1000,
    "offline_slow_hashing": int(1e4),
    "offline_medium_hashing": int((1e4 * 1e10) ** 0.5),
    "offline_fast_hashing": int(1e10),
    "kraxx": int(1.4e12),
}


def print_entropy_data(n_choices: int) -> None:
    """Print the entropy and time to crack for a number of choices."""
    print(f"for {n_choices:,} choices")
    entropy = math.log2(n_choices)
    entropy10 = math.log10(n_choices)
    print(f"naive {entropy = :.1f} bits, {entropy10:.2f} digits")
    rate_name_len = max(len(name) for name in RATES)
    for rate_name, rate in RATES.items():
        rate_name_justified = f"[{rate_name}]".ljust(rate_name_len + 2)
        seconds_to_guess = n_choices / rate
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


def main(s: str) -> None:
    """Display entropy information."""
    s = s.replace("^", "**")
    if "**" in s:
        base, exp = s.split("**")
        if "*" in exp:
            a, b = exp.split("*")
            exp = int(a) * int(b)
        n = int(base) ** int(exp)
    else:
        n = int(s)
    print_entropy_data(n)


if __name__ == "__main__":
    typer.run(main)
