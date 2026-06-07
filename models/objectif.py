from sqlalchemy import *

from database import Base

class Objectif(Base):

    __tablename__ = "objectifs"

    id = Column(
        Integer,
        primary_key=True
    )

    nom = Column(
        String(150)
    )

    description = Column(Text)

    montant_cible = Column(
        Numeric(15,2)
    )

    montant_actuel = Column(
        Numeric(15,2)
    )

    date_limite = Column(Date)