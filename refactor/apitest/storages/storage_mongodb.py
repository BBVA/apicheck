import logging

import pymongo
from slugify import slugify

from pymongo import MongoClient

from apitest.model_maps import APITestModel, EndPoint, APIMetadata
from apitest.importers import APIImporter

log = logging.getLogger(__name__)


class StorageMongoDB:

    def __init__(self,
                 *,
                 mongo_host: str = "localhost",
                 mongo_port: int = 27017,
                 mongo_user: str = None,
                 mongo_password: str = None):
        self.mongo_port = mongo_port or 27017
        self.mongo_host = mongo_host or "localhost"

        self.mongo_user = mongo_user or None
        self.mongo_password = mongo_password or None

        self._mongo_connection = None
        self._collection = None
        self._db = None

    @property
    def db(self):
        if not self._db:
            self._db = getattr(self.connection, "apitest")

        return self._db

    @property
    def connection(self):
        if not self._mongo_connection:
            log.debug(f"Connecting to MongoDB: "
                      f"'{self.mongo_host}':'{self.mongo_port}'")

            self._mongo_connection = MongoClient(
                host=self.mongo_host,
                port=self.mongo_port,
                username=self.mongo_user,
                password=self.mongo_password
            )

        return self._mongo_connection

    def __update_metadata(self, model: APIImporter):

        collection = getattr(self.db, "metadata")

        # Indexing
        collection.create_index([
            ('version', pymongo.ASCENDING),
            ('deployments.domain', pymongo.ASCENDING)
        ], unique=True)

        try:
            collection.insert_one(model.metadata.to_dict())
        except pymongo.errors.DuplicateKeyError:
            pass

    def get_api_collection(self, model: APIImporter):

        #
        # Before getting collection for the API, update the global metadata
        # and global deployment collections
        #
        self.__update_metadata(model)

        collection = getattr(self.db, model.metadata.name)

        # Indexing
        collection.create_index([
            ('metadata', pymongo.ASCENDING),
            ('uri', pymongo.ASCENDING)
        ], unique=True)

        return collection

    def save_model(self, model: APIImporter):

        collection = self.get_api_collection(model)

        # Indexing
        collection.create_index([
            ('metadata.version', pymongo.ASCENDING),
            ('metadata.base_api_path', pymongo.ASCENDING),
            ('uri', pymongo.ASCENDING)
        ], unique=True)

        for end_point in model.end_points:
            try:
                to_insert = end_point.to_dict()
                to_insert["metadata"] = model.metadata.to_dict()

                collection.insert_one(to_insert)
            except pymongo.errors.DuplicateKeyError:
                pass
