"""
This module is named source instead of import because import is a Python
keyword.
"""
from flask import Blueprint
from egstudio.app.utils.api import configure_api_from_blueprint

from egstudio.app.blueprints.export.csv.assets import AssetsCsvExport
from egstudio.app.blueprints.export.csv.casting import CastingCsvExport
from egstudio.app.blueprints.export.csv.projects import ProjectsCsvExport
from egstudio.app.blueprints.export.csv.shots import ShotsCsvExport
from egstudio.app.blueprints.export.csv.persons import PersonsCsvExport
from egstudio.app.blueprints.export.csv.playlists import PlaylistCsvExport
from egstudio.app.blueprints.export.csv.task_types import TaskTypesCsvExport
from egstudio.app.blueprints.export.csv.tasks import TasksCsvExport
from egstudio.app.blueprints.export.csv.time_spents import TimeSpentsCsvExport
from egstudio.app.blueprints.export.csv.edits import EditsCsvExport

routes = [
    ("/export/csv/projects/<project_id>/assets.csv", AssetsCsvExport),
    ("/export/csv/projects/<project_id>/shots.csv", ShotsCsvExport),
    ("/export/csv/projects/<project_id>/casting.csv", CastingCsvExport),
    ("/export/csv/projects/<project_id>/edits.csv", EditsCsvExport),
    ("/export/csv/playlists/<playlist_id>", PlaylistCsvExport),
    ("/export/csv/persons.csv", PersonsCsvExport),
    ("/export/csv/projects.csv", ProjectsCsvExport),
    ("/export/csv/tasks.csv", TasksCsvExport),
    ("/export/csv/time-spents.csv", TimeSpentsCsvExport),
    ("/export/csv/task-types.csv", TaskTypesCsvExport),
]

blueprint = Blueprint("export", "export")
api = configure_api_from_blueprint(blueprint, routes)
