#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "typer>=0.9.0",
# ]
# ///

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
            n = int(base) ** (int(a) * int(b))
        elif "." in exp:
            n = int(int(base) ** float(exp))
        else:
            n = int(base) ** int(exp)
    else:
        n = int(s)
    print_entropy_data(n)


if __name__ == "__main__":
    typer.run(main)
