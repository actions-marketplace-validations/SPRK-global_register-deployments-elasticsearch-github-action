import click
from elasticsearch import RequestError

import metrics
from es_client import ESClient


@click.command()
@click.argument(
    "es-host",
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


def _prepare_kw_args(es_host, es_password, es_user):
    kwargs = {
        "es_host": es_host,
        "es_user": es_user,
        "es_password": es_password,
    }
    return kwargs


def _process_supported_metrics(client):
    for metric in metrics.supported_metrics:
        metric_index = metric.index(metric)
        _make_request(client, metric_index)


def _make_request(client, metric_index) -> None:
    try:
        client.indices.create(metric_index)
    except RequestError:
        pass


if __name__ == '__main__':
    setup(auto_envvar_prefix="KPI")
