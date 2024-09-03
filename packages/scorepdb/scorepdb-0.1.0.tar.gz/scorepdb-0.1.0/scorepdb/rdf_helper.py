from rdflib import Namespace, Graph, RDF, URIRef
import logging
from contextlib import contextmanager

SCOREP = Namespace("http://scorep-fair.github.io/ontology#")
SCOREP_JSONLD_FILE = "scorep.fair.json"


def test_if_already_exists(database: Graph, new_entry: Graph, key: URIRef) -> bool:
    subject = list(new_entry.subjects(predicate=RDF.type, object=key))
    assert len(subject) == 1
    subject = subject[0]

    if (subject, RDF.type, SCOREP.Experiment) in database:
        logging.info(f"The subject '{subject}' already exists in the existing graph.")
        return True
    else:
        logging.info(f"The subject '{subject}' does not exist in the existing graph.")
        return False
