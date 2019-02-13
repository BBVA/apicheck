from apitest.importers.openapi_3 import OpenAPISource
from apitest.storages.storage_mongodb import StorageMongoDB


def main():
    api = OpenAPISource("openapi.yaml")
    storage = StorageMongoDB(mongo_user="root", mongo_password="example")
    storage.save_model(api)


if __name__ == '__main__':
    main()
