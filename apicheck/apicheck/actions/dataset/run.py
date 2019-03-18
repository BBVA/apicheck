"""
This file contains python3.6+ syntax!
Feel free to import and use whatever new package you deem necessary.
"""
import dataclasses
import json
import logging
import pandas as pd
from pandas import HDFStore

from typing import Optional, List, Any, Iterable, Tuple, Set

from apicheck.db import ProxyLogs, get_engine
from apicheck.exceptions import APICheckException

from .config import RunningConfig

logger = logging.getLogger("apicheck")


def json_to_columns(df, column):
    return df[column].apply(json.loads).apply(pd.Series)


def run(running_config: RunningConfig):
    target = HDFStore(running_config.fout)
    df = pd.read_sql_table(
        "proxy_logs",
        "sqlite:///mydatabase.sqlite3",
        index_col='id'
    )

    request = json_to_columns(df, 'request')
    request["session"] = df["proxy_session_id"]
    response = json_to_columns(df, 'response')
    response["session"] = df["proxy_session_id"]
    request_headers = request['headers'].apply(pd.Series)
    response_headers = response['headers'].apply(pd.Series)
    request = request.drop("headers", 1)
    request_headers_norm = pd.melt(request_headers.reset_index(), id_vars=["id"], var_name="header")
    request_headers_norm = request_headers_norm.dropna()
    request_headers_norm["type"] = "request"
    response = response.drop("headers", 1)
    response_headers_norm = pd.melt(response_headers.reset_index(), id_vars=["id"], var_name="header")
    response_headers_norm = response_headers_norm.dropna()
    response_headers_norm["type"] = "response"
    headers_norm = pd.concat([request_headers_norm, response_headers_norm])
    target.put("request", request, format="table", data_columns=True)
    target.put("response", response, format="table", data_columns=True)
    target.put("headers", headers_norm, format="table", data_columns=True)
    target.close()

