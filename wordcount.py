"""Count the words in a text file.

Usage: python wordcount.py FILE
"""

import sys


def count_words(text):
    """Return the number of words in text (words are separated by whitespace)."""
    return len(text.split())


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("Usage: python wordcount.py FILE", file=sys.stderr)
        return 2
    path = args[0]
    try:
        with open(path, encoding="utf-8") as handle:
            text = handle.read()
    except OSError as exc:
        print(f"Cannot read {path}: {exc.strerror}", file=sys.stderr)
        return 1
    print(count_words(text))
    return 0


if __name__ == "__main__":
    sys.exit(main())
