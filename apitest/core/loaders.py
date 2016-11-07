"""
This file contains auxiliary methods for load API Test information form:
- A MongoDB
- A JSON File
"""

import asyncio
import motor.motor_asyncio

try:
    import ujson as json
except ImportError:  # pragma no cover
    import json

from urllib.parse import urlparse

from .model import APITest
from .exceptions import ApitestConnectionError

async def _do_mongodb_query(col, query: dict):  # pragma no cover
    """
    Do a query in a MongoDB and return the result
    
    :param query: the query in MongoDB format
    :type query: dict
    
    :return: MongoDB Returned information
    :rtype: dict
    """
    # Get last inserted record
    cursor = col.find().sort("$natural", -1).limit(1)
    
    # Get the result
    return await cursor.to_list(length=1)


def _load_from_mongo(mongo_uri: str):
    """
    Load API Test information from a MongoDB.
    
    Collection used to store API Test information will be named: **apitest**
    
    >>> load_from_mongo("mongodb://127.0.0.1:27017")
    <type 'APITest'>
    
    >>> _load_from_mongo("mongodb://user:pass@mongo.example.com:27017/database")
    <type 'APITest'>
    
    :param mongo_uri: MongoDB connection string
    :type mongo_uri: str
    
    :return: Return a APITest object instance
    :rtype: APITest
    
    :raise ApitestConnectionError: If some error occurs when try to connect to MongoDB
    """
    
    try:
        # Make connection
        client = motor.motor_asyncio.AsyncIOMotorClient(mongo_uri)
        
        # Get database form connectionstring
        db = urlparse(mongo_uri).path
        if not db:
            db = "apitest"
        
        # Get database -> collection
        col = client[db]["apitest"]
        
        # Do the query
        loop = asyncio.get_event_loop()
        ret = loop.run_until_complete(_do_mongodb_query(col, {}))
        
        if ret:
            return ret[0]
        else:
            return {}
    
    except Exception as e:
        raise ApitestConnectionError from e


def _load_from_file(file_path: str):
    assert isinstance(file_path, str)
    
    # Get path
    path = file_path.replace("file://", "")
    
    with open(path, "r") as f:
        return json.loads(f.read())


def load_data(connection_string: str):
    """
    Load data from a source. Source could be:
    
    - A JSON File
    - A MongoDB
    
    Load data from a file
    ---------------------
    
    If you want to load data from a File, you must to provide this connection string:
    
    >>> connection_string = "/path/to/my/file.json"
    
    or using URI format:
    
    >>> connection_string = "file:///path/to/my/file.json"
    
    Load file from a MongoDB
    ------------------------
    
    If you want to load data from a MongoDB database, you must to provide a connection string like:
    
    >>> connection_string = "mongodb://mongo.example.com:27017"
    
    Or event more complicate:
    
    >>> connection_string = "mongodb://db1.example.net,db2.example.net:2500/?replicaSet=test"
     
    :param connection_string:
    :type connection_string:
    :return:
    :rtype:
    """
    assert isinstance(connection_string, str)
    
    if connection_string.startswith("mongodb://"):
        data = _load_from_mongo(connection_string)
    elif connection_string.startswith("file://"):
        data = _load_from_file(connection_string)
    else:
        data = _load_from_file("file://{}".format(connection_string))
            
    # Load JSON info
    return APITest(**data)


__all__ = ("load_data",)

