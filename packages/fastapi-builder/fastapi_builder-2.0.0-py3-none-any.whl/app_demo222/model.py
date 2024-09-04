from sqlalchemy import Column, String

from models.base import Base
from models.mixins import DateTimeModelMixin, SoftDeleteModelMixin


class Demo222(Base["Demo222"], DateTimeModelMixin, SoftDeleteModelMixin):
    __tablename__ = "demo222"

    name = Column(String(255))
