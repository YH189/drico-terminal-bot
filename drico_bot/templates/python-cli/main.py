"""Minimal CLI entry point (stdlib only)."""

import sys


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    print("Hello from CLI", argv)


if __name__ == "__main__":
    main()
