from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime

from database import Base

class Patrimoine(Base):

    __tablename__ = "patrimoines"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    type_bien = Column(
        String,
        nullable=False
    )

    categorie = Column(
        String,
        nullable=False
    )

    valeur = Column(
        Float,
        nullable=False
    )

    date_creation = Column(
        DateTime
    )