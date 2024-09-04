from sqlalchemy_utils import UUIDType

from egstudio.app import db
from egstudio.app.models.serializer import SerializerMixin
from egstudio.app.models.base import BaseMixin


class DesktopLoginLog(db.Model, BaseMixin, SerializerMixin):
    """
    Table to log all desktop session logins. The aim is to build report that
    helps validating presence form.
    """

    person_id = db.Column(
        UUIDType(binary=False),
        db.ForeignKey("person.id"),
        nullable=False,
        index=True,
    )
    date = db.Column(db.DateTime, nullable=False)
