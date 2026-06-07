from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base

class Membre(Base):

    __tablename__ = "membres"

    id = Column(
        Integer,
        primary_key=True
    )

    nom = Column(
        String(100)
    )

    lien_parental = Column(
        String(100)
    )