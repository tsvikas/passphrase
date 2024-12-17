Passphrase Generator with Memorable Word Selection.

This module helps create secure passphrases.
See [this XKCD comic](https://xkcd.com/936/) about passphrases.
To correctly use a passphrase, you need to make sure your selections are
chosen at random (i.e. don't pick them yourself) and that you use enought
bits of entropy.

It draws from the most frequent words in the English language.
This ensures memorability by choosing common, easily recognized words.

It limits the wordlist to words with unique 3-letter prefixes.
The unique prefix approach enables users to potentially shorten the passphrase
while maintaining readability, as each prefix corresponds to a distinct word.

This is instead of using
[eff_large_wordlist](https://www.eff.org/document/passphrase-wordlists)
which contains many obscure or hard to spell words.
Note that this means that the wordlist is shorter, and a longer phrase is
needed to reach the same entropy.

Usage:
    $ uv run passphrase_generator.py --help
