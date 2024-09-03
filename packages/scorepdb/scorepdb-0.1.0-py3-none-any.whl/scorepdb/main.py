# scorep_db/main.py

import argparse
import logging
from scorepdb.command_add import add_arguments_add
from scorepdb.command_merge import add_arguments_merge
from scorepdb.command_clear import add_arguments_clear
from scorepdb.command_query import add_arguments_query
from scorepdb.command_get_id import add_arguments_get_id
from scorepdb.command_download import add_arguments_download
from scorepdb.command_health_check import add_arguments_health_check


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
