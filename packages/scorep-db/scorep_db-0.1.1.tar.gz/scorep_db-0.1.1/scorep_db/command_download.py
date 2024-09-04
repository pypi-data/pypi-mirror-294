import logging
from pathlib import Path
from rdflib import Graph
from .rdf_database import get_rdf_database
from .object_store import get_object_store
from .exceptions import IllFormedQueryError


def add_arguments_download(subparsers):
    parser_query = subparsers.add_parser(
        "download",
        help="Download the experiments that are the result of a SPARQL query",
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
    parser_query.add_argument(
        "download_directory",
        type=lambda p: Path(p).resolve(),
        help="Path to the downloaded files",
    )

    parser_query.add_argument(
        "--dryrun",
        action="store_true",
        help="Simulate the download process without downloading files",
    )

    parser_query.set_defaults(func=download_function)


def handle_download(mode, config_file, sparql_query, download_directory, dryrun=False):
    rdf_database: Graph = get_rdf_database(config_file, mode).get_graph()

    # Execute the query
    try:
        results = rdf_database.query(sparql_query)

        logging.info("Query executed successfully.")

    except Exception as e:
        logging.error(f"Failed to execute query: {e}")

    # Handle the results.

    already_downloaded = {}

    for i, row in enumerate(results, start=1):
        # Iterate Result Subjects
        experiment_id: str = None
        store_path: str = None

        new_name = {}
        for var in row.labels:
            key = str(var).strip()
            value = str(row[var]).strip()

            if value == "":
                # This might not be needed? This prevents from empty keys being present
                continue

            if key.lower() == "experiment":
                experiment_id = value
                continue

            if key.lower() == "storepath":
                store_path = value
                continue

            # Collect key value pairs for the download
            new_name[str(key)] = str(value.strip())

        if experiment_id is None:
            raise IllFormedQueryError(
                f"The used SPARQL query has no '?Experiment' result, but this is needed!"
            )
        if store_path is None:
            raise IllFormedQueryError(
                f"The used SPARQL query has no '?StorePath' result, but this is needed!"
            )

        print(f"Working on '{experiment_id}'")

        if not new_name:
            # Use "old" store path as fallback
            new_name[store_path] = ""

        row_result = {"source_path": store_path, "target_path": new_name}

        if already_downloaded.get(experiment_id, False):
            logging.info(f"Updating exsiting entry for {experiment_id}")
            # There was already a matching experiment
            #  --> Update target path with new path
            existing_experiment = already_downloaded.get(experiment_id)

            existing_experiment["target_path"].update(new_name)

        else:
            logging.info(f"New entry for {experiment_id}")
            # No previous entry
            already_downloaded[experiment_id] = row_result
        print("-" * 40)

    if dryrun:
        logging.info("Dry run mode enabled. The following files would be downloaded:")
    else:
        object_store = get_object_store(config_file, mode)

    for id, v in already_downloaded.items():
        source_path = v["source_path"]

        new_target_name = v["target_path"]

        new_name_string = []
        for sorted_keys in sorted(new_target_name.keys()):
            new_name_string.append(sorted_keys + "_" + new_target_name[sorted_keys])

        merged_string = ".".join(new_name_string)

        # Append the run_id to the folder to make sure that no overwriting takes place.
        merged_string += f".{id.split('/')[-1]}"

        target_path: Path = Path(download_directory) / Path(merged_string)

        if dryrun:
            logging.info(
                f"Would download\n\t'{id}'\nfrom\n\t'{source_path}'\nto\n\t'{target_path}'"
            )
        else:
            object_store.download_experiment(source_path, target_path)
            logging.info(f"Downloaded\t\n'{id}'\nto\n\t'{target_path}'")

    rdf_database.close()


def download_function(args):
    config_file: Path = args.config_file
    mode: str = args.mode
    query_file: Path = args.query_file
    download_directory: Path = args.download_directory
    dryrun: bool = args.dryrun

    if not config_file.exists():
        logging.error(f"Config file '{config_file}' does not exist. Aborting.")
        return

    if not query_file.exists():
        logging.error(f"Query file '{query_file}' does not exist. Aborting.")
        return

    if not download_directory.exists():
        logging.error(
            f"Download destination directory '{download_directory}' does not exist. Aborting."
        )
        return

    # Read the query
    with query_file.open("r") as file:
        sparql_query = file.read()

    logging.info(f"Executing SPARQL query from file: {query_file}")

    handle_download(mode, config_file, sparql_query, download_directory, dryrun)
    # Connect to the RDF database
