from typing import Optional

from boto3 import Session
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth


class ESClient:

    MODE_HTTP: str = 'http'
    MODE_AWS: str = 'aws'

    @classmethod
    def _build_aws_client(cls, **kwargs: Optional[str]):
        service = 'es'
        assume_role_arn = kwargs["aws_assume_role_arn"]
        aws_access_key = kwargs["aws_access_key"]
        aws_secret_key = kwargs["aws_secret_key"]
        region = kwargs["aws_region"]
        host = kwargs["es_host"]
        aws_sts_session_name = kwargs["aws_sts_session_name"]

        sess = cls._get_session(aws_access_key, aws_secret_key, region)

        if assume_role_arn is None:
            credentials = sess.get_credentials()

            awsauth = AWS4Auth(
                credentials.access_key,
                credentials.secret_key,
                region,
                service,
                session_token=credentials.token,
            )
        else:
            sts_connection = sess.client('sts')
            assume_role_object = sts_connection.assume_role(
                RoleArn=assume_role_arn, RoleSessionName=aws_sts_session_name,
                DurationSeconds=3600)
            tmp_credentials = assume_role_object['Credentials']

            assume_role_session = Session(
                aws_access_key_id=tmp_credentials['AccessKeyId'],
                aws_secret_access_key=tmp_credentials['SecretAccessKey'],
                aws_session_token=tmp_credentials['SessionToken']
            )

            credentials = assume_role_session.get_credentials()

            awsauth = AWS4Auth(
                region=region,
                service=service,
                refreshable_credentials=credentials,
            )

        return Elasticsearch(
            hosts=[{'host': host, 'port': 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection
        )

    @classmethod
    def _build_http_auth_client(cls, **kwargs: Optional[str]):
        return Elasticsearch(
            hosts=[{'host': (kwargs["es_host"]), 'port': 443}],
            http_auth=(kwargs["es_user"], kwargs["es_password"]),
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,

        )

    @classmethod
    def _get_session(cls, aws_access_key: Optional[str], aws_secret_key: Optional[str], region: str):
        has_credentials_set = aws_access_key is not None and aws_secret_key is not None

        if has_credentials_set:
            sess = Session(aws_access_key_id=aws_access_key,
                           aws_secret_access_key=aws_secret_key,
                           region_name=region)
        else:
            sess = Session(region_name=region)

        return sess

    @classmethod
    def factory(cls, name: str, **kwargs: Optional[str]) -> Elasticsearch:
        builders = {
            cls.MODE_AWS: cls._build_aws_client,
            cls.MODE_HTTP: cls._build_http_auth_client,
        }

        return builders[name](**kwargs)
