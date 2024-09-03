import logging
from pathlib import Path
from .rdf_database import get_rdf_database


def add_arguments_query(subparsers):
    parser_query = subparsers.add_parser(
        "query", help="Execute a SPARQL query on the RDF database"
    )
    parser_query.add_argument(
        "config_file", type=lambda p: Path(p).resolve(), help="Path to config file"
    )
    parser_query.add_argument(
        "mode", choices=["offline", "online"], help="Operation mode"
    )
    parser_query.add_argument(
        "query_file", type=lambda p: Path(p).resolve(), help="Path to SPARQL query file"
    )
    parser_query.set_defaults(func=query_function)


def query_function(args):
    config_file: Path = args.config_file
    mode: str = args.mode
    query_file: Path = args.query_file

    if not config_file.exists():
        logging.error(f"Config file '{config_file}' does not exist. Aborting.")
        return

    if not query_file.exists():
        logging.error(f"Query file '{query_file}' does not exist. Aborting.")
        return

    # Read the query
    with query_file.open("r") as file:
        sparql_query = file.read()

    logging.info(f"Executing SPARQL query from file: {query_file}")

    # Connect to the RDF database
    rdf_database = get_rdf_database(config_file, mode).get_graph()

    # Execute the query
    try:
        results = rdf_database.query(sparql_query)

        for i, row in enumerate(results, start=1):
            print(f"Result {i}:")
            for var in row.labels:
                print(f"  {var}: {row[var]}")
            print("-" * 40)

        logging.info("Query executed successfully.")

    except Exception as e:
        logging.error(f"Failed to execute query: {e}")

    finally:
        rdf_database.close()
