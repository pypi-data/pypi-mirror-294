"""
This module is named source instead of import because import is a Python
keyword.
"""
from flask import Blueprint
from egstudio.app.utils.api import configure_api_from_blueprint

from egstudio.app.blueprints.index.resources import (
    ConfigResource,
    IndexResource,
    InfluxStatusResource,
    StatusResource,
    StatusResourcesResource,
    StatsResource,
    TestEventsResource,
    TxtStatusResource,
)

routes = [
    ("/", IndexResource),
    ("/status", StatusResource),
    ("/status/influx", InfluxStatusResource),
    ("/status/resources", StatusResourcesResource),
    ("/status.txt", TxtStatusResource),
    ("/status/test-event", TestEventsResource),
    ("/stats", StatsResource),
    ("/config", ConfigResource),
]

blueprint = Blueprint("index", "index")
api = configure_api_from_blueprint(blueprint, routes)
