"""
Make snowdrop runnable as a script with default settings.
"""

import sys
from snowdrop import cli


def main():
    """
    Entry point.
    """
    cli.main(sys.argv[1:])


if __name__ == "__main__":
    main()
