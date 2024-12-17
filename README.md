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
