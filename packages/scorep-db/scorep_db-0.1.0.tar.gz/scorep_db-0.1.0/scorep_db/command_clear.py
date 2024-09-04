import logging
from pathlib import Path
from .rdf_database import get_rdf_database
from .object_store import get_object_store


def add_arguments_clear(subparsers):
    parser_clear = subparsers.add_parser(
        "clear", help="Clear the databases and storage"
    )
    parser_clear.add_argument(
        "config_file", type=lambda p: Path(p).resolve(), help="Path to config file"
    )
    parser_clear.add_argument(
        "mode", choices=["online", "offline"], help="Operation mode"
    )
    parser_clear.set_defaults(func=clear_function)


def clear_function(args):
    config_file: Path = args.config_file
    mode: str = args.mode

    if not config_file.exists():
        logging.error(f"Config file '{config_file}' does not exist. Aborting.")
        return

    logging.info(f"Clearing databases and storage for mode: {mode}")

    rdf_database = get_rdf_database(config_file, mode)
    object_store = get_object_store(config_file, mode)

    confirmation = input(
        f"Are you sure you want to clear all data in the following paths?\n"
        f"RDF Database: '{rdf_database.get_database_path()}'\n"
        f"Object Store: '{object_store.get_storage_path()}'\n"
        f"This action cannot be undone. (yes/no): "
    )
    if confirmation.lower() != "yes":
        logging.info("Clear operation aborted by the user.")
        return

    logging.info("User confirmed. Proceeding with clearing operation.")

    # Clear RDF Database

    existing_graph = rdf_database.get_graph()
    existing_graph.remove((None, None, None))  # Remove all triples
    existing_graph.commit()
    existing_graph.close()
    logging.info("RDF database cleared.")

    # Clear Object Store

    object_store.clear_storage()
    logging.info("Object store cleared.")
