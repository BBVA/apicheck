from apitest.importers import APIImporter
from apitest.importers.openapi_3 import OpenAPISource
from apitest.storages.storage_mongodb import StorageMongoDB

from .running_config import RunningConfig


def resolver_source(config: RunningConfig) -> APIImporter:
    if config.action == "openapi":
        OpenAPISource(config)


def run(config: RunningConfig):
    api = OpenAPISource("openapi.yaml")
    storage = StorageMongoDB(mongo_user="root", mongo_password="example")
    storage.save_model(api)

