from pathlib import Path
import logging
from rdflib import Graph, Namespace, Literal, RDF

from .rdf_database import get_rdf_database
from .object_store import get_object_store

from .rdf_helper import SCOREP, SCOREP_JSONLD_FILE, test_if_already_exists


def add_arguments_merge(subparsers):
    parser_add = subparsers.add_parser(
        "merge", help="Merge an offline database into an online database"
    )
    parser_add.add_argument(
        "config_file", type=lambda p: Path(p).resolve(), help="Path to config file"
    )
    parser_add.add_argument(
        "--dryrun",
        action="store_true",
        help="Simulate the download process without downloading files",
    )

    parser_add.set_defaults(func=merge_function)


def handle_merge(config_file: Path, dryrun: bool = False):
    local_rdf_db: Graph = get_rdf_database(config_file, "offline").get_graph()
    remote_rdf_db: Graph = get_rdf_database(config_file, "online").get_graph()

    local_object_store = get_object_store(config_file, "offline")
    remote_object_store = get_object_store(config_file, "online")

    local_experiments = list(
        local_rdf_db.subjects(predicate=RDF.type, object=SCOREP.Experiment)
    )
    assert len(local_experiments) > 1

    for local_experiment in local_experiments:
        if (local_experiment, RDF.type, SCOREP.Experiment) in remote_rdf_db:
            continue
        if not local_experiment:
            print("None local experiment")

            continue

        store_path = None
        for obj in local_rdf_db.objects(
            subject=local_experiment, predicate=SCOREP.storePath
        ):
            store_path = obj
            break
        print(f"{store_path=}")
        if not store_path:
            logging.error(
                f"Entry '{local_experiment}' has no store path! This should not have happened."
            )
            raise ValueError

        local_store_path = Path(str(store_path))

        local_db_root = Path(local_object_store.get_storage_path())
        # Reuse the old name for upload.
        # Directly upload the files without moving them into a local storage

        if dryrun:
            logging.info(f"Dryrun: Would upload {local_experiment}.")
        else:
            logging.info(f"Upload {local_experiment}.")
            remote_object_store.upload_experiment(
                local_db_root / local_store_path, local_store_path
            )

    if dryrun:
        logging.info(f"Dryrun: Would merge graphs.")
    else:
        logging.info(f"Merging graphs.")
        remote_rdf_db += local_rdf_db
        remote_rdf_db.commit()

    remote_rdf_db.close()
    local_rdf_db.close()

    return


def merge_function(args):
    config_file: Path = args.config_file
    dryrun: bool = args.dryrun

    if not config_file.exists():
        logging.error(f"File '{config_file}' does not exist. Abort.")

    handle_merge(config_file, dryrun)
