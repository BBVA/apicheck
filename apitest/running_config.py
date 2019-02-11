import abc


class APITestStorage:

    def __init__(self,
                 storage: str):
        self.storage: str = storage

    @abc.abstractmethod
    @property
    def connection_string(self) -> str:
        raise NotImplementedError()


# -------------------------------------------------------------------------
# Storage
# -------------------------------------------------------------------------
class StorageMongoDB(APITestStorage):

    __slots__ = ("mongo_host", "mongo_port", "mongo_username",
                 "mongo_password", "action")

    def __init__(self,
                 mongo_host: str,
                 mongo_port: int,
                 mongo_user: str,
                 mongo_password: str,
                 **kwargs):
        super(StorageMongoDB, self).__init__(**kwargs)

        self.mongo_port = mongo_port or 27017
        self.mongo_host = mongo_host or "127.0.0.1"
        self.mongo_username = mongo_user or None
        self.mongo_password = mongo_password or None

    @property
    def connection_string(self) -> str:
        return f"mongodb://{self.mongo_username}:{self.mongo_password}@" \
               f"{self.mongo_host}:{self.mongo_port}/"

    @classmethod
    def from_cli(cls, argparser_opt):
        return cls(**argparser_opt.__dict__)


# -------------------------------------------------------------------------
# Importers
# -------------------------------------------------------------------------
class APITestImporter:

    pass


class ImporterOpenAPI3(APITestImporter):

    def __init__(self, yaml_file: str, **kwargs):
        self.yaml_file = yaml_file

        super(ImporterOpenAPI3, self).__init__(**kwargs)

    @classmethod
    def from_cli(cls, argparser_opt):
        return cls(**argparser_opt.__dict__)


class RunningConfig:

    def __init__(self,
                 action: str,
                 storage: APITestStorage,
                 importer: APITestImporter):
        self.action: str = action
        self.storage: APITestStorage = storage
        self.importer: APITestImporter = importer


def build_config_from_argparser(action: str, argparser) -> RunningConfig:

    if action not in ("importer", "exporter"):
        raise ValueError(f"Action '{action}' is not recognized")

    # -------------------------------------------------------------------------
    # IMPORTER model action
    # -------------------------------------------------------------------------
    importer_model = None
    if action == "importer":
        importer_type = argparser.importer_type

        if importer_type == "openapi":
            importer_model = ImporterOpenAPI3.from_cli(argparser)

        else:
            raise ValueError(f"Invalid importer type: '{action}'")
    else:
        raise ValueError(f"Invalid action: '{action}'")

    # -------------------------------------------------------------------------
    # EXPORTER model action
    # -------------------------------------------------------------------------

    # -------------------------------------------------------------------------
    # STORAGE
    # -------------------------------------------------------------------------
    storage_model = None
    if argparser.storage == "mongodb":
        storage_model = StorageMongoDB.from_cli(argparser)
    else:
        raise ValueError(f"Storage backend '{argparser.storage}' is unknown")

    return RunningConfig(
        action=action,
        storage=storage_model,
        importer=importer_model
    )
