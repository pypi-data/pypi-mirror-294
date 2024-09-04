# scorep_db/rdf_database.py

from abc import ABC, abstractmethod
import logging
import os
from pathlib import Path
from dotenv import load_dotenv
from rdflib import Graph, URIRef
from rdflib_sqlalchemy import registerplugins
from rdflib_sqlalchemy.store import SQLAlchemy
import contextlib

registerplugins()


class RDFDatabase(ABC):
    def __init__(self, config_file: Path):
        self.config_file = config_file
        load_dotenv(str(self.config_file))

    @abstractmethod
    def get_graph(self) -> Graph:
        pass

    @staticmethod
    def open_graph(db_path: str) -> Graph:
        static_identifier = URIRef("http://internal.scorep.org/")
        with contextlib.suppress(TypeError):
            store = SQLAlchemy(identifier=None)
            graph = Graph(store=store, identifier=static_identifier)

        try:
            graph.open(db_path, create=False)
        except RuntimeError:
            graph.open(db_path, create=True)

        return graph

    @abstractmethod
    def get_database_path(self) -> str:
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check if the RDF database is reachable and configured correctly."""
        pass


class OfflineRDFDatabase(RDFDatabase):
    def __init__(self, config_file: Path):
        super().__init__(config_file)
        self.scorep_db_path = Path(
            os.path.expandvars(os.getenv("SCOREP_DB_OFFLINE_PATH"))
        )
        self.scorep_db_name = Path(os.getenv("SCOREP_DB_OFFLINE_NAME"))

    def get_graph(self) -> Graph:
        db_path = f"sqlite:///{self.scorep_db_path / self.scorep_db_name}"

        logging.info(f"Connecting to offline database at {db_path}")

        return self.open_graph(db_path)

    def get_database_path(self) -> str:
        return str(self.scorep_db_path / self.scorep_db_name)

    def health_check(self):
        """Check if the offline RDF database file exists and is accessible."""
        if self.scorep_db_path.exists():  # and self.scorep_db_name.exists():
            logging.info(
                f"Offline RDF database file '{self.scorep_db_path / self.scorep_db_name}' is accessible."
            )
        else:
            raise Exception(
                f"Offline RDF database file '{self.scorep_db_path / self.scorep_db_name}' is not accessible."
            )


class OnlineRDFDatabase(RDFDatabase):
    def __init__(self, config_file: Path):
        super().__init__(config_file)
        self.hostname = os.getenv("SCOREP_DB_ONLINE_RDF_HOSTNAME")
        self.port = os.getenv("SCOREP_DB_ONLINE_RDF_PORT")
        self.user = os.getenv("SCOREP_DB_ONLINE_RDF_USER")
        self.password = os.getenv("SCOREP_DB_ONLINE_RDF_PASSWORD")
        self.scorep_db_name = os.getenv("SCOREP_DB_ONLINE_RDF_DB_NAME")

    def get_graph(self) -> Graph:
        db_path = self._get_db_path()

        logging.info(f"Connecting to online database at {db_path}")

        return self.open_graph(db_path)

    def get_database_path(self) -> str:
        return f"{self.user}@{self.hostname}:{self.port}/{self.scorep_db_name}"

    def health_check(self) -> bool:
        """Check if the online RDF database is reachable by attempting a connection."""
        try:
            db_path = self._get_db_path()
            graph = self.open_graph(db_path)
            if graph:
                logging.info(
                    f"Successfully connected to the online RDF database at '{db_path}'."
                )

            else:
                raise Exception(
                    f"Failed to connect to the online RDF database at '{db_path}'."
                )
        except Exception as e:
            raise Exception(f"Failed to check online RDF database: '{e}'")

    def _get_db_path(self) -> str:
        return f"postgresql+psycopg2://{self.user}:{self.password}@{self.hostname}:{self.port}/{self.scorep_db_name}"


def get_rdf_database(config_file: Path, mode: str) -> RDFDatabase:
    if mode == "offline":
        return OfflineRDFDatabase(config_file)
    elif mode == "online":
        return OnlineRDFDatabase(config_file)
    else:
        logging.error(f"Unknown mode '{mode}'. Aborting.")
        raise ValueError(f"Unknown mode '{mode}'")
