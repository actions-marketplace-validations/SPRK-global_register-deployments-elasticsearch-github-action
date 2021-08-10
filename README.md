# Register Deployments in ElasticSearch GitHub Action

This GitHub Action tracks deployments for applications and their statuses (successful or failed) in an Elasticsearch index. 

## Prerequisites

You'll need a reachable ElasticSearch instance and a previously created index.

## Usage

```yaml
- name: Register deployment in elasticsearch index
  uses: register-deployments-in-elasticsearch
  env:
    KPI_SEND_ES_HOST: elasticsearch-host.com
    KPI_SEND_ES_USER: elasticsearch
    KPI_SEND_ES_PASSWORD: ${{ secrets.ES_PASSWORD }}
  with:
    index: deployments
    application-id: my-app
    version: ${{ github.sha }}
    environment: "prod" # The env in which the deployment occurs, defaults to "local"
    status: "true" # JSON string representation is needed, defaults to "false"
    service-id: my-service-within-app # Optional, defaults to "null"
    meta: '{"key":"value","another_key":"another_value"}' # Custom meta JSON object, defaults to '{}'
```
