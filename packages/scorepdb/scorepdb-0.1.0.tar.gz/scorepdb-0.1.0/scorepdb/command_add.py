# scorep_db/add.py

import logging
from pathlib import Path
from rdflib import Graph, RDF, Namespace, Literal

from .rdf_database import get_rdf_database
from .object_store import get_object_store

from .rdf_helper import SCOREP, SCOREP_JSONLD_FILE, test_if_already_exists


def add_arguments_add(subparsers):
    parser_add = subparsers.add_parser("add", help="Add a Scorep experiment")
    parser_add.add_argument(
        "config_file", type=lambda p: Path(p).resolve(), help="Path to config file"
    )
    parser_add.add_argument(
        "mode", choices=["online", "offline"], help="Operation mode"
    )
    parser_add.add_argument(
        "experiment_path",
        type=lambda p: Path(p).resolve(),
        help="Path to Scorep experiment",
    )
    parser_add.add_argument(
        "append_files",
        type=lambda p: Path(p).resolve(),
        nargs="*",
        help="Optional additional JSON-LD files to append and merge",
    )
    parser_add.set_defaults(func=add_function)


def handle_add(
    mode: str,
    config_file: Path,
    experiment_path: Path,
    metadata_file_name: str,
    append_files: list[Path] = None,
) -> None:
    rdf_database = get_rdf_database(config_file, mode)
    object_store = get_object_store(config_file, mode)

    existing_graph = rdf_database.get_graph()

    new_graph = Graph().parse(
        str(experiment_path / metadata_file_name), format="json-ld"
    )

    # Parse and merge additional JSON-LD files if provided
    if append_files:
        for file_path in append_files:
            logging.info(f"Appending JSON-LD file: {file_path}")
            additional_graph = Graph().parse(str(file_path), format="json-ld")
            new_graph += additional_graph

        turtle_data = new_graph.serialize(format="turtle")


    already_merged = test_if_already_exists(
        existing_graph, new_graph, SCOREP.Experiment
    )

    if already_merged:
        new_graph.close()
        existing_graph.close()
        return

    new_experiment_directory_path = object_store.generate_new_experiment_path()

    subject = list(new_graph.subjects(predicate=RDF.type, object=SCOREP.Experiment))[0]
    new_graph.add((subject, SCOREP.storePath, Literal(new_experiment_directory_path)))

    new_graph.commit()

    logging.info(f"Added new attribute to {subject}")

    object_store.upload_experiment(experiment_path, new_experiment_directory_path)

    existing_graph += new_graph
    new_graph.close()
    existing_graph.commit()
    existing_graph.close()


def add_function(args):
    metadata_file_name = SCOREP_JSONLD_FILE

    config_file: Path = args.config_file
    mode: str = args.mode
    experiment_path: Path = args.experiment_path

    append_files: list[Path] = args.append_files if args.append_files else []

    if not config_file.exists():
        logging.error(f"Config file '{config_file}' does not exist. Aborting.")
        return

    if not experiment_path.exists():
        logging.error(f"Experiment path '{experiment_path}' does not exist. Aborting.")
        return

    metadata_file = experiment_path / metadata_file_name
    if not metadata_file.exists():
        logging.error(f"Metadata file '{metadata_file}' does not exist. Aborting.")
        return
    elif metadata_file.stat().st_size == 0:
        logging.error(f"Metadata file '{metadata_file}' is empty. Aborting.")
        return

    logging.info(
        f"Adding experiment with config: {config_file}, mode: {mode}, path: {experiment_path}"
    )
    handle_add(mode, config_file, experiment_path, metadata_file_name, append_files)
