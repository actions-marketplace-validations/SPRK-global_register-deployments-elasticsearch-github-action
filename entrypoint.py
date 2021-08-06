#!/usr/bin/env python3
import json

import click
from elasticsearch import RequestError

import metrics
from es_client import ESClient


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--es-host",
)
@click.option(
    "--es-user",
)
@click.option(
    "--es-password",
)
def setup(es_host: str, es_user: str, es_password: str):
    _process_supported_metrics(
        ESClient.factory(
            ESClient.MODE_HTTP,
            **(_prepare_kw_args(es_host, es_password, es_user))
        )
    )


@cli.command()
@click.argument(
    'doc_as_json'
)
@click.option(
    "--es-host",
)
@click.option(
    "--es-user",
)
@click.option(
    "--es-password",
)
def deployment(doc_as_json: str, es_host: str, es_user: str, es_password: str):
    doc = json.loads(doc_as_json)
    merged_doc = {**(_default_doc_structure()), **doc}
    new_deployment = metrics.Deployment(
        merged_doc["application_id"],
        merged_doc["version"],
        merged_doc["environment"],
        merged_doc["service"],
        merged_doc["meta"],
        bool(merged_doc["status"]),
    )

    es = ESClient.factory(ESClient.MODE_HTTP, **(_prepare_kw_args(es_host, es_password, es_user)))
    es.index(metrics.Deployment.index(), body=new_deployment.__dict__, id=new_deployment.id())


def _prepare_kw_args(es_host, es_password, es_user):
    kwargs = {
        "es_host": es_host,
        "es_user": es_user,
        "es_password": es_password,
    }
    return kwargs


def _process_supported_metrics(client):
    for metric in metrics.supported_metrics:
        metric_index = metric.index()
        _make_request(client, metric_index)


def _make_request(client, metric_index) -> None:
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
        "meta": None,
        "status": None,
    }


if __name__ == '__main__':
    cli(auto_envvar_prefix="KPI")

    # This is how you produce outputs.
    # Make sure corresponds to output variable names in action.yml
    # print("::set-output name=output-one::" + output1)
    # print("::set-output name=output-two::" + output2)
