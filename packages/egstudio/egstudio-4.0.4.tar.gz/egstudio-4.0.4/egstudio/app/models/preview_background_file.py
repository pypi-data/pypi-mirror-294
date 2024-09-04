from egstudio.app import db
from egstudio.app.models.serializer import SerializerMixin
from egstudio.app.models.base import BaseMixin


class PreviewBackgroundFile(db.Model, BaseMixin, SerializerMixin):
    """
    Describe a preview background file.
    """

    name = db.Column(db.String(40), nullable=False)
    archived = db.Column(db.Boolean(), default=False)
    is_default = db.Column(db.Boolean(), default=False, index=True)
    original_name = db.Column(db.String(250))
    extension = db.Column(db.String(6))
    file_size = db.Column(db.BigInteger(), default=0)
