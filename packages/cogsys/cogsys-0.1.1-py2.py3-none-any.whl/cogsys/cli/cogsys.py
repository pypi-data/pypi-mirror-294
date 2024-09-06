"""Console script for cogsys."""

import argparse
import sys


def main():
    """Console script for cogsys."""
    parser = argparse.ArgumentParser()
    parser.add_argument("_", nargs="*")
    args = parser.parse_args()

    str0 = (
        "🚀🚀🚀 Replace this message by putting your code into cogsys.cli.cogsys:main"
    )

    print("Arguments: " + str(args._))
    print(str0)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
