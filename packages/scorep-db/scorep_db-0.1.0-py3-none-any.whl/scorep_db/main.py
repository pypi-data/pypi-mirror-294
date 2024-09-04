# scorep_db/main.py

import argparse
import logging
from .command_add import add_arguments_add
from .command_merge import add_arguments_merge
from .command_clear import add_arguments_clear
from .command_query import add_arguments_query
from .command_get_id import add_arguments_get_id
from .command_download import add_arguments_download
from .command_health_check import add_arguments_health_check


def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    parser = argparse.ArgumentParser(
        prog="scorep-db", description="Scorep-DB Command Line Tool"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_arguments_add(subparsers)
    add_arguments_merge(subparsers)
    add_arguments_clear(subparsers)
    add_arguments_query(subparsers)
    add_arguments_get_id(subparsers)
    add_arguments_download(subparsers)
    add_arguments_health_check(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
