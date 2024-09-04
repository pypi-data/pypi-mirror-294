# scorep_db/object_store.py

from abc import ABC, abstractmethod
import logging
import os
import uuid
from pathlib import Path
from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error
import shutil


class ObjectStore(ABC):
    def __init__(self, config_file: Path):
        self.config_file = config_file
        load_dotenv(str(self.config_file))

    @abstractmethod
    def upload_experiment(
        self, experiment_path: Path, new_experiment_directory_path: str
    ) -> None:
        pass

    @abstractmethod
    def download_experiment(self, source_path: str, target_path: Path) -> None:
        pass

    @abstractmethod
    def generate_new_experiment_path(self) -> str:
        pass

    @abstractmethod
    def clear_storage(self) -> None:
        pass

    @abstractmethod
    def get_storage_path(self) -> str:
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """Check if the storage is reachable and configured correctly."""
        pass


class OfflineObjectStore(ObjectStore):
    def __init__(self, config_file: Path):
        super().__init__(config_file)
        self.offline_directory: Path = Path(
            os.path.expandvars(os.getenv("SCOREP_DB_OFFLINE_DIRECTORY"))
        )

    @staticmethod
    def _copy_recursive(source, target):
        src_dir = source
        dst_dir = target
        os.makedirs(dst_dir, exist_ok=True)

        for item in os.listdir(src_dir):
            s = os.path.join(src_dir, item)
            d = os.path.join(dst_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

        logging.info(f"Copied experiment directory to {dst_dir}")

    def upload_experiment(
        self, experiment_path: Path, new_experiment_directory_path: str
    ) -> None:
        target = self.offline_directory / Path(new_experiment_directory_path)
        self._copy_recursive(experiment_path, target)

    def download_experiment(self, source: Path, target: Path) -> None:
        source_ = self.offline_directory / source
        self._copy_recursive(source_, target)

    def generate_new_experiment_path(self) -> str:
        return str(uuid.uuid4())

    def clear_storage(self) -> None:
        directory_root = self.offline_directory
        if directory_root.exists():
            for item in directory_root.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
            logging.info(
                f"Cleared all contents within the offline storage at {directory_root}"
            )
        else:
            logging.info(f"No offline storage found at {directory_root}")

    def get_storage_path(self) -> str:
        return str(self.offline_directory)

    def health_check(self):
        """Check if the offline directory exists and is writable."""
        if self.offline_directory.exists() and os.access(
            self.offline_directory, os.W_OK
        ):
            logging.info(
                f"Offline storage directory '{self.offline_directory}' is accessible and writable."
            )
        else:
            raise Exception(
                f"Offline storage directory '{self.offline_directory}' is not accessible or writable."
            )


class OnlineObjectStore(ObjectStore):
    def __init__(self, config_file: Path):
        super().__init__(config_file)
        self.endpoint = f"{os.getenv('SCOREP_DB_ONLINE_OBJ_HOSTNAME')}:{os.getenv('SCOREP_DB_ONLINE_OBJ_PORT')}"
        self.access_key = os.getenv("SCOREP_DB_ONLINE_OBJ_USER")
        self.secret_key = os.getenv("SCOREP_DB_ONLINE_OBJ_PASSWORD")

        self.bucket_name = os.getenv("SCOREP_DB_ONLINE_OBJ_BUCKET_NAME")

        self.client = Minio(
            endpoint=self.endpoint,
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False,
        )

    def upload_experiment(
        self, experiment_path: Path, new_experiment_directory_path: str
    ) -> None:
        self.ensure_bucket_exists(self.bucket_name)

        base_dir = new_experiment_directory_path

        for root, dirs, files in os.walk(experiment_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                object_name = os.path.relpath(file_path, experiment_path)
                if base_dir:
                    object_name = os.path.join(base_dir, object_name)

                try:
                    self.client.fput_object(self.bucket_name, object_name, file_path)
                    logging.info(
                        f"Successfully uploaded {file_name} to {self.bucket_name}/{object_name}"
                    )
                except S3Error as e:
                    logging.error(f"Failed to upload {file_name}: {e}")

    def download_experiment(
        self, experiment_directory_path: str, local_directory: Path
    ) -> None:
        try:
            objects = self.client.list_objects(
                self.bucket_name, prefix=experiment_directory_path, recursive=True
            )
            for obj in objects:
                # Construct the local file path
                local_file_path = local_directory / obj.object_name[
                    len(experiment_directory_path) :
                ].lstrip("/")
                local_file_path.parent.mkdir(parents=True, exist_ok=True)

                # Download the object
                self.client.fget_object(
                    self.bucket_name, obj.object_name, str(local_file_path)
                )
                logging.info(
                    f"Successfully downloaded {obj.object_name} to {local_file_path}"
                )

        except S3Error as e:
            logging.error(
                f"Failed to download experiment from {experiment_directory_path}: {e}"
            )

    def ensure_bucket_exists(self, bucket_name):
        if not self.client.bucket_exists(bucket_name):
            self.client.make_bucket(bucket_name)
            logging.info(f"Bucket '{bucket_name}' created.")
        else:
            logging.info(f"Bucket '{bucket_name}' already exists.")

    def generate_new_experiment_path(self) -> str:
        return str(uuid.uuid4())

    def clear_storage(self) -> None:
        try:
            objects = self.client.list_objects(self.bucket_name, recursive=True)
            for obj in objects:
                self.client.remove_object(self.bucket_name, obj.object_name)
            logging.info(f"Cleared online storage bucket '{self.bucket_name}'")
        except S3Error as e:
            logging.error(f"Failed to clear online storage: {e}")

    def get_storage_path(self) -> str:
        return f"{self.endpoint}/{self.bucket_name}"

    def health_check(self):
        """Check if the online object store is reachable and bucket exists."""
        try:
            if self.client.bucket_exists(self.bucket_name):
                logging.info(
                    f"Online storage bucket '{self.bucket_name}' is reachable."
                )
            else:
                raise Exception(
                    f"Online storage bucket '{self.bucket_name}' does not exist."
                )

        except S3Error as e:
            raise Exception(
                f"Failed to check online storage bucket '{self.bucket_name}': {e}"
            )


def get_object_store(config_file: Path, mode: str) -> ObjectStore:
    if mode == "offline":
        return OfflineObjectStore(config_file)
    elif mode == "online":
        return OnlineObjectStore(config_file)
    else:
        logging.error(f"Unknown mode '{mode}'. Aborting.")
        raise ValueError(f"Unknown mode '{mode}'")
