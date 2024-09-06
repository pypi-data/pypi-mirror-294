# FastStream Prometheus Collector

FastStream Based Metrics Collection for Prometheus

[![PyPI](https://img.shields.io/pypi/v/faststream-prometheus)](https://pypi.org/project/faststream-prometheus/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/faststream-prometheus)](https://pypi.org/project/faststream-prometheus/)
[![GitLab last commit](https://img.shields.io/gitlab/last-commit/rocshers/python/faststream-prometheus)](https://gitlab.com/rocshers/python/faststream-prometheus)
[![Docs](https://img.shields.io/badge/docs-exist-blue)](https://projects.rocshers.com/open-source/faststream-prometheus/docs)

[![Test coverage](https://codecov.io/gitlab/rocshers:python/faststream-prometheus/graph/badge.svg)](https://codecov.io/gitlab/rocshers:python/faststream-prometheus)
[![Downloads](https://static.pepy.tech/badge/faststream-prometheus)](https://pepy.tech/project/faststream-prometheus)
[![GitLab stars](https://img.shields.io/gitlab/stars/rocshers/python/faststream-prometheus)](https://gitlab.com/rocshers/python/faststream-prometheus)

## Functionality

- Collection metrics via `middleware`
- Collecting general metrics
- Collecting `details kafka` metrics

## Installation

`pip install faststream-prometheus`

## Quick start

See [example](https://gitlab.com/rocshers/python/faststream-prometheus/-/blob/release/test_app.py) for details

```python
import uvicorn
from fastapi import FastAPI
from faststream.kafka.fastapi import KafkaRouter
from prometheus_fastapi_instrumentator import Instrumentator

# Import Faststream Middleware for collect metrics 
from faststream_prometheus import FaststreamPrometheusMiddleware

# Adding middleware 
faststream_router = KafkaRouter(
    'localhost:9092',
    middlewares=[FaststreamPrometheusMiddleware(prefix='test_faststream')],
)

# Setup export metrics via FastAPI -> HTTP GET /metrics
app = FastAPI(lifespan=faststream_router.lifespan_context)
app.include_router(faststream_router)

instrumentator = Instrumentator().instrument(app, metric_namespace='fastapi').expose(app)

```

```bash
# see default metrics
curl localhost:8000/metrics
```

## Contribute

Issue Tracker: <https://gitlab.com/rocshers/python/faststream-prometheus/-/issues>  
Source Code: <https://gitlab.com/rocshers/python/faststream-prometheus>

Before adding changes:

```bash
make install-dev
```

After changes:

```bash
make format test
```
