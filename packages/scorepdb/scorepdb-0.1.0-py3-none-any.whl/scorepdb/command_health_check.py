from .rdf_database import get_rdf_database
from .object_store import get_object_store

from pathlib import Path
import logging
import sys


def add_arguments_health_check(subparsers):
    parser_health_check = subparsers.add_parser(
        "health_check", help="Verify database accessibility"
    )
    parser_health_check.add_argument(
        "config_file", type=lambda p: Path(p).resolve(), help="Path to config file"
    )
    parser_health_check.add_argument(
        "mode", choices=["offline", "online"], help="Operation mode"
    )
    parser_health_check.set_defaults(func=health_check_function)


def handle_health_check(config_file: Path, mode: str):
    rdf_db = get_rdf_database(config_file, mode)
    rdf_db.health_check()

    object_store = get_object_store(config_file, mode)
    object_store.health_check()


def health_check_function(args):
    config_file: Path = args.config_file
    mode: str = args.mode

    if not config_file.exists():
        logging.error(f"File '{config_file}' does not exist. Abort.")
        return

    handle_health_check(config_file, mode)
