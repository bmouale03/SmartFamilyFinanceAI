from sqlalchemy import *

from database import Base

class Compte(Base):

    __tablename__ = "comptes"

    id = Column(
        Integer,
        primary_key=True
    )

    mois_budget = Column(
        String(20),
        nullable=True
    )

    nom_compte = Column(
        String(100)
    )

    devise = Column(
        String(20),
        default="FCFA"
    )

    solde = Column(
        Numeric(15,2),
        default=0
    )

    type_compte = Column(
        String(50)
    )