#!/usr/bin/env python3
import json
import math
import time

import click
from elasticsearch import RequestError

from es_client import ESClient


@click.group()
def cli():
    pass


@cli.command()
@click.argument("index-name")
@click.option(
    "--es-host",
    default="localhost",
)
@click.option(
    "--es-user",
    default="",
)
@click.option(
    "--es-password",
    default="",
)
def setup(index_name: str, es_host: str, es_user: str, es_password: str):
    _make_index_creation_request(
        ESClient.factory(ESClient.MODE_HTTP, **(_prepare_kw_args(es_host, es_password, es_user))),
        index_name
    )


@cli.command()
@click.argument(
    'doc-as-json'
)
@click.argument(
    "doc-id",
)
@click.argument(
    "index",
)
@click.option(
    "--es-host",
    default="localhost",
)
@click.option(
    "--es-user",
    default="",
)
@click.option(
    "--es-password",
    default="",
)
def send(doc_as_json: str, doc_id: str, index: str, es_host: str, es_user: str, es_password: str):
    doc = json.loads(doc_as_json)
    merged_doc = {**(_default_doc_structure()), **doc}

    es = ESClient.factory(ESClient.MODE_HTTP, **(_prepare_kw_args(es_host, es_password, es_user)))
    es.index(index, body=merged_doc, id=doc_id)
    print("::set-output name=doc-id::" + doc_id)
    print("::set-output name=doc::" + json.dumps(merged_doc))


def _prepare_kw_args(es_host, es_password, es_user):
    kwargs = {
        "es_host": es_host,
        "es_user": es_user,
        "es_password": es_password,
    }
    return kwargs


def _make_index_creation_request(client, metric_index) -> None:
    try:
        client.indices.create(metric_index)
    except RequestError:
        pass


def _default_doc_structure() -> dict:
    return {
        "application_id": None,
        "version": None,
        "environment": None,
        "service": None,
        "meta": {},
        "status": False,
        "timestamp": math.floor(time.time_ns() / 1000 / 1000),
    }


if __name__ == '__main__':
    cli(auto_envvar_prefix="KPI")

    # This is how you produce outputs.
    # Make sure corresponds to output variable names in action.yml
    # print("::set-output name=output-one::" + output1)
    # print("::set-output name=output-two::" + output2)
