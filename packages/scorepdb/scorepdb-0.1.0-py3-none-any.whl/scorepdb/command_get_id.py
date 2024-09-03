import logging
from pathlib import Path
from rdflib import Graph, RDF

from .rdf_helper import SCOREP, SCOREP_JSONLD_FILE


def add_arguments_get_id(subparsers):
    parser_add = subparsers.add_parser("get-id", help="Add a Scorep experiment")
    parser_add.add_argument(
        "experiment_path",
        type=lambda p: Path(p).resolve(),
        help="Path to Scorep experiment",
    )
    parser_add.set_defaults(func=get_id_function)


def handle_get_id(experiment_path, metadata_file_name) -> bool:
    new_graph = Graph().parse(
        str(experiment_path / metadata_file_name), format="json-ld"
    )

    subject = list(new_graph.subjects(predicate=RDF.type, object=SCOREP.Experiment))
    assert len(subject) == 1
    subject = subject[0]

    print(str(subject))


def get_id_function(args):
    metadata_file_name = SCOREP_JSONLD_FILE

    experiment_path: Path = args.experiment_path

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

    handle_get_id(experiment_path, metadata_file_name)
